from django_filters import rest_framework as filters

from .models import Assignment


class AssinmentsFilters(filters.FilterSet):

    class Meta:
        model = Assignment
        fields = {
            'user_id': ['exact'],
            'created_at': ['exact', 'lte', 'gte'],
            'updated_at': ['exact', 'lte', 'gte'],
            'title': ['icontains'],
            'description': ['icontains'],
            'due_date': ['exact', 'lte', 'gte'],
            'status': ['exact'],
        }
