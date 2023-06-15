import unittest

from django.core import signing
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.helpers import encode_token

from .factories.user import UserFactory
from .factories.email import ExpiredEmailVerificationFactory, ValidEmailVerificationFactory


class RegisterUserTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        email = 'foo@example.com'
        cls.user = UserFactory(email=email)

    def setUp(self):
        self.url = reverse('accounts:register')

    @unittest.skip('Not implemented yet')
    def test_register_user_invalid_email(self):
        pass
    
    def test_register_user_already_exists_email(self):
        data = {
            'email': 'foo@example.com',
            'password': 'Hola.Chau123',
            'confirm_password': 'Hola.Chau123',
        }
        response = self.client.post(self.url, data=data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('User with this email already exists.', response_data['email'])

    def test_register_user_short_passwords(self):
        data = {
            'email': 'bar@example.com',
            'password': 'Hola',
            'confirm_password': 'Hola',
        }
        response = self.client.post(self.url, data=data)
        response_data = response.json()
        password_errors = response_data.get('password', [])
        confirm_password_errors = response_data.get('confirm_password', [])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This password is too short. It must contain at least 8 characters.', password_errors)
        self.assertIn('This password is too common.', password_errors)
        self.assertIn('This password is too short. It must contain at least 8 characters.', confirm_password_errors)
        self.assertIn('This password is too common.', confirm_password_errors)

    def test_register_user_different_passwords(self):
        data = {
            'email': 'bar@example.com',
            'password': 'Hola.Chau123',
            'confirm_password': 'Hola.Chau321',
        }
        response = self.client.post(self.url, data=data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The two password fields didn't match.", response_data['non_field_errors'])

    def test_register_valid_user(self):
        data = {
            'email': 'bar@example.com',
            'password': 'Hola.Chau123',
            'confirm_password': 'Hola.Chau123',
        }
        response = self.client.post(self.url, data=data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data.get('email'), 'bar@example.com')


class EmailVerificationTestCase(APITestCase):

    def setUp(self):
        self.user_1 = UserFactory(email='valid@example.com')
        self.user_2 = UserFactory(email='expired@example.com')
        self.user_3 = UserFactory(email='invalid@example.com')
        self.valid_token = ValidEmailVerificationFactory(user=self.user_1)
        self.expired_token = ExpiredEmailVerificationFactory(user=self.user_2)

    def test_no_token(self):
        token = '?'
        url = reverse('accounts:verify-email', kwargs={'token': f'{token}'})
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid token.', response_data.get('message'))

    def test_expired_token(self):
        token = encode_token(self.expired_token)
        url = reverse('accounts:verify-email', kwargs={'token': f'{token}'})
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Token expired.', response_data.get('message'))

    def test_token_already_verified(self):
        token = encode_token(self.valid_token)
        url = reverse('accounts:verify-email', kwargs={'token': f'{token}'})
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Email verified successfully.', response_data['message'])
        self.user_1.refresh_from_db()
        self.assertTrue(self.user_1.email_verified)
        self.assertTrue(self.user_1.is_active)
        self.assertFalse(self.user_1.email_verify_tokens.exists())
        
        url = reverse('accounts:verify-email', kwargs={'token': f'{token}'})
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid token.', response_data.get('message'))

    def test_invalid_token(self):
        token_data = {
            'token_id': '',
            'user_id': '',
        }
        token = signing.dumps(token_data)
        url = reverse('accounts:verify-email', kwargs={'token': f'{token}'})
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid token.', response_data.get('message'))
        self.user_3.refresh_from_db()
        self.assertFalse(self.user_3.email_verified)
        self.assertFalse(self.user_3.is_active)
        self.assertFalse(self.user_3.email_verify_tokens.exists())

    def test_valid_token(self):
        token = encode_token(self.valid_token)
        url = reverse('accounts:verify-email', kwargs={'token': f'{token}'})
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Email verified successfully.', response_data['message'])
        self.user_1.refresh_from_db()
        self.assertTrue(self.user_1.email_verified)
        self.assertTrue(self.user_1.is_active)
        self.assertFalse(self.user_1.email_verify_tokens.exists())
