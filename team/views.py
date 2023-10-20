from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from team.models import (
    Type,
    Team,
    Task,
)
from team.serializers import (
    TypeSerializer,
    TeamSerializer,
    TaskSerializer,
    TaskDetailSerializer,
    TeamDetailSerializer,
    TeamCreateUpdateSerializer,
    TypeDetailSerializer,
)
from team_management.paginations import (
    TwentySizePagination,
    TenSizePagination,
)
from team_management.permissions import (
    IsTeamMemberOrIsAdmin,
    IsUsersTaskOrIsAdmin,
)


@extend_schema(tags=["Type"])
class TypeView(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    pagination_class = TwentySizePagination
    permission_classes = [IsAdminUser, ]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TypeDetailSerializer

        return TypeSerializer


@extend_schema(tags=["Team"])
class TeamView(viewsets.ModelViewSet):
    queryset = Team.objects.select_related(
        "leader", "type"
    ).prefetch_related("members", "tasks")
    pagination_class = TenSizePagination
    permission_classes = [IsTeamMemberOrIsAdmin, ]

    def get_serializer_class(self):
        if self.action == "list":
            return TeamSerializer
        if self.action in ("create", "update"):
            return TeamCreateUpdateSerializer

        return TeamDetailSerializer


@extend_schema(tags=["Task"])
class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("team")
    pagination_class = TenSizePagination
    permission_classes = [IsUsersTaskOrIsAdmin, ]

    def get_serializer_class(self):
        if self.action in (
            "create", "update", "retrieve"
        ):
            return TaskDetailSerializer

        return TaskSerializer
