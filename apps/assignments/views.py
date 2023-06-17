import logging

from django_filters import rest_framework as filters
from rest_framework import viewsets, permissions

from .models import Assignments
from .serializers import AssignmentsCreateSerializer, AssignmentsRetrieveSerializer
from .filters import AssignmentsFilters

logger = logging.getLogger(__name__)


class AssignmentsViewSet(viewsets.ModelViewSet):
    queryset = Assignments.objects.all()
    filterset_class = AssignmentsFilters
    filters_backends = (filters.DjangoFilterBackend,)
    permissions_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return AssignmentsCreateSerializer
        return AssignmentsRetrieveSerializer

    serializer_class = get_serializer_class

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(user_id=user.id)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        logger.info('Creating assignment for user id:{}'.format(user.id))
