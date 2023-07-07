from django.test import TestCase

from apps.accounts.models import User


class UserManagerTestCase(TestCase):
    def test_create_user(self):
        email = 'foo@example.com'
        password = 'hola.chau1234'
        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        email = 'bar@example.com'
        password = 'hola.chau1234'
        superuser = User.objects.create_superuser(email=email, password=password)

        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.check_password(password))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password='hola.chau1234')
