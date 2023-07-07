from rest_framework import serializers

from .models import Assignments


class AssignmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignments
        exclude = ['user']
        read_only_fields = ('id', 'created_at', 'updated_at')
