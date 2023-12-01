from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .serializers import UserSerializer, UserLoginSerializer
from .serializers import VideoUploadSerializer, VideoListSerializer
from .serializers import NerfSerializer
from .serializers import NerfModelListSerializer
from .serializers import NerfObjectListSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .models import Video, Nerf, NerfModel, NerfObject

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
            {'message': 'Usuario registrado exitosamente'}, 
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

# NERFS

class AllNerfsView(generics.ListAPIView):
    queryset = Nerf.objects.all()
    serializer_class = NerfSerializer

#  MODELS

from .utils import generate_nerf_model

class GenerateNerfModelView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        nerf = request.data.get('nerf')
        video_id = request.data.get('video_id')

        if nerf and video_id:
            generate_nerf_model.delay(nerf, video_id)  # Llama a la tarea Celery en segundo plano
            return Response({'message': 'Generando modelo, esto puede llevar tiempo.'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message': 'Se requieren nerf y video_id en los datos'}, status=status.HTTP_400_BAD_REQUEST)

class UserNerfModelsView(generics.ListAPIView):
    serializer_class = NerfModelListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna la lista de modelos del usuario actual
        return Modelo.objects.filter(video__usuario=self.request.user)


# OBJECTS

from .utils import generate_nerf_object

class GenerateNerfObjectView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        modelo_id = request.data.get('modelo_id')

        if modelo_id:
            generate_nerf_object.delay(modelo_id)  # Llama a la tarea Celery en segundo plano
            return Response({'message': 'Generando objeto, esto puede llevar tiempo.'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message': 'Se requiere modelo_id en los datos'}, status=status.HTTP_400_BAD_REQUEST)

class UserNerfObjectsView(generics.ListAPIView):
    serializer_class = NerfObjectListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Objeto.objects.filter(modelo__video__usuario=self.request.user)


