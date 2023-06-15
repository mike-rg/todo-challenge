from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny

from .mixins import EmailVerificationMixin
from .serializers import UserEmailSerializer, RegisterUserSerializer


class RegisterUserAPIView(CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)


class UserEmailVerificationAPIView(GenericAPIView, EmailVerificationMixin):
    serializer_class = UserEmailSerializer
    permission_classes = (AllowAny,)

    def get(self, request, token):
        return self.verify_email_token(token)
