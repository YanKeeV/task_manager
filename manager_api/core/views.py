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
        #user.set_password(request.data["password"])
        #user.save()
    except:
        message = "Email already exist"
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
    items = User.objects.filter(email = request.user)
    data = items
    serializer = UserSerializer(data, context={'request': request}, many = True)
    return Response({'data': serializer.data})

@api_view(['PUT'])
def edit_user(request):

    user = User.objects.get(email = request.user)

    if request.data["first_name"] != "":
        user.first_name = request.data["first_name"]
    
    if request.data["last_name"] != "":
        user.last_name = request.data["last_name"]

    password_data = {
        "old_password": request.data["old_password"],
        "new_password": request.data["new_password"],
    }

    if request.data["new_password"] != "":
        serializer = ChangePasswordSerializer(data = password_data)
        if serializer.is_valid():
            if user.check_password(serializer.data.get('old_password')):
                user = request.user
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
            else:
                return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)

    if request.data["status"] != "":
        user.status = request.data["status"]

    user.save()

    data = []
    user = User.objects.filter(email = request.user) 
    data = user
    serializer = UserSerializer(data, context={'request': request}, many = True)
    
    return Response({'data': serializer.data}, status=status.HTTP_200_OK) #add return new object
