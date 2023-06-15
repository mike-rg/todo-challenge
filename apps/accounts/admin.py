from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.helpers import send_email_verification

from .models import User


def resend_email_verification(modeladmin, request, queryset):
    for user in queryset.filter(email_verified=False, is_active=False):
        send_email_verification(user)


resend_email_verification.short_description = "Resend confirmation email"


class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active', 'email_verified']
    actions = [resend_email_verification]


admin.site.register(User, UserAdmin)
