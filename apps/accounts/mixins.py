import logging
import traceback

from django.db import DatabaseError, IntegrityError, transaction
from django.core import signing
from django.core.exceptions import MultipleObjectsReturned, ValidationError

from rest_framework import status
from rest_framework.response import Response

from .helpers import decode_token
from .models import EmailVerificationToken

logger = logging.getLogger(__name__)


class EmailVerificationMixin:
    def handle_expired_token(self):
        logger.warning('Email verification token expired.')

        return Response(
            {'message': 'Token expired.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def handle_invalid_token(self, exc_info):
        logger.error('Failed token verification.', exc_info=exc_info)

        return Response(
            {'message': 'Invalid token.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def handle_successful_verification(self):
        logger.info('Email verified successfully.')

        return Response(
            {'message': 'Email verified successfully.'},
            status=status.HTTP_200_OK,
        )

    def handle_unsuccessful_verification(self, exc_info):
        logger.error('Failed to verify email.', exc_info=exc_info)

        return Response(
            {'message': 'Cannot verified email.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def handle_invalid_token_data(self):
        logger.error('Failed token verification.')

        return Response(
            {'message': 'Invalid token.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @transaction.atomic
    def verify_email_token(self, token):
        try:
            data = decode_token(token)

            if not data:
                logger.warning('Invalid email verification token.')
                return self.handle_invalid_token_data()

            if not {'token_id', 'user_id', 'expired_at'}.issubset(data.keys()):
                logger.warning('Invalid email verification token. Missing required fields.')
                return self.handle_invalid_token_data()

            instance = EmailVerificationToken.get_token(**data)
            if not instance.is_token_expired():
                return self.handle_expired_token()

            user = instance.user
            instance.delete()
            user.email_verified = True
            user.is_active = True
            user.save(update_fields=['email_verified', 'is_active'])
            return self.handle_successful_verification()

        except (EmailVerificationToken.DoesNotExist, signing.SignatureExpired, signing.BadSignature) as e:  # noqa: F841
            return self.handle_invalid_token(exc_info=traceback.format_exc())

        except (MultipleObjectsReturned, DatabaseError, IntegrityError, ValidationError) as e:  # noqa: F841
            return self.handle_unsuccessful_verification(exc_info=traceback.format_exc())
