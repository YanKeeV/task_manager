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
    items = Task.objects.filter(user = request.user)
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
def users_by_project(request, project):

    data = []
    id_list = []
    try:
        items = UserToProject.objects.filter(project = project).select_related("user")
    except ValueError: 
        return Response(exception=ValueError, status=status.HTTP_400_BAD_REQUEST)
    print(items.query)

    users =[]
    for item in items:
        users.append({
            'id': item.user.pk,
            'first_name': item.user.first_name,
            'last_name': item.user.last_name,
            'email': item.user.email,
            'status': item.user.status,
            'project_role': item.project_role,
        })

    return Response(users, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_project(request, project):

    data = []
    project = Project.objects.filter(name = project)
    data = project
    serializer = ProjectSerializer(data, context={'request': request}, many = True)
    return Response({'data': serializer.data})

@api_view(['GET'])
def project_list_by_user(request):
    
    data = []
    id_list = []
    items = UserToProject.objects.filter(user = request.user)
    for i in range(len(items)):
        id_list.append(items[i].project.pk)
    projects = Project.objects.filter(pk__in = id_list)
    data = projects
    serializer = ProjectSerializer(data, context={'request': request}, many = True)
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
            "password": request.data["password"],
            "description": request.data["description"],
            "status": "some",
            "start_date": request.data["start_date"],     #time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "end_date": request.data["end_date"] 
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
        "project_role": "O",
    }

    serializer = UserToProjectSerializer(data=userToProject)

    if serializer.is_valid():
        print('serializer is valid')
        serializer.save()
    else:    
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(data = [userToProject, project], status=status.HTTP_201_CREATED)

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

        if request.data['password'] != "":
            project.password = request.data["password"]

        if request.data['description'] != "":
            project.description = request.data["description"]
        
        if request.data['status'] != "":
            project.status = request.data["status"]

        if request.data['end_date'] != "":
            project.end_date = request.data["end_date"]

        project.save()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    data = []
    project = Project.objects.filter(pk = request.data["pk"]) 
    data = project
    serializer = ProjectSerializer(data, context={'request': request}, many = True)
    
    return Response({'data': serializer.data}, status=status.HTTP_200_OK) #add return new object

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

@api_view(['POST'])
def finish_project(request):

    project = Project.objects.get(pk = request.data["project"])

    project.is_finished = True
    
    return Response(status=status.HTTP_200_OK)