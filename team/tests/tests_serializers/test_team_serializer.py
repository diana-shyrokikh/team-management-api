from unittest import TestCase

from django.contrib.auth import get_user_model

from team.models import (
    Team,
    Type,
    Task,
)
from team.serializers import TeamCreateUpdateSerializer


class TeamSerializerTest(TestCase):
    def setUp(self):
        self.leader, created = get_user_model(
        ).objects.get_or_create(
            email="leader@example.com",
            first_name="leader test name",
            last_name="leader last name",
            password="leader123456"
        )
        self.type, created = Type.objects.get_or_create(
            name="Test Type"
        )
        self.members = [
            get_user_model().objects.get_or_create(
                email=f"test_member{letter}@example.com",
                first_name=f"test {letter} name",
                last_name=f"last {letter} name",
                password="leader123456"
            )
            for letter in "abcd"
        ]
        self.tasks = [
            Task.objects.get_or_create(
                name=f"Test Task {number}",
                description="This is a test task",
            )
            for number in range(5)
        ]

    def test_team_serializer_invalid_name(self):
        invalid_names = ["", "123name", "name-=+"]

        for name in invalid_names:
            data = {
                "name": name,
                "type": self.type.name,
                "leader": None,
                "tasks": [],
                "members": []
            }
            serializer = TeamCreateUpdateSerializer(data=data)

            self.assertFalse(serializer.is_valid())
            self.assertIn("name", serializer.errors)

    def test_team_serializer_valid_create(self):
        data = {
            "name": "Test Team 3",
            "type": self.type.name,
            "leader": self.leader.email,
            "members": [
                member[0].email for member in self.members
            ],
            "tasks": []
        }
        serializer = TeamCreateUpdateSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        instance = serializer.save()

        self.leader.refresh_from_db()

        self.assertEqual(instance.name, "Test Team 3")
        self.assertEqual(instance.type, self.type)
        self.assertEqual(instance.leader, self.leader)
        self.assertEqual(self.leader.is_leader, True)
        self.assertEqual(self.leader.team, instance)

        for member in self.members:
            member[0].refresh_from_db()
            self.assertEqual(member[0].team, instance)

    def test_team_serializer_update(self):
        team, created = Team.objects.get_or_create(
            name="Test Team",
            type=self.type,
        )
        new_leader, created = get_user_model(
        ).objects.get_or_create(
            email="new_leader@example.com",
            first_name="new leader test name",
            last_name="new leader last name",
            password="leader123456"
        )
        data = {
            "name": "Updated Team 2",
            "type": self.type.name,
            "leader": new_leader.email,
            "members": [],
            "tasks": [
                task[0].name for task in self.tasks
            ]
        }
        serializer = TeamCreateUpdateSerializer(team, data=data)

        self.assertTrue(serializer.is_valid())

        instance = serializer.save()

        new_leader.refresh_from_db()

        self.assertEqual(instance.name, "Updated Team 2")
        self.assertEqual(self.leader.is_leader, False)
        self.assertEqual(self.leader.team, None)
        self.assertEqual(new_leader.is_leader, True)
        self.assertEqual(new_leader.team, instance)
        self.assertEqual(instance.members.count(), 1)

        for task in self.tasks:
            task[0].refresh_from_db()
            self.assertEqual(task[0].team, instance)
