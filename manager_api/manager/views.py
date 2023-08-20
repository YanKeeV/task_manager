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

from .models import *
from .serializers import *

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def auth(request, format=None):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):

    validated_data = {
        "email": request.data["email"],
        "first_name": request.data["first_name"],
        "last_name": request.data["last_name"],
        "password": request.data["password"],
    }
    
    try:
        user = UserSerializer.create(validated_data)
    except:
        message = "Email already exist"
        return Response(data = message, status=status.HTTP_400_BAD_REQUEST)
    
    data = serialize("json", [user], fields = ('email', 'first_name', 'last_name'))

    return Response(data = data)

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
def users_by_project(request):

    data = []
    try:
        users = UserToProject.objects.filter(project = request.data["project"])
    except ValueError: 
        return Response(exception=ValueError, status=status.HTTP_400_BAD_REQUEST)
    data = users
    serializer = TaskSerializer(data, context={'request': request}, many = True)
    return Response({'data': serializer.data})

@api_view(['GET'])
def get_user(request):

    data = []
    items = User.objects.filter(email = request.user)
    data = items
    serializer = UserSerializer(data, context={'request': request}, many = True)
    return Response({'data': serializer.data})

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
def task_list_by_user_and_project(request):

    data = []
    items = Task.objects.filter(user = request.user, project = request.data["project"]) 
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
            "start_date": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "end_date":request.data["end_date"], 
            "priority": request.data["priority"],
            "status": "N",
            "group": request.data["group"],
            "project": request.data["project"],
            "executor": request.user.pk,
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

        if request.data.__contains__('name'):
            project.name = request.data["name"]

        if request.data.__contains__('password'):
            project.password = request.data["password"]

        if request.data.__contains__('description'):
            project.description = request.data["description"]
        
        if request.data.__contains__('status'):
            project.status = request.data["status"]

        if request.data.__contains__('end_date'):
            project.end_date = request.data["end_date"]

        project.save()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
    
    return Response(status=status.HTTP_200_OK) #add return new object

@api_view(['PUT'])
def edit_task(request):

    try:
        task = Task.objects.get(pk = request.data["pk"])

        if request.data.__contains__('name'):
            task.name = request.data["name"]

        if request.data.__contains__('description'):
            task.description = request.data["description"]

        if request.data.__contains__('end_date'):
            task.end_date = request.data["end_date"]
        
        if request.data.__contains__('status'):
            task.status = request.data["status"]

        if request.data.__contains__('group'):
            task.group = request.data["group"]

        if request.data.__contains__('user'):
            task.user = request.data["user"]

        task.save()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK) #add return new object

@api_view(['PUT'])
def task_status(request):

    task = Task.objects.get(pk = request.data["pk"])

    task.status = request.data["status"]

    task.save()

    return Response(status=status.HTTP_200_OK)

@api_view(['PUT'])
def edit_user(request):

    user = User.objects.get(email = request.user)

    #add if state

    user.save()
    
    return Response(status=status.HTTP_200_OK) #add return new object

@api_view(['POST'])
def user_to_project(request):

    try:
        project = Project.objects.get(name = request.data["name"])
    except:
        message = 'project not exist'
        return Response(data = message, status=status.HTTP_400_BAD_REQUEST)
    

    if(UserToProject.objects.get(user = request.user.pk, project = request.data["name"])):
        message = 'user already exist'
        return Response(data = message, status=status.HTTP_400_BAD_REQUEST)

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
    
    return Response(status=status.HTTP_200_OK) #add return new object

@api_view(['DELETE'])
def delete_task(request):

    Task.objects.filter(pk = request.data["task_id"]).delete()
    
    return Response(status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_project(request):

    Project.objects.filter(pk = request.data["project"]).delete()
    
    return Response(status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_user_from_task(request):

    task = Task.objects.get(pk = request.data["task_id"])

    task.user = None

    task.save()
    
    return Response(status=status.HTTP_200_OK) #add validation on request.data

@api_view(['DELETE'])
def delete_user_from_project(request):

    UserToProject.objects.filter(project = request.data["project"], user = request.data["user"]).delete()
    
    return Response(status=status.HTTP_200_OK) #add validation on request.data