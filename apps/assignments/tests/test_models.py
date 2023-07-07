from django.test import TestCase
from django.utils import timezone

from apps.assignments.constants import AssignmentStatus

from apps.accounts.tests.factories.user import (
    VerifiedUserFactory,
)
from apps.assignments.tests.factories.assignment import (
    PendingAssignmentFactory,
)


class AssignmentsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.due_date = timezone.now()
        cls.user = VerifiedUserFactory()
        cls.assignment = PendingAssignmentFactory.make_assignment_for_user(
            user=cls.user,
            title='Assignment',
            description='Assignment Description',
            due_date=cls.due_date,
        )

    def test_assigment_models(self):
        self.assertEqual(str(self.assignment), f"{self.user} - Assignment")
        self.assertEqual(self.assignment.title, 'Assignment')
        self.assertEqual(self.assignment.description, 'Assignment Description')
        self.assertEqual(self.assignment.due_date, self.due_date)
        self.assertEqual(self.assignment.status, AssignmentStatus.PENDING)
        self.assertEqual(self.assignment.user, self.user)
