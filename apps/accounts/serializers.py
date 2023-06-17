import logging

from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .constants import REGISTRATION_EMAIL_CONFIRM
from .exceptions import EmailVerificationTokenException
from .helpers import send_email_verification
from .models import User


logger = logging.getLogger(__name__)


class RegisterUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data

    def validate_password(self, value):
        validate_password(password=value)
        return value

    def validate_confirm_password(self, value):
        validate_password(password=value)
        return value

    def create(self, validated_data):
        try:
            email = validated_data.pop('email')
            password = validated_data.pop('password')

            instance = self.Meta.model(email=email)
            instance.set_password(password)
            instance.save()

            if REGISTRATION_EMAIL_CONFIRM:
                send_email_verification(instance)
                logger.info('Email verification was sent successfully for user email:{}'.format(instance.email))

            return instance

        except IntegrityError:
            logger.error('Cannot create user for email:{}'.format(email))
            raise serializers.ValidationError("Cannot create user for email:{}.".format(email))

        except ValidationError as e:  # noqa: F841
            logger.error('An error occurred during user creation for email:{}'.format(email), exc_info=True)
            raise serializers.ValidationError(str(e))

        except EmailVerificationTokenException as e:  # noqa: F841
            raise serializers.ValidationError(str(e))


class UserEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email']
