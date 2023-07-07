from django.test import TestCase

from apps.accounts.utils import get_expiration_date
from apps.accounts.tests.factories.user import (
    VerifiedUserFactory,
)
from apps.accounts.tests.factories.email import (
    ValidEmailVerificationTokenFactory,
)


class EmailVerificationTokenModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.expired_at = get_expiration_date()
        cls.user = VerifiedUserFactory(email="foo@example.com")
        cls.token = ValidEmailVerificationTokenFactory(user=cls.user, expired_at=cls.expired_at)

    def test_token_models(self):
        self.assertEqual(str(self.token), f"{self.user} - {self.expired_at}")
        self.assertEqual(self.token.user, self.user)
        self.assertEqual(self.token.expired_at, self.expired_at)
