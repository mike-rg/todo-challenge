from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from apps.base.models import BaseModel

from .manager import UserManager


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True, null=False, blank=False)
    is_active = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)


class EmailVerificationToken(BaseModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='email_verify_tokens')
    expired_at = models.DateTimeField()

    def __str__(self):
        return f'{self.user} - {self.expired_at}'

    @classmethod
    def _get_expired_at(cls):
        return timezone.now() + timezone.timedelta(days=1)

    @classmethod
    def get_token(cls, token_id, user_id, **kwargs):
        return cls.objects.select_related('user').get(id=token_id, user_id=user_id)

    @classmethod
    def create_token(cls, user_id, **kwargs):
        return cls.objects.create(user_id=user_id, expired_at=cls._get_expired_at())

    def is_token_expired(self):
        return self.expired_at > timezone.now()
