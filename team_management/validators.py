import re

from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

NAME_PATTERN = r"^[A-Za-z][A-Za-z0-9-\s]*$"
USER_NAME_PATTERN = r"^[A-Za-z][A-Za-z\s]*$"


def validate_name(
        name: str, field_name: str,
) -> str | ValidationError:
    if not re.search(NAME_PATTERN, name.strip()):
        raise ValidationError({
            f"{field_name}":
                f"The {field_name} should starts with letter "
                f"and contain only letters, digits and space"
        })

    return name.strip()


def validate_user_name(
        name: str, field_name: str,
) -> str | ValidationError:
    if not re.search(USER_NAME_PATTERN, name.strip()):
        raise ValidationError({
            f"{field_name}":
                f"The {field_name} should starts with letter "
                f"and contain only letters and space"
        })

    return name.strip()


def validate_leader(
        leader: get_user_model(),
        team_name: str
) -> get_user_model() | ValidationError:
    if leader.team and leader.team.name != team_name:
        raise ValidationError({
            "leader":
                "The user cannot be the leader and "
                "a member of another team at the same time"
        })

    return leader


def validate_members(
        members: list[get_user_model()],
        team_name: str
) -> get_user_model() | ValidationError:
    for member in members:
        if member.is_leader:
            if team_name != member.team.name:
                raise ValidationError({
                    "members":
                        f"The {member.email} cannot be a team member "
                        f"because the user is the leader of another team"
                })

    return members
