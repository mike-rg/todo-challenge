from rest_framework import serializers

from apps.accounts.models import User
from .models import Assignment


class AssignmentsSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.values_list('pk', flat=True))

    class Meta:
        model = Assignment
        exclude = ('user')
        read_only_fields = ('id', 'created_at', 'updated_at')
