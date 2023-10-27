from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from google_api_auth.serializers import InputSerializer
from google_api_auth.utils import (
    GoogleSdkLoginFlowService,
    get_jwt_pair_token,
)

from team_management import settings


class GoogleLoginRedirectView(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        google_login_flow = GoogleSdkLoginFlowService()

        authorization_url = google_login_flow.get_authorization_url()

        return redirect(authorization_url)


class GoogleLoginView(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        input_serializer = InputSerializer(data=request.GET)

        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get("code")
        error = validated_data.get("error")
        state = validated_data.get("state")

        if error is not None:
            return Response(
                {"error": error},
                status=status.HTTP_400_BAD_REQUEST
            )

        if code is None or state is None:
            return Response(
                {"error": "Code and state are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        google_login_flow = GoogleSdkLoginFlowService()

        google_tokens = google_login_flow.get_tokens(
            code=code, state=state
        )

        id_token_decoded = google_tokens.decode_id_token()

        user_email = id_token_decoded["email"]
        user_last_name = id_token_decoded.get("family_name")
        user_default_password = (
            f"{user_email}123456{user_last_name}"
            if not settings.DEFAULT_USER_PASSWORD
            else settings.DEFAULT_USER_PASSWORD
        )
        user = get_user_model().objects.filter(email=user_email)

        if not user:
            get_user_model().objects.create_user(
                email=user_email,
                first_name=id_token_decoded["given_name"],
                last_name=id_token_decoded["family_name"],
                password=user_default_password
            )

        return Response(
            get_jwt_pair_token(
                user_email, user_default_password
            ),
            status=status.HTTP_200_OK
        )
