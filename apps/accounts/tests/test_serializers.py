from unittest.mock import patch

from django.db import IntegrityError
from django.test import TestCase

from rest_framework import serializers

from apps.accounts.serializers import RegisterUserSerializer
from apps.accounts.tests.factories.user import UserFactory


class RegisterUserSerializerTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        email = 'foo@example.com'
        cls.user = UserFactory(email=email)

    @patch('apps.accounts.models.User')
    def test_register_user_integrity_error(self, mock_user):
        mock_user.objects.create_user.side_effect = IntegrityError
        data = {
            'email': 'foo@example.com',
            'password': 'Hola.Chau123',
            'confirm_password': 'Hola.Chau123',
        }
        validated_data = {
            'email': 'foo@example.com',
            'password': 'Hola.Chau123',
        }
        serializer = RegisterUserSerializer(data=data)
        with self.assertRaises(serializers.ValidationError):
            serializer.create(validated_data)

    @patch('apps.accounts.models.User')
    def test_register_user_get_validated_data_fail(self, mock_user):
        mock_user.objects.create_user.side_effect = IntegrityError
        data = {
            'email': 'foo@example.com',
            'password': 'Hola.Chau123',
            'confirm_password': 'Hola.Chau123',
        }
        validated_data = {
            'email': 'foo@example.com',
        }
        serializer = RegisterUserSerializer(data=data)
        with self.assertRaises(Exception):
            serializer.create(validated_data)
