from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .decorators import handler_celery_exceptions
from .models import User, EmailVerificationToken
from .tasks import send_email_verification_task


@handler_celery_exceptions
def resend_email_verification(modeladmin, request, queryset):
    if settings.REGISTRATION_EMAIL_CONFIRM_ENABLED:
        for user in queryset.filter(email_verified=False):
            send_email_verification_task.delay(user_id=user.id)
    else:
        messages.warning(request, "Email verification is disabled")


resend_email_verification.short_description = "Resend confirmation email"


class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active', 'email_verified']
    actions = [resend_email_verification]


admin.site.register(User, UserAdmin)


class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'expired_at', 'user', 'created_at', 'updated_at']


admin.site.register(EmailVerificationToken, EmailVerificationTokenAdmin)
