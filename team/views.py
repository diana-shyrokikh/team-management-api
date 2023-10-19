from rest_framework import viewsets

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
)
from team_management.paginations import (
    TwentySizePagination,
    TenSizePagination,
)


class TypeView(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    pagination_class = TwentySizePagination


class TeamView(viewsets.ModelViewSet):
    queryset = Team.objects.select_related(
        "leader", "type"
    ).prefetch_related("members", "tasks")
    pagination_class = TenSizePagination

    def get_serializer_class(self):
        if self.action == "list":
            return TeamSerializer
        if self.action in ("create", "update"):
            return TeamCreateUpdateSerializer

        return TeamDetailSerializer


class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("team")
    pagination_class = TenSizePagination

    def get_serializer_class(self):
        if self.action in (
            "create", "update", "retrieve"
        ):
            return TaskDetailSerializer

        return TaskSerializer
