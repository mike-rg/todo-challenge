from rest_framework import serializers

from .models import Assignments


class AssignmentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignments
        exclude = ['user']
        read_only_fields = ('id', 'created_at', 'updated_at')


class AssignmentsRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignments
        exclude = ['user']
        read_only_fields = ('id', 'created_at', 'updated_at')


class AssignmentsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignments
        exclude = ['user']
        read_only_fields = ('id', 'created_at', 'updated_at')
