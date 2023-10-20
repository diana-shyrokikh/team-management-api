from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from user.serializers import UserSerializer


class UserSerializerTests(TestCase):
    def test_valid_user_creation(self):
        data = {
            "email": "test@example.com",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "password": "securepassword"
        }
        serializer = UserSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        user = serializer.save()

        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "TestFirst")
        self.assertEqual(user.last_name, "TestLast")
        self.assertTrue(user.check_password("securepassword"))

    def test_missing_email_validation(self):
        data = {
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "password": "securepassword"
        }
        serializer = UserSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_email_validation(self):
        data = {
            "email": "invalid-email",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "password": "securepassword"
        }
        serializer = UserSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_first_last_name_validation(self):
        invalid_names = ["123name", "name-=+"]

        for name in invalid_names:
            data = {
                "email": "test@example.com",
                "first_name": name,
                "last_name": "TestLast",
                "password": "securepassword"
            }
            serializer = UserSerializer(data=data)

            self.assertFalse(serializer.is_valid())
            self.assertIn("first_name", serializer.errors)

        for name in invalid_names:
            data = {
                "email": "test@example.com",
                "first_name": "TestFirst",
                "last_name": name,
                "password": "securepassword"
            }
            serializer = UserSerializer(data=data)

            self.assertFalse(serializer.is_valid())
            self.assertIn("last_name", serializer.errors)

    def test_create_and_update_user(self):
        user = get_user_model().objects.create_user(
            email="existing@example.com",
            password="existingpassword"
        )
        data = {
            "email": "new@example.com",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "password": "newpassword"
        }
        serializer = UserSerializer(instance=user, data=data)

        self.assertTrue(serializer.is_valid())

        updated_user = serializer.save()

        self.assertEqual(updated_user.email, "new@example.com")
        self.assertEqual(updated_user.first_name, "TestFirstName")
        self.assertEqual(updated_user.last_name, "TestLastName")
        self.assertTrue(updated_user.check_password("newpassword"))

    def test_password_change(self):
        user = get_user_model().objects.create_user(
            email="change@example.com",
            password="oldpassword"
        )
        data = {
            "password": "newpassword"
        }
        serializer = UserSerializer(
            instance=user, data=data, partial=True
        )

        self.assertTrue(serializer.is_valid())

        updated_user = serializer.save()

        self.assertTrue(updated_user.check_password("newpassword"))
