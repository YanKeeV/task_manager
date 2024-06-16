from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status

from .models import *
from .serializers import *

@api_view(['GET'])
def file_list_by_folder(request):

    data = []
    items = Task.objects.filter(user = request.user).order_by('end_date')
    data = items
    serializer = TaskSerializer(data, context={'request': request}, many = True)
    return Response({'data': serializer.data})

@api_view(['POST'])
def upload_file(request):

    
    return Response()

@api_view(['DELETE'])
def delete_file(request):

    
    return Response()