from rest_framework import serializers

from django.contrib.auth.models import User

# USERS

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

from .models import Video

# VIDEOS

class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'user', 'video_file', 'name', 'upload_date']
        read_only_fields = ['id', 'user', 'upload_date']

class VideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'name', 'upload_date']

from .models import DataType

# DATA TYPE

class DataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataType
        fields = '__all__'

from .models import Data

# DATA

class GenerateDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['id', 'user', 'video', 'data_type', 'status', 'data_file', 'start_date', 'end_date', 'creation_time']
        read_only_fields = ['id', 'user', 'status', 'data_file', 'start_date', 'end_date', 'creation_time']

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'

from .models import Nerf

# NERFS

class NerfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nerf
        fields = '__all__'

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
