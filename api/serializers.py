from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Video, Nerf, NerfModel, NerfObject

# USERS

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

# VIDEOS

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'user', 'video_file', 'name', 'upload_date']
        read_only_fields = ['id', 'user', 'upload_date']

class VideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'nombre', 'fecha_subida']

# NERFS

class NerfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nerf
        fields = ['id', 'name', 'long_name', 'url']

# MODELS

class NerfModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NerfModel
        fields = '__all__'

class NerfModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NerfModel
        fields = ['id', 'archivo', 'fecha_creacion'] 

# OBJECTS

class NerfObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = NerfObject
        fields = '__all__'

class NerfObjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NerfObject
        fields = ['id', 'archivo', 'fecha_creacion']
