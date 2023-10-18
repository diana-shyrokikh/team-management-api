from django.contrib.auth import get_user_model
from rest_framework import serializers

from team.models import (
    Type,
    Team,
    Task,
)
from team_management.validators import (
    validate_name,
    validate_leader,
    validate_members,
)


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


class TeamSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
        queryset=Type.objects.all()

    )
    leader = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="email",
        allow_null=True,
        queryset=get_user_model().objects.all()
    )
    members = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field="email",
        allow_null=True,
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "type",
            "leader",
            "members",
        )

    def validate(self, attrs):
        data = super(
            TeamSerializer, self
        ).validate(attrs)

        validate_name(
            name=attrs["name"],
            field_name="name"
        )

        if attrs["leader"]:
            validate_leader(
                leader=attrs["leader"]
            )

        if attrs["members"]:
            validate_members(
                members=attrs["members"]
            )

        return data

    def update(self, instance, validated_data):
        leader = validated_data.get("leader")

        if not leader and instance.leader:
            instance.leader.is_leader = False
            instance.leader.save()

        instance = super(
            TeamSerializer, self
        ).update(instance, validated_data)

        return instance


class TaskSerializer(serializers.ModelSerializer):
    team = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
        queryset=Team.objects.select_related(
            "leader", "type"
        ).prefetch_related("members")
    )

    class Meta:
        model = Task
        fields = (
            "id",
            "name",
            "status",
            "team",
        )


class TaskDetailSerializer(TaskSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "name",
            "status",
            "team",
            "description"
        )

    def validate(self, attrs):
        data = super(
            TaskSerializer, self
        ).validate(attrs)

        validate_name(
            name=attrs["name"],
            field_name="name"
        )

        return data
