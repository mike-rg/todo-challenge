from factory import Faker
from factory.django import DjangoModelFactory

from apps.accounts.models import User


class BaseUserFactory(DjangoModelFactory):
    email = Faker('email')
    password = Faker('password')

    class Meta:
        model = User


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
