from rest_framework import serializers

from .models import *
from core.serializers import *

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'

class TaskListSerializer(serializers.ModelSerializer):
    
    user_id = serializers.CharField(source='user.pk')
    user_first_name = serializers.CharField(source='user.first_name')
    user_last_name = serializers.CharField(source='user.last_name')
    user_tag = serializers.CharField(source='user.tag')
    
    class Meta:
        model = Task
        fields = ('pk', 'name', 'user_first_name', 'user_last_name', 'description', 'start_date', 'end_date', 'priority', 'status', 'group', 'project', 'user_id', 'user_tag')

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

class TestProjectInviteSerializer(serializers.ModelSerializer):

    project = serializers.CharField(source='project.name')
    project_id = serializers.CharField(source='project.pk')
    user_sent = serializers.CharField(source='user_sent.first_name')
    user_get = serializers.CharField(source='user_get.first_name')

    class Meta:
        model = ProjectInvite
        fields = ('pk', 'project', 'project_id', 'user_sent', 'user_get')

class ArchiveSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='user.pk')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    status = serializers.CharField(source='user.status')
    tag = serializers.CharField(source='user.tag')
    role = serializers.CharField(source='user.role')
    image = serializers.ImageField(source='user.image')

    class Meta:
        model = UserToProject
        fields = ('id', 'first_name', 'last_name', 'email', 'status', 'tag', 'role', 'image')

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
        model = TeamInvite
        fields = '__all__'

class PermissionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permissions
        fields = '__all__'

class TaskCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskComment
        fields = "__all__"

class GetTaskCommentSerializer(serializers.ModelSerializer):

    user_tag = serializers.CharField(source='user.tag')

    class Meta:
        model = TaskComment
        fields = ("pk", "task", "user_tag", "created_at", "text")