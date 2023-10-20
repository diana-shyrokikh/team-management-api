from django.contrib.auth import get_user_model
from django.test import TestCase

from team.models import (
    Type,
    Team,
    Task,
)


class ModelTests(TestCase):
    def setUp(self):
        self.type, created = Type.objects.get_or_create(
            name="Test Type"
        )

        self.leader, created = get_user_model(
        ).objects.get_or_create(
            email="leader@example.com",
            first_name="leader test name",
            last_name="leader last name",
            password="leader123456"
        )

        self.team, created = Team.objects.get_or_create(
            name="Test Team",
            type=self.type,
            leader=self.leader
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

    def test_type_str_method(self):
        self.assertEqual(str(self.type), "Test Type")

    def test_task_str_method(self):
        self.assertEqual(str(self.tasks[0][0]), "Test Task 0")

    def test_team_str_method(self):
        self.assertEqual(str(self.team), "Test Team")

    def test_team_leader(self):
        self.assertEqual(self.team.leader, self.leader)

    def test_members(self):
        self.team.members.set([
            member[0] for member in self.members
        ])

        for member in self.members:
            self.assertEqual(member[0].team, self.team)

    def test_task_team(self):
        self.team.tasks.set([
            task[0] for task in self.tasks
        ])

        for task in self.tasks:
            self.assertEqual(task[0].team, self.team)
