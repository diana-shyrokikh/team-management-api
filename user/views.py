from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, generics
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

from team_management.paginations import TwentySizePagination
from user.serializers import (
    UserSerializer,
    UserMiniSerializer,
    UserDetailUpdateSerializer,
)


@extend_schema(tags=["User (Admin/Staff required)"])
class UserView(viewsets.ModelViewSet):
    queryset = get_user_model().objects.select_related(
        "team"
    )
    pagination_class = TwentySizePagination
    permission_classes = [IsAdminUser, ]

    def get_serializer_class(self):
        if self.action == "list":
            return UserMiniSerializer

        if self.action in ("update", "retrieve"):
            return UserDetailUpdateSerializer

        return UserSerializer


@extend_schema(tags=["User Profile"])
class UserMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailUpdateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user


@extend_schema(tags=["JWT Tokens"])
class TokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=["JWT Tokens"])
class TokenRefreshView(TokenRefreshView):
    pass
