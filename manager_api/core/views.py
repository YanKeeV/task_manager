import time
from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.serializers import serialize
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework import status
from django.contrib.auth import update_session_auth_hash

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
        "tag": request.data["tag"],
    }
    
    try:
        user = UserSerializer.create(validated_data)
        #user.set_password(request.data["password"])
        #user.save()
    except:
        message = "Email or tag already exist"
        return Response(data = message, status=status.HTTP_400_BAD_REQUEST)
    
    #data = serialize("json", [user], fields = ('email', 'first_name', 'last_name'))

    data = []
    user = User.objects.filter(email = request.data["email"])
    data = user
    serializer = UserSerializer(data, context={'request': request}, many = True)
    return Response({'data': serializer.data}, status = status.HTTP_201_CREATED)

@api_view(['GET'])
def get_user(request):

    data = []
    items = User.objects.filter(email = request.user.email)
    data = items
    print(items)
    serializer = UserSerializer(data, context={'request': request}, many = True)
    return Response({'data': serializer.data})

@api_view(['PUT'])
def edit_user(request):
    print(request.data)
    user = User.objects.get(email = request.user.email)

    if request.data["first_name"] != "":
        user.first_name = request.data["first_name"]
    
    if request.data["last_name"] != "":
        user.last_name = request.data["last_name"]

    if request.data["email"] != "":
        user.email = request.data["email"]

    if request.data["status"] != "":
        user.status = request.data["status"]

    if request.data["tag"] != "":
        user.tag = request.data["tag"]

    if request.data["role"] != "":
        user.role = request.data["role"]

    user.save()

    data = []
    user = User.objects.filter(email = user.email) 
    print(user)
    data = user
    serializer = UserSerializer(data, context={'request': request}, many = True)
    
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def edit_user_password(request):

    user = request.user

    # Получаем данные из запроса
    current_password = request.data.get("old_password")
    new_password = request.data.get("new_password")
        
    print(current_password, new_password)
    # Проверяем, что текущий пароль правильный
    if not user.check_password(current_password):
        return Response({"error": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

    # Устанавливаем новый пароль и сохраняем
    user.set_password(new_password)
    user.save()

    update_session_auth_hash(request, user)  # To update session after password change

    return Response({"success": "Password changed successfully."}, status=status.HTTP_200_OK)
            
@api_view(['PUT'])
@parser_classes([MultiPartParser, FormParser])
def set_image(request):

    user = request.user
    print(request.data)
    user_serializer = UserSerializer(user, data=request.data, partial=True)
    if user_serializer.is_valid():
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
