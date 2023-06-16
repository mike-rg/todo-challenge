import logging

from django.db import IntegrityError, transaction
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .constants import REGISTRATION_EMAIL_CONFIRM
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

    @transaction.atomic
    def create(self, validated_data):
        try:
            email = validated_data.pop('email')
            password = validated_data.pop('password')

            instance = self.Meta.model(email=email)
            instance.set_password(password)
            instance.save()

            if REGISTRATION_EMAIL_CONFIRM:
                send_email_verification(instance)

            return instance

        except IntegrityError:
            raise serializers.ValidationError("Email address already exists.")

        except ValidationError as e:
            logger.error('An error occurred during user creation. Validated data: %s', validated_data, exc_info=True)
            raise serializers.ValidationError(str(e))

        except Exception as e:  # noqa: F841
            logger.error('An error occurred during user creation.', exc_info=True)
            raise serializers.ValidationError("An error occurred during user creation.")


class UserEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email']
