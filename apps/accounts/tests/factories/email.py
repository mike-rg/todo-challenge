from django.utils import timezone

from factory.django import DjangoModelFactory

from apps.accounts.models import EmailVerificationToken


class BaseEmailVerificationFactory(DjangoModelFactory):
    class Meta:
        model = EmailVerificationToken


class ExpiredEmailVerificationTokenFactory(BaseEmailVerificationFactory):
    expired_at = timezone.now() - timezone.timedelta(days=1)


class ValidEmailVerificationTokenFactory(BaseEmailVerificationFactory):
    expired_at = timezone.now() + timezone.timedelta(days=1)
