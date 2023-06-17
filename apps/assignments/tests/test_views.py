import json

from datetime import timedelta
from unittest import mock

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

    def test_list_assignments(self):
        PendingAssignmentFactory.make_assignment_for_user(user=self.user)
        url = reverse('assignments:assignments-list')
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']['data']['results']), 1)

    def test_create_assignment(self):
        url = reverse('assignments:assignments-list')
        data = {
            'title': 'Assignment',
            'description': 'Assignment Description',
            'due_date': '2021-01-01'
        }
        response = self.client.post(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assignments.objects.count(), 1)
        self.assertEqual(response.data['data']['message'], 'Created successfully')
        self.assertEqual(response.data['data']['results']['title'], 'Assignment')
        self.assertEqual(response.data['data']['results']['description'], 'Assignment Description')
        self.assertEqual(response.data['data']['results']['due_date'], '2021-01-01T00:00:00Z')

    def test_retrieve_assignment(self):
        assignment = PendingAssignmentFactory.make_assignment_for_user(
            user=self.user,
            title='Assignment',
            description='Assignment Description',
        )
        url = reverse('assignments:assignments-detail', args=[assignment.id])
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Assignments.objects.count(), 1)
        self.assertEqual(response.data['data']['message'], 'Success')
        self.assertEqual(response.data['data']['results']['title'], 'Assignment')
        self.assertEqual(response.data['data']['results']['description'], 'Assignment Description')

    def test_update_assignment(self):
        assignment = InProgressAssignmentFactory.make_assignment_for_user(user=self.user)
        url = reverse('assignments:assignments-detail', args=[assignment.id])
        data = {
            'title': 'Update Assignment',
            'description': 'Update Assignment Description',
            'due_date': '2021-01-01',
            'status': AssignmentStatus.COMPLETED
        }
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        response = self.client.put(url, json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['message'], 'Updated successfully')
        self.assertEqual(response.data['data']['results']['title'], 'Update Assignment')
        self.assertEqual(response.data['data']['results']['description'], 'Update Assignment Description')
        self.assertEqual(response.data['data']['results']['status'], AssignmentStatus.COMPLETED)
        self.assertEqual(response.data['data']['results']['due_date'], '2021-01-01T00:00:00Z')

    def test_delete_assignment(self):
        assignment = CancelledAssignmentFactory.make_assignment_for_user(user=self.user)
        url = reverse('assignments:assignments-detail', args=[assignment.id])
        response = self.client.delete(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Assignments.objects.filter(id=assignment.id).exists())
        self.assertEqual(response.data['data']['message'], 'Deleted successfully')
