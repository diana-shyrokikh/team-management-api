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


class TypeView(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class TeamView(viewsets.ModelViewSet):
    queryset = Team.objects.select_related(
        "leader", "type"
    ).prefetch_related("members", "tasks")

    def get_serializer_class(self):
        if self.action == "list":
            return TeamSerializer
        if self.action in ("create", "update"):
            return TeamCreateUpdateSerializer

        return TeamDetailSerializer


class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("team")

    def get_serializer_class(self):
        if self.action in (
            "create", "update", "retrieve"
        ):
            return TaskDetailSerializer

        return TaskSerializer
