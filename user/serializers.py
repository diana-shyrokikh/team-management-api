from django.contrib.auth import get_user_model
from rest_framework import serializers

from team_management.validators import validate_user_name


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "first_name",
            "last_name",
            "password"
        )

    def validate(self, attrs):
        data = super(
            UserSerializer, self
        ).validate(attrs)

        if attrs["first_name"]:
            validate_user_name(
                name=attrs["first_name"],
                field_name="first_name"
            )

        if attrs["last_name"]:
            validate_user_name(
                name=attrs["last_name"],
                field_name="last_name"
            )

        return data

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserDetailUpdateSerializer(UserSerializer):
    team = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name",
        allow_null=True,
    )
    is_leader = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "team",
            "is_leader",
            "password",
        )


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "full_name",
        )
