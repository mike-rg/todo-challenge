from django.contrib.auth.password_validation import validate_password
from django.db import transaction

from rest_framework import serializers

from .constants import REGISTRATION_EMAIL_CONFIRM
from .helpers import send_email_verification
from .models import User


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
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        instance = self.Meta.model(email=email)
        instance.set_password(password)
        instance.save()

        if REGISTRATION_EMAIL_CONFIRM:
            send_email_verification(instance)

        return instance


class UserEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email']
