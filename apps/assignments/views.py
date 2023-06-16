from django_filters import rest_framework as filters
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from apps.accounts.models import User

from .models import Assignments
from .serializers import AssignmentsSerializer
from .filters import AssignmentsFilters


class AssignmentsViewSet(viewsets.ModelViewSet):
    queryset = Assignments.objects.all()
    serializer_class = AssignmentsSerializer
    filterset_class = AssignmentsFilters
    filters_backends = (filters.DjangoFilterBackend,)
    permissions_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(user_id=user.id)

    def perform_create(self, serializer):
        user_id = serializer.validated_data.get('user_id')
        user = self.request.user

        if not user.id == user_id:
            raise PermissionDenied("You can not create assignments for other users")
        else:
            user = User.objects.get(id=user_id)
        serializer.save(user=user)
