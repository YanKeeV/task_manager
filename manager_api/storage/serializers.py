from rest_framework import serializers

from .models import *
from core.serializers import *

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = '__all__'