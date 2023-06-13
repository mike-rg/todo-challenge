from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.base.models import BaseModel


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)
