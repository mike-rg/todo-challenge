from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from apps.accounts.models import User


class BaseUserFactory(DjangoModelFactory):
    email = Faker('email')

    class Meta:
        model = User
        django_get_or_create = ["email"]

    @post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password("hola.chau1234")


class UserFactory(BaseUserFactory):
    is_staff = False
    is_superuser = False
    is_active = False
    email_verified = False


class UserStaffFactory(BaseUserFactory):
    is_staff = True
    is_superuser = False


class SuperUserFactory(BaseUserFactory):
    is_staff = True
    is_superuser = True


class VerifiedUserFactory(BaseUserFactory):
    is_staff = False
    is_active = True
    email_verified = True
