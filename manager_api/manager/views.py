import time
from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.serializers import serialize
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from django.contrib.auth import update_session_auth_hash

from .models import *
from .serializers import *

@api_view(['GET'])
def task_list_by_user(request):

    data = []
    items = Task.objects.filter(user = request.user).order_by('end_date')
    data = items
    serializer = TaskSerializer(data, context={'request': request}, many = True)
    return Response({'data': serializer.data})

@api_view(['GET'])
def get_user_permissions(request, user, project):

    data = []
    items = Permissions.objects.filter(user = user, project = project)
    data = items
    serializer = TaskSerializer(data, context={'request': request}, many = True)
    return Response({'data': serializer.data})

@api_view(['GET'])
def task_list_by_project(request, project):

    data = []
    items = Task.objects.filter(project = project)
    data = items
    serializer = TaskSerializer(data, context={'request': request}, many = True)
    return Response({'data': serializer.data})

@api_view(['GET'])
def task_list_by_team(request, team):

    users = UserToTeam.object.filter(team = team)

    id_list = []

    for i in range(len(users)):
        id_list.append(users[i].user.email)
    teamTasks = Task.objects.filter(user__in = id_list)

    data = []
    data = teamTasks
    serializer = TaskSerializer(data, context={'request': request}, many = True)
    return Response({'data': serializer.data})

@api_view(['GET'])
def users_by_project(request, project):

    try:
        items = UserToProject.objects.filter(project = project)
    except ValueError: 
        return Response(exception=ValueError, status=status.HTTP_400_BAD_REQUEST)

    users =[]
    for item in items:
        users.append({
            'id': item.user.pk,
            'first_name': item.user.first_name,
            'last_name': item.user.last_name,
            'email': item.user.email,
            'status': item.user.status,
            'tag': item.user.tag,
            'role': item.user.role,
        })

    return Response(users, status=status.HTTP_200_OK)

