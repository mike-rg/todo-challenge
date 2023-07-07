from unittest import mock

from django.test import TestCase

from apps.accounts.exceptions import EmailVerificationTokenException
from apps.accounts.tasks import send_email_verification_task
from apps.accounts.tests.factories.user import UserFactory


class SendEmailVerificationTaskTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_send_email_verification_task_success(self):
        send_email_verification_task(self.user.id)
        self.assertTrue(self.user.email_verify_tokens.exists())

    def test_fail_send_email_verification_fail(self):
        with mock.patch('django.core.mail.send_mail') as mocked_send_mail:
            mocked_send_mail.side_effect = EmailVerificationTokenException()
            send_email_verification_task(self.user.id)
        self.assertTrue(self.user.email_verify_tokens.exists())
