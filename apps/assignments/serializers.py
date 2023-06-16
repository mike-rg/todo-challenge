from rest_framework import serializers

from .models import Assignments


class AssignmentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignments
        exclude = ['user']
        read_only_fields = ('id', 'created_at', 'updated_at')


class AssignmentsRetrieveSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Assignments
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
