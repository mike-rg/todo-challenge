import logging

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .exceptions import EmailVerificationTokenException
from .helpers import send_email_verification
from .models import User, EmailVerificationToken

logger = logging.getLogger(__name__)


def resend_email_verification(modeladmin, request, queryset):
    for user in queryset.filter(email_verified=False):
        try:
            send_email_verification(user)
        except EmailVerificationTokenException:
            logger.error('An error occurred to resend email verification', exc_info=True)


resend_email_verification.short_description = "Resend confirmation email"


class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active', 'email_verified']
    actions = [resend_email_verification]


admin.site.register(User, UserAdmin)


class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'expired_at', 'user', 'created_at', 'updated_at']


admin.site.register(EmailVerificationToken, EmailVerificationTokenAdmin)
