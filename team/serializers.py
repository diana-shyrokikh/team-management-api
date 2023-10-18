from rest_framework import serializers

from team.models import Type
from team_management.validators import validate_name


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"

    def validate(self, attrs):
        data = super(
            TypeSerializer, self
        ).validate(attrs)

        validate_name(
            name=attrs["name"],
            field_name="name"
        )

        return data
