from unittest import TestCase

from django.contrib.auth import get_user_model

from team.models import Type, Team
from team.serializers import (
    TaskSerializer,
    TaskDetailSerializer,
)


class TaskSerializerTestCase(TestCase):
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
        self.task_data = {
            "name": "Test Task",
            "status": "Pending",
            "team": self.team.name
        }

    def test_task_serializer_valid(self):
        serializer = TaskSerializer(data=self.task_data)

        self.assertTrue(serializer.is_valid())

        task = serializer.save()

        self.assertEqual(task.name, "Test Task")
        self.assertEqual(task.status, "Pending")
        self.assertEqual(task.team, self.team)

    def test_task_serializer_invalid_name(self):
        invalid_names = ["", "123name", "name-=+"]

        for name in invalid_names:
            self.task_data["name"] = name

            serializer = TaskDetailSerializer(data=self.task_data)

            self.assertFalse(serializer.is_valid())

    def test_task_detail_serializer_valid(self):
        serializer = TaskDetailSerializer(
            instance=self.task_data, data=self.task_data
        )

        self.assertTrue(serializer.is_valid())

        updated_task = serializer.save()

        self.assertEqual(updated_task.name, "Updated Task")
        self.assertEqual(updated_task.status, "In Progress")
        self.assertEqual(updated_task.description, "Updated description")

    def test_task_detail_serializer_invalid_name(self):
        self.task_data["name"] = ""

        serializer = TaskDetailSerializer(
            instance=self.task_data, data=self.task_data
        )

        self.assertFalse(serializer.is_valid())
