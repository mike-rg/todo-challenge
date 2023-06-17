import logging

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django_filters import rest_framework as filters
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .exceptions import AssignmentApiExceptionHandler
from .models import Assignments
from .filters import AssignmentsFilters
from .serializers import (
    AssignmentsCreateSerializer,
    AssignmentsRetrieveSerializer,
    AssignmentsUpdateSerializer
)

logger = logging.getLogger(__name__)


class AssignmentsViewSet(viewsets.ModelViewSet):
    queryset = Assignments.objects.all()
    filterset_class = AssignmentsFilters
    filters_backends = (filters.DjangoFilterBackend,)
    permissions_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'put', 'delete']

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def handle_exception(self, exc):
        if isinstance(exc, tuple([PermissionDenied, Http404, APIException])):
            response = AssignmentApiExceptionHandler().format_response(exc)
            return response
        handler_ex = super().handle_exception(exc)

        return handler_ex

    def get_serializer_class(self):
        if self.action == 'create':
            return AssignmentsCreateSerializer
        elif self.action == 'update':
            return AssignmentsUpdateSerializer
        return AssignmentsRetrieveSerializer

    serializer_class = get_serializer_class

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(user_id=user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        data = {
            'status': status.HTTP_200_OK,
            'data': {
                'message': 'Success',
                'results': serializer.data
            }
        }
        return self.get_paginated_response(data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = {
            'status': status.HTTP_201_CREATED,
            'data': {
                'message': 'Created successfully',
                'results': serializer.data
            }
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {
            'status': status.HTTP_200_OK,
            'data': {
                'message': 'Success',
                'results': serializer.data
            }
        }
        return Response(data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = {
            'status': status.HTTP_200_OK,
            'data': {
                'message': 'Updated successfully',
                'results': serializer.data
            }
        }
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {
            'status': status.HTTP_204_NO_CONTENT,
            'data': {
                'message': 'Deleted successfully'
            }
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
