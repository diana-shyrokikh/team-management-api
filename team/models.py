from django.db import models


class Type(models.Model):
    name = models.CharField(
        max_length=63, unique=True
    )

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(
        max_length=63
    )
    type = models.ForeignKey(
        to=Type,
        related_name="teams",
        on_delete=models.SET_NULL,
        null=True
    )
    leader = models.OneToOneField(
        "user.User",
        related_name="task",
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        unique_together = ("name", "type")

    def __str__(self):
        return self.name


class Task(models.Model):
    TYPES = (
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Done", "Done"),
    )

    name = models.CharField(
        max_length=63, unique=True
    )
    description = models.TextField()
    status = models.CharField(
        max_length=63,
        choices=TYPES,
        default="Pending"
    )
    team = models.ForeignKey(
        to=Team,
        related_name="tasks",
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        unique_together = ("name", "team")

    def __str__(self):
        return self.name
