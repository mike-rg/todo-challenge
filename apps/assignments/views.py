import logging

from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Assignments
from .filters import AssignmentsFilters
from .serializers import AssignmentsSerializer

logger = logging.getLogger(__name__)


class AssignmentsViewSet(viewsets.ModelViewSet):
    queryset = Assignments.objects.all()
    filterset_class = AssignmentsFilters
    filters_backends = (filters.DjangoFilterBackend,)
    permissions_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = AssignmentsSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(user_id=user.id)
