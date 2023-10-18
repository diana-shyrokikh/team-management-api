import re

from rest_framework.exceptions import ValidationError

NAME_PATTERN = r"^[A-Za-z][A-Za-z0-9\s]*$"


def validate_name(
        name: str, field_name: str
) -> str | ValidationError:
    if not re.search(NAME_PATTERN, name.strip()):
        raise ValidationError({
            f"{field_name}":
                f"{field_name.upper()} should starts with letter "
                f"and contain only letters, digits and space"

        })

    return name.strip()
