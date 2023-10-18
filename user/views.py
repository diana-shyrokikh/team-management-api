from django.contrib.auth import get_user_model
from rest_framework import viewsets

from user.serializers import (
    UserSerializer,
    UserMiniSerializer,
    UserDetailUpdateSerializer,
)


class UserView(viewsets.ModelViewSet):
    queryset = get_user_model().objects.select_related(
        "team"
    )

    def get_serializer_class(self):
        if self.action == "list":
            return UserMiniSerializer

        if self.action in ("update", "retrieve"):
            return UserDetailUpdateSerializer

        return UserSerializer

