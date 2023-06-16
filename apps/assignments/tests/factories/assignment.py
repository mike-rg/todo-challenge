from django.utils import timezone

from factory import Faker
from factory.django import DjangoModelFactory

from apps.assignments.models import Assignments


class BaseAssignmentFactory(DjangoModelFactory):
    title = Faker('sentence')
    description = Faker('text')

    class Meta:
        model = Assignments

    @classmethod
    def make_assignment_for_user(cls, user, due_date=None):
        if not due_date:
            due_date = timezone.now() + timezone.timedelta(days=1)  # default due date
        assignment = cls.build()
        assignment.user = user
        assignment.due_date = due_date
        assignment.save()
        return assignment


class PendingAssignmentFactory(BaseAssignmentFactory):
    status = 'pending'


class InProgressAssignmentFactory(BaseAssignmentFactory):
    status = 'in_progress'


class CancelledAssignmentFactory(BaseAssignmentFactory):
    status = 'cancelled'
