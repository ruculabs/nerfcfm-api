from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from dotenv import load_dotenv

load_dotenv()

from django.contrib.auth.models import User
from .serializers import UserSerializer, UserLoginSerializer

# USERS

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'message': 'User registration succesful'}, 
            status=status.HTTP_201_CREATED, 
            headers=headers)

class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'username': user.username}, status=status.HTTP_200_OK)

from .models import Video
from .serializers import VideoUploadSerializer, VideoListSerializer

# VIDEOS

class VideoUploadView(generics.CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoUploadSerializer
    permission_classes = [IsAuthenticated]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserVideosView(generics.ListAPIView):
    serializer_class = VideoListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Video.objects.filter(user=self.request.user)

from .models import DataType
from .serializers import DataTypeSerializer

# DATA TYPES

class AllDataTypesView(generics.ListAPIView):
    queryset = DataType.objects.all()
    serializer_class = DataTypeSerializer

from .models import Data
from .serializers import GenerateDataSerializer, UserDataSerializer

# DATA

class GenerateDataView(generics.CreateAPIView):
    queryset = Data.objects.all()
    serializer_class = GenerateDataSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        run_nerfstudio_command(serializer.data) 

class UserDataView(generics.ListAPIView):
    serializer_class = UserDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Data.objects.filter(user=self.request.user)

from .models import Nerf
from .serializers import NerfSerializer

# NERFS

class AllNerfsView(generics.ListAPIView):
    queryset = Nerf.objects.all()
    serializer_class = NerfSerializer

#  MODELS
from .serializers import NerfModelSerializer, GenerateNerfModelSerializer, NerfModelListSerializer
from .utils import generate_nerf_model

class GenerateNerfModelView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GenerateNerfModelSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        generate_nerf_model.delay(serializer.data) 

class UserNerfModelsView(generics.ListAPIView):
    serializer_class = NerfModelListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NerfModel.objects.filter(user=self.request.user)

# EXPORT METHODS
from .models import ExportMethod
from .serializers import ExportMethodSerializer

class AllExportMethodsView(generics.ListAPIView):
    queryset = ExportMethod.objects.all()
    serializer_class = ExportMethodSerializer

# OBJECTS
from .models import NerfObject
from .serializers import NerfObjectSerializer, GenerateNerfObjectSerializer
from .utils import generate_nerf_object

class GenerateNerfObjectView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GenerateNerfObjectSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        generate_nerf_object.delay(serializer.data)

class UserNerfObjectsView(generics.ListAPIView):
    serializer_class = NerfObjectListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Objeto.objects.filter(modelo__video__usuario=self.request.user)

# REVIEWS
from .models import Review
from .serializers import ReviewSerializer, AddReviewSerializer

class AddReviewView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DataTypeReviewsView(generics.ListAPIView):
    pass

class DataReviewsView(generics.ListAPIView):
    pass

class NerfReviewsView(generics.ListAPIView):
    pass

class NerfModelReviewsView(generics.ListAPIView):
    pass

class ExportMethodReviewsViews(generics.ListAPIView):
    pass

class NerfObjectReviewsView(generics.ListAPIView):
    pass