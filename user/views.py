from django.contrib.auth import get_user_model
from rest_framework import viewsets

from team_management.paginations import TwentySizePagination
from user.serializers import (
    UserSerializer,
    UserMiniSerializer,
    UserDetailUpdateSerializer,
)


class UserView(viewsets.ModelViewSet):
    queryset = get_user_model().objects.select_related(
        "team"
    )
    pagination_class = TwentySizePagination

    def get_serializer_class(self):
        if self.action == "list":
            return UserMiniSerializer

        if self.action in ("update", "retrieve"):
            return UserDetailUpdateSerializer

        return UserSerializer

