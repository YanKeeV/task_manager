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

class ProjectInviteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectInvite
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = '__all__'

class UserToTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserToTeam
        fields = '__all__'

class TeamInviteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectInvite
        fields = '__all__'

class PermissionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permissions
        fields = '__all__'