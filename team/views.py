from rest_framework import viewsets

from team.models import Type
from team.serializers import TypeSerializer


class TypeView(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
