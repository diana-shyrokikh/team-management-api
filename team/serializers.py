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


class TypeDetailSerializer(serializers.ModelSerializer):
    teams = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
        allow_null=True,
    )

    class Meta:
        model = Type
        fields = (
            "id",
            "name",
            "teams",
        )


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
        queryset=get_user_model().objects.select_related(
            "team"
        )
    )

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "type",
            "leader",
        )


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


class TeamDetailSerializer(TeamSerializer):
    tasks = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field="name",
        allow_null=True,
        queryset=Task.objects.select_related("team")
    )
    members = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "type",
            "leader",
            "members",
            "tasks",
        )

    @staticmethod
    def get_members(obj):
        members = obj.members.all()
        return [member.get_full_name() for member in members]


class TeamCreateUpdateSerializer(TeamDetailSerializer):
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
            "tasks",
        )

    def validate(self, attrs):
        data = super(
            TeamSerializer, self
        ).validate(attrs)
        name = (
            self.instance.name
            if not attrs.get("name")
            else attrs.get("name")
        )

        validate_name(
            name=name,
            field_name="name"
        )

        if attrs.get("leader"):
            validate_leader(
                leader=attrs["leader"],
                team_name=name,
            )

        if attrs.get("members"):
            validate_members(
                members=attrs["members"],
                team_name=name,
            )

        return data

    def update(self, instance, validated_data):
        leader = validated_data.get("leader")

        if (
            not leader and instance.leader
        ) or (
            leader
            and instance.leader
            and leader != instance.leader
        ):
            instance.leader.is_leader = False
            instance.leader.save()

        instance = super(
            TeamSerializer, self
        ).update(instance, validated_data)

        if leader:
            leader.is_leader = True
            leader.team = instance
            leader.save()
            instance.members.add(leader)
            instance.save()

        return instance

    def create(self, validated_data):
        leader_data = validated_data.pop("leader", None)
        members_data = validated_data.pop("members", [])
        tasks_data = validated_data.pop("tasks", [])
        team = Team.objects.create(**validated_data)

        if leader_data:
            team.leader = leader_data
            leader_data.is_leader = True
            leader_data.team = team

            leader_data.save()
            members_data.append(leader_data)

        team.members.set(members_data)
        team.tasks.set(tasks_data)
        team.save()

        return team
