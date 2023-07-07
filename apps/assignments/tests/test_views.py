import json

from datetime import timedelta
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.tests.factories.user import (
    SuperUserFactory,
    UserFactory,
    VerifiedUserFactory,
)
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
        self.assertEqual(len(response.data["results"]), 1)

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
        self.assertEqual(response.data['title'], 'Assignment')
        self.assertEqual(response.data['description'], 'Assignment Description')
        self.assertEqual(response.data['due_date'], '2021-01-01T00:00:00Z')

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
        self.assertEqual(response.data['title'], 'Assignment')
        self.assertEqual(response.data['description'], 'Assignment Description')

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
        self.assertEqual(response.data['title'], 'Update Assignment')
        self.assertEqual(response.data['description'], 'Update Assignment Description')
        self.assertEqual(response.data['status'], AssignmentStatus.COMPLETED)
        self.assertEqual(response.data['due_date'], '2021-01-01T00:00:00Z')

    def test_delete_assignment(self):
        assignment = CancelledAssignmentFactory.make_assignment_for_user(user=self.user)
        url = reverse('assignments:assignments-detail', args=[assignment.id])
        response = self.client.delete(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Assignments.objects.filter(id=assignment.id).exists())

    def test_delete_assignment_not_found(self):
        url = reverse('assignments:assignments-detail', args=[100])
        response = self.client.delete(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(str(response.data['detail']), 'Not found.')
        self.assertEqual(response.data['detail'].code, 'not_found')


class AssignmentsSuperUserViewSetTestCase(TestCase):

    @classmethod
    @mock.patch('rest_framework_simplejwt.tokens.AccessToken.lifetime', timedelta(minutes=30))
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = SuperUserFactory(email='foo@example.com')
        response = cls.client.post(reverse('token_obtain_pair'), {
            'email': 'foo@example.com',
            'password': 'hola.chau1234'})
        cls.access_token = response.data['access']
        cls.refresh_token = response.data['refresh']
        cls.headers = {
            'Authorization': f'Bearer {cls.access_token}',
        }
        # create an pending assignment for another user
        PendingAssignmentFactory.make_assignment_for_user(user=UserFactory())

    def test_list_assignments(self):
        url = reverse('assignments:assignments-list')
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
