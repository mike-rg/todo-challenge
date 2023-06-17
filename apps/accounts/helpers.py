import logging

from smtplib import SMTPException

from django.core import mail, signing
from django.db import IntegrityError, DatabaseError, transaction
from django.urls import reverse

from django.core.exceptions import ValidationError

from .constants import (
    REGISTRATION_EMAIL_CONFIRM_MODEL_FIELD,
    REGISTRATION_EMAIL_BASE_URL,
    REGUSTRATION_EMAIL_MESSAGE,
    REGISTRATION_EMAIL_SUBJECT,
    REGISTRATION_EMAIL_FROM
)
from .exceptions import EmailVerificationTokenException
from .models import EmailVerificationToken

logger = logging.getLogger(__name__)


def _get_verification_url(token):
    """Returns the verification url with a given token.

    Args:
        token: The token object to be verified.

    Returns:
        A string representing the verification url.
    """
    path = reverse('accounts:verify-email', args=(token,))
    return REGISTRATION_EMAIL_BASE_URL + path


def encode_token(token):
    """Encodes the token object into a secure format.

    Args:
        token: The token object to be encoded.

    Returns:
        A string representing the encoded token.
    """
    return signing.dumps({
        'token_id': str(token.id),
        'user_id': str(token.user.id),
        'expired_at': token.expired_at.isoformat(),
    })


def decode_token(token):
    """Decodes a token and return the data payload.

    Args:
        token: The token to be decode.

    Returns:
        dict: The data payload from the decoding process, or None if the token is invalid.

    """
    try:
        data = signing.loads(token)
    except signing.SignatureExpired:
        raise
    except signing.BadSignature:
        raise
    else:
        return data


def send_email_verification(user):
    """Send an email to verify the user's email.

    Args:
        user: The user object whose email needs to be verified.

    Raises:
        ValidationError: If the user's email is already confirmed or if there is a failure in sending the email.
        EmailVerificationTokenException: If there is an error in creating the verification token or sending the email.

    """
    if getattr(user, REGISTRATION_EMAIL_CONFIRM_MODEL_FIELD):
        logger.warning('Email already confirmed for user email:{}'.format(user.email))
        raise ValidationError('Email already confirmed for user email:{}'.format(user.email))
    try:
        instance = EmailVerificationToken.get_or_create_token(user.id)
        token = encode_token(instance)
        url = _get_verification_url(token)
        message = REGUSTRATION_EMAIL_MESSAGE.format(url=url,)
        mail.send_mail(
            REGISTRATION_EMAIL_SUBJECT,
            message,
            REGISTRATION_EMAIL_FROM,
            [user.email],
            fail_silently=False,
        )
    except SMTPException as e:  # noqa: F84
        logger.exception('Failed to send verifiction email for user id:{}'.format(user.id), extra={
            'user_id': user.id,
            'token_id': instance.id,
        })
        raise EmailVerificationTokenException("Failed to send verification email for user {}".format(user.id)) from e
    except (IntegrityError, DatabaseError) as e:  # noqa: F84
        logger.error('Cannot create verification token for user id:{}'.format(user.id), exc_info=True)
        raise EmailVerificationTokenException('Cannot create verification token for user id:{}'.format(user.id))

    except Exception as e:  # noqa: F841
        logger.error('An error occurred to send email verification for user id:{}'.format(user.id), exc_info=True)
        raise EmailVerificationTokenException('An error occurred to send email verification for user id:{}'.format(user.id))
