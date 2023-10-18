from rest_framework import viewsets

from team.models import (
    Type,
    Team,
)
from team.serializers import (
    TypeSerializer,
    TeamSerializer,
)


class TypeView(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class TeamView(viewsets.ModelViewSet):
    queryset = Team.objects.select_related(
        "leader", "type"
    )
    serializer_class = TeamSerializer
