import logging

from celery import shared_task

from .exceptions import EmailVerificationTokenException
from .helpers import send_email_verification
from .models import User

logger = logging.getLogger(__name__)


@shared_task
def send_email_verification_task(user_id):
    """ TODO: Pass user id instead of user object to the send_email_verification method."""
    user = User.objects.get(id=user_id)
    try:
        send_email_verification(user)
    except EmailVerificationTokenException:
        logger.error('An error occurred to resend email verification for user id:{}'.format(user_id))
