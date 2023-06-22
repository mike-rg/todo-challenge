from unittest import mock

from django.conf import settings
from django.core import mail
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.accounts.constants import (
    REGUSTRATION_EMAIL_MESSAGE,
    REGISTRATION_EMAIL_SUBJECT,
)
from apps.accounts.helpers import encode_token, decode_token, send_email_verification
from apps.accounts.exceptions import EmailVerificationTokenException

from .factories.user import UserFactory
from .factories.email import ValidEmailVerificationFactory


class HelpersEmailVerificationTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(email='foo@example.com')
        self.token = ValidEmailVerificationFactory(user=self.user)
        self.verified_user = UserFactory(email='bar@example.com', email_verified=True)
        self.no_verified_user = UserFactory(email='foobar@example.com')

    def test_encode_token(self):
        encoded_token = encode_token(self.token)
        self.assertIsNotNone(encoded_token)

    def test_decode_valid_token(self):
        encoded_token = encode_token(self.token)
        decoded_token = decode_token(encoded_token)

        self.assertIsNotNone(decoded_token)
        self.assertEqual(decoded_token.get('token_id'), str(self.token.id))
        self.assertEqual(decoded_token.get('user_id'), str(self.token.user.id))
        self.assertEqual(
            decoded_token.get('expired_at'), self.token.expired_at.isoformat()
        )

    def test_already_verified_token(self):
        with self.assertRaises(ValidationError):
            send_email_verification(self.verified_user)

    def test_fail_send_email_verification(self):
        with mock.patch('django.core.mail.send_mail') as mocked_send_mail:
            mocked_send_mail.side_effect = EmailVerificationTokenException(
                'Failed to send confirmation email'
            )
            with self.assertRaises(EmailVerificationTokenException):
                send_email_verification(self.no_verified_user)
        self.assertTrue(self.no_verified_user.email_verify_tokens.exists())

    def test_send_email_verification(self):
        with mock.patch(
            'apps.accounts.helpers._get_verification_url',
            return_value='http://example.com/TOKEN',
        ):
            send_email_verification(self.user)

        email = mail.outbox[0]
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(email.subject, REGISTRATION_EMAIL_SUBJECT)
        self.assertEqual(email.from_email, settings.REGISTRATION_EMAIL_FROM)
        self.assertEqual(email.to, ['foo@example.com'])
        self.assertEqual(
            email.body,
            REGUSTRATION_EMAIL_MESSAGE.format(url='http://example.com/TOKEN'),
        )
