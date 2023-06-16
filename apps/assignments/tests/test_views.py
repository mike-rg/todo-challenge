from datetime import timedelta
from unittest import mock, skip

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.tests.factories.user import UserStaffFactory, VerifiedUserFactory
from apps.assignments.constants import AssignmentStatus
from apps.assignments.models import Assignments
from apps.assignments.tests.factories.assignment import (
    PendingAssignmentFactory,
    InProgressAssignmentFactory,
    CancelledAssignmentFactory,
)


class AssignmentsViewSetTestCase(TestCase):

    @classmethod
    @mock.patch('rest_framework_simplejwt.tokens.AccessToken.lifetime', timedelta(minutes=30))
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = VerifiedUserFactory(email='foo@example.com')
        response = cls.client.post(reverse('token_obtain_pair'), {'email': 'foo@example.com', 'password': 'hola.chau1234'})
        cls.access_token = response.data['access']
        cls.refresh_token = response.data['refresh']
        cls.headers = {
            'Authorization': f'Bearer {cls.access_token}',
        }
        cls.user_staff = UserStaffFactory(email='bar@example.com')
        response = cls.client.post(reverse('token_obtain_pair'), {'email': 'bar@example.com', 'password': 'hola.chau1234'})
        cls.staff_access_token = response.data['access']
        cls.staff_refresh_token = response.data['refresh']
        cls.staff_headers = {
            'Authorization': f'Bearer {cls.staff_access_token}',
        }

    @mock.patch('rest_framework_simplejwt.tokens.AccessToken.lifetime', timedelta(minutes=30))
    def test_staff_list_assignments(self):
        self.client.logout()
        assignment = PendingAssignmentFactory.make_assignment_for_user(user=self.user)
        url = reverse('assignments:assignments-list')
        response = self.client.get(url, headers=self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user_id'], assignment.user_id)
        self.assertEqual(response.data[0]['title'], assignment.title)
        self.assertEqual(response.data[0]['description'], assignment.description)

    def test_list_assignments(self):
        assignment = PendingAssignmentFactory.make_assignment_for_user(user=self.user)
        url = reverse('assignments:assignments-list')
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user_id'], assignment.user_id)
        self.assertEqual(response.data[0]['title'], assignment.title)
        self.assertEqual(response.data[0]['description'], assignment.description)

    def test_create_assignment(self):
        url = reverse('assignments:assignments-list')
        data = {
            'user_id': self.user.id,
            'title': 'New Assignment',
            'description': 'New Assignment Description',
            'due_date': '2021-01-01'
        }
        response = self.client.post(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assignments.objects.count(), 1)
        self.assertEqual(Assignments.objects.first().title, 'New Assignment')
        self.assertEqual(Assignments.objects.first().description, 'New Assignment Description')

    def test_cannot_create_assignment_for_other_user(self):
        url = reverse('assignments:assignments-list')
        data = {
            'user_id': self.user_staff.id,
            'title': 'New Assignment',
            'description': 'New Assignment Description',
            'due_date': '2021-01-01'
        }
        response = self.client.post(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Assignments.objects.count(), 0)

    def test_retrieve_assignment(self):
        assignment = PendingAssignmentFactory.make_assignment_for_user(user=self.user)
        url = reverse('assignments:assignments-detail', args=[assignment.id])
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_id'], assignment.user_id)
        self.assertEqual(Assignments.objects.count(), 1)

    @skip('Not implemented yet')
    def test_update_assignment(self):
        assignment = InProgressAssignmentFactory.make_assignment_for_user(user=self.user)
        url = reverse('assignments:assignments-detail', args=[assignment.id])
        data = {
            'user_id': self.user_staff.id,
            'title': 'New Assignment',
            'description': 'New Assignment Description',
            'due_date': '2021-01-01',
            'status': AssignmentStatus.COMPLETED
        }
        response = self.client.put(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_assignment(self):
        assignment = CancelledAssignmentFactory.make_assignment_for_user(user=self.user)
        url = reverse('assignments:assignments-detail', args=[assignment.id])
        response = self.client.delete(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Assignments.objects.filter(id=assignment.id).exists())