@api_view(['GET'])
def users_by_team(request, team):

    try:
        items = UserToTeam.objects.filter(team = team)
    except ValueError: 
        return Response(exception=ValueError, status=status.HTTP_400_BAD_REQUEST)

    users =[]
    for item in items:
        users.append({
            'id': item.user.pk,
            'first_name': item.user.first_name,
            'last_name': item.user.last_name,
            'email': item.user.email,
            'status': item.user.status,
            'tag': item.user.tag,
            'role': item.user.role,
        })

    return Response(users, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_project(request, project):

    data = []
    project = Project.objects.filter(name = project, is_finished = False)
    data = project
    serializer = ProjectSerializer(data, context={'request': request}, many = True)
    return Response({'data': serializer.data})

@api_view(['GET'])
def project_list_by_user(request, status):
    
    if(status == "archived"):
        is_finished = True
    else:
        is_finished = False

    data = []
    id_list = []
    items = UserToProject.objects.filter(user = request.user)
    for i in range(len(items)):
        id_list.append(items[i].project.pk)
    projects = Project.objects.filter(pk__in = id_list, is_finished = is_finished)
    data = projects
    serializer = ProjectSerializer(data, context={'request': request}, many = True)
    return Response({'data': serializer.data})

@api_view(['GET'])
def team_list_by_user(request):
    
    data = []
    id_list = []
    items = UserToTeam.objects.filter(user = request.user)
    for i in range(len(items)):
        id_list.append(items[i].project.pk)
    teams = Team.objects.filter(pk__in = id_list)
    data = teams
    serializer = TeamSerializer(data, context={'request': request}, many = True)
    return Response({'data': serializer.data})

@api_view(['GET'])
def task_list_by_user_and_project(request, project):

    data = []
    items = Task.objects.filter(user = request.user, project = project) 
    data = items
    serializer = TaskSerializer(data, context={'request': request}, many = True)
    return Response({'data': serializer.data})

@api_view(['POST'])
def create_project(request):

    project = {
            "name": request.data["name"],
            "description": request.data["description"],
            "status": request.data["status"],
            "created_by": request.user.pk,
            "start_date": request.data["start_date"],     #time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "finish_date": request.data["finish_date"],
            "created_at": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "is_fineshed": False,
        }

    serializer = ProjectSerializer(data=project)

    if serializer.is_valid():
        print('serializer is valid')
        serializer.save()
    else:    
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    currProject = Project.objects.last()

    userToProject = {
        "user": request.user.pk,
        "project": currProject.pk,
    }

    serializer = UserToProjectSerializer(data=userToProject)

    if serializer.is_valid():
        print('serializer is valid')
        serializer.save()
    else:    
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer = PermissionsSerializer(data=userToProject)

    if serializer.is_valid():
        print('serializer is valid')
        serializer.save()
    else:    
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(data = [userToProject, project], status=status.HTTP_201_CREATED)

@api_view(['POST'])
def create_team(request):

    team = {
            "name": request.data["name"],
            "created_by": request.user.pk,
            "created_at": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        }

    serializer = TeamSerializer(data=team)

    if serializer.is_valid():
        print('serializer is valid')
        serializer.save()
    else:    
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    currTeam = Team.objects.last()

    userToTeam = {
        "user": request.user.pk,
        "team": currTeam.pk,
    }

    serializer = UserToTeamSerializer(data=userToTeam)

    if serializer.is_valid():
        print('serializer is valid')
        serializer.save()
    else:    
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(data = [userToTeam, team], status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_project_invites(request):

    data = []
    invites = ProjectInvite.objects.filter(user_get = request.user.pk)

    #id_list = []

    #for i in len(invites):
    #    id_list.append(invites[i].project.pk)

    #projects = Project.objects.filter(id__in = id_list)

    for invite in invites:
        data.append({
            "pk": invite.pk,
            "project": invite.project.name,
            "project_id": invite.project.pk,
            "user_send": invite.user_sent.first_name,
            "user_get": invite.user_get.first_name,
        })

    #data = invites
    #serializer = ProjectInviteSerializer(data, context={'request': request}, many = True)
    return Response(data = data)

@api_view(['POST'])
def create_project_invite(request):

    try:
        user = User.objects.get(tag = request.data["user_get"])
    except:
        message = "User does not exist"
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    if(ProjectInvite.objects.filter(user_sent = request.user.pk, user_get = user.pk, project = request.data["project"])):
        
        message = "Invite already exist"
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    projectInvite = {
        "user_sent": request.user.pk,
        "user_get": user.pk,
        "project": request.data["project"],
        "created_at": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "message": request.data["message"],
    }

    serializer = ProjectInviteSerializer(data=projectInvite)

    if serializer.is_valid():
        print('serializer is valid')
        serializer.save()
    else:    
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(projectInvite, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def accept_project_invite(request):

    invite = ProjectInvite.objects.get(pk = request.data["invite"])

    userToProject = {
        "user": invite.user_get.pk,
        "project": invite.project.pk
    }

    serializer = UserToProjectSerializer(data=userToProject)

    if serializer.is_valid():
        print('serializer is valid')
        serializer.save()
    else:    
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = PermissionsSerializer(data=userToProject)

    if serializer.is_valid():
        print('serializer is valid')
        serializer.save()
    else:    
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    ProjectInvite.objects.filter(pk = request.data["invite"]).delete()

    return Response(status = status.HTTP_200_OK)

@api_view(['DELETE'])
def decline_project_invite(request):

    ProjectInvite.objects.filter(pk = request.data["invite"]).delete()

    return Response(status = status.HTTP_200_OK)

@api_view(['GET'])
def get_team_invites(request):

    data = []
    invites = TeamInvite.objects.filter(user_get = request.user.pk)
    data = invites
    serializer = TeamInviteSerializer(data, context={'request': request}, many = True)
    return Response({'data': serializer.data})

@api_view(['POST'])
def create_team_invite(request):

    teamInvite = {
        "user_sent": request.user.pk,
        "user_get": request.data["user_get"],
        "team": request.data["project"],
        "created_at": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "message": request.data["message"],
    }

    serializer = TeamInviteSerializer(data=teamInvite)

    if serializer.is_valid():
        print('serializer is valid')
        serializer.save()
    else:    
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(teamInvite, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def accept_team_invite(request):

    invite = TeamInvite.objects.get(pk = request.data["invite"])

    userToTeam = {
        "user": invite.user_get,
        "team": invite.team
    }

    serializer = UserToTeamSerializer(data=userToTeam)

    if serializer.is_valid():
        print('serializer is valid')
        serializer.save()
    else:    
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    TeamInvite.objects.filter(pk = request.data["invite"]).delete()

    return Response(status = status.HTTP_200_OK)

@api_view(['DELETE'])
def deciline_team_invite(request):

    TeamInvite.objects.filter(pk = request.data["invite"]).delete()

    return Response(status = status.HTTP_200_OK)

@api_view(['POST'])
def create_task(request):

    task = {
            "name": request.data["name"],
            "description": request.data["description"],
            "start_date": request.data["start_date"],
            "end_date":request.data["end_date"], 
            "priority": request.data["priority"],
            "status": "N",
            "group": request.data["group"],
            "project": request.data["project"],
        }

    serializer = TaskSerializer(data=task)

    if serializer.is_valid():
        print('serializer is valid')
        serializer.save()
    else:    
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(data = task, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def edit_project(request):

    try:
        project = Project.objects.get(pk = request.data["pk"])

        if request.data['name'] != "":
            project.name = request.data["name"]

        if request.data['description'] != "":
            project.description = request.data["description"]
        
        if request.data['status'] != "":
            project.status = request.data["status"]

        project.save()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    data = []
    project = Project.objects.filter(pk = request.data["pk"]) 
    data = project
    serializer = ProjectSerializer(data, context={'request': request}, many = True)
    
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def edit_permission(request, user, project, permission):

    try:
        permissions = Permissions.objects.get(user = user, project = project)

        if permission == "can_invite_user":
            permissions.can_invite_user = not permissions.can_invite_user

        if permission == "can_kick_user":
            permissions.can_kick_user = not permissions.can_kick_user
        
        if permission == "can_edit_user_permission":
            permissions.can_edit_user_permission = not permissions.can_edit_user_permission
        
        if permission == "can_create_task":
            permissions.can_create_task = not permissions.can_create_task

        if permission == "can_delete_task":
            permissions.can_delete_task = not permissions.can_delete_task

        if permission == "can_edit_task":
            permissions.can_edit_task = not permissions.can_edit_task
        
        if permission == "can_checkout_task":
            permissions.can_checkout_task = not permissions.can_checkout_task
        
        if permission == "can_set_user_to_task":
            permissions.can_set_user_to_task = not permissions.can_set_user_to_task

        permissions.save()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_200_OK)

@api_view(['PUT'])
def edit_task(request):

    try:
        task = Task.objects.get(pk = request.data["pk"])

        if request.data['name'] != "":
            task.name = request.data["name"]

        if request.data['description'] != "":
            task.description = request.data["description"]

        if request.data['start_date'] != "":
            task.start_date = request.data["start_date"]

        if request.data['end_date'] != "":
            task.end_date = request.data["end_date"]
        
        if request.data['priority'] != "":
            task.status = request.data["priority"]

        if request.data['group'] != "":
            task.group = request.data["group"]

        task.save()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    data = []
    task = Task.objects.filter(pk = request.data["pk"]) 
    data = task
    serializer = TaskSerializer(data, context={'request': request}, many = True)

    return Response({'data': serializer.data}, status=status.HTTP_200_OK) #add return new object

@api_view(['PUT'])
def task_status(request):

    task = Task.objects.get(pk = request.data["pk"])

    task.status = request.data["status"]

    task.save()

    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def user_to_project(request):

    print(request.data)

    try:
        project = Project.objects.get(name = request.data["name"])
    except:
        message = 'project not exist'
        return Response(data = message, status=status.HTTP_400_BAD_REQUEST)
    

    if(len(UserToProject.objects.filter(user = request.user.pk, project = project)) >= 1):
        message = 'Project already exist'
        return Response(data = message, status=status.HTTP_406_NOT_ACCEPTABLE)

    if request.data["password"] == project.password:
    
        userToProject = {
            "user": request.user.pk,
            "project": project.pk,
            "project_role": "W",
        }

        serializer = UserToProjectSerializer(data=userToProject)

        if serializer.is_valid():
            print('serializer is valid')
            serializer.save()
        else:    
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = []
        items = Project.objects.filter(pk = project.pk,) 
        data = items
        serializer = ProjectSerializer(data, context={'request': request}, many = True)

        return Response(data = serializer.data, status=status.HTTP_201_CREATED)
    
    message = 'invalid password'

    return Response(data = message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def user_to_task(request):

    task = Task.objects.get(pk = request.data["task_id"])
    user = User.objects.get(email = request.data["email"])

    task.user = user

    task.save()
    
    data = []
    tasks = Task.objects.filter(pk = request.data["task_id"]) 
    data = tasks
    serializer = TaskSerializer(data, context={'request': request}, many = True)
    
    return Response(data = serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_task(request):
    print(request.data)
    Task.objects.filter(pk = request.data["task_id"]).delete()
    
    return Response(status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_project(request):

    Project.objects.filter(pk = request.data["project"]).delete()

    UserToProject.objects.filter(project = request.data["project"]).delete()
    
    return Response(status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_user_from_task(request):

    task = Task.objects.get(pk = request.data["task_id"])

    task.user = None

    task.save()

    data = []
    tasks = Task.objects.filter(pk = request.data["task_id"]) 
    data = tasks
    serializer = TaskSerializer(data, context={'request': request}, many = True)
    
    return Response(data = serializer.data, status=status.HTTP_200_OK) 

@api_view(['DELETE'])
def delete_user_from_project(request):

    UserToProject.objects.filter(project = request.data["project"], user = request.data["user"]).delete()
    
    return Response(status=status.HTTP_200_OK) #add validation on request.data

@api_view(['DELETE'])
def delete_user_from_team(request):

    UserToTeam.objects.filter(project = request.data["team"], user = request.data["user"]).delete()
    
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def finish_project(request):

    project = Project.objects.get(pk = request.data["project"])

    project.is_finished = True
    
    return Response(status=status.HTTP_200_OK)