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
)


class TypeView(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class TeamView(viewsets.ModelViewSet):
    queryset = Team.objects.select_related(
        "leader", "type"
    ).prefetch_related("members")
    serializer_class = TeamSerializer


class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("team")
    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.action in (
            "create", "update", "retrieve"
        ):
            return TaskDetailSerializer

        return TaskSerializer
