from rest_framework import serializers

from .models import *
from core.serializers import *

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'

class UserToProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserToProject
        fields = '__all__'

