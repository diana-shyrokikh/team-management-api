from unittest import TestCase

from team.models import Type
from team.serializers import TypeSerializer


class TypeSerializerTests(TestCase):

    def test_type_serializer_missing_name(self):
        data = {}
        serializer = TypeSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_type_serializer_invalid_name(self):
        invalid_names = ["", "123name", "name-=+"]

        for name in invalid_names:
            data = {"name": name}
            serializer = TypeSerializer(data=data)

            self.assertFalse(serializer.is_valid())
            self.assertIn("name", serializer.errors)

    def test_type_serializer_duplicate_name(self):
        Type.objects.get_or_create(name="TestType")

        data = {"name": "TestType"}
        serializer = TypeSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_type_serializer_valid_create(self):
        data = {"name": "Test Type 0"}
        serializer = TypeSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        instance = serializer.save()

        self.assertEqual(instance.name, "Test Type 0")

    def test_type_serializer_update(self):
        type_obj, created = Type.objects.get_or_create(
            name="Test Type 13"
        )
        data = {"name": "Updated Type"}
        serializer = TypeSerializer(type_obj, data=data)

        self.assertTrue(serializer.is_valid())

        instance = serializer.save()

        self.assertEqual(instance.name, "Updated Type")
