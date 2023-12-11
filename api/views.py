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

# NERFS

class AllNerfsView(generics.ListAPIView):
    queryset = Nerf.objects.all()
    serializer_class = NerfSerializer

#  MODELS

from .utils import generate_nerf_model

class GenerateNerfModelView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        try:
            # get request values
            nerf_id = request.data.get('nerf_id')
            video_id = request.data.get('video_id')
            user_id = request.data.get('user_id')

            # check that there are both nerf_id and video_id
            if not (nerf_id and video_id and user_id):
                return Response(
                    {'message': 'Need nerf_id, video_id and user_id'}, 
                    status=status.HTTP_400_BAD_REQUEST)
            
            # check if nerf_id and video_id are integers
            try:
                nerf_id = int(nerf_id)
                video_id = int(video_id)
                user_id = int(user_id)
            except:
                return Response(
                    {'message': 'nerf_id, video_id and user_id must be integers'}, 
                    status=status.HTTP_400_BAD_REQUEST)

            # get nerf 
            nerf = Nerf.objects.get(id=nerf_id)

            if not nerf:
                return Response(
                    {'message': f'No nerf found for: nerf_id = {nerf_id}'}, 
                    status=status.HTTP_400_BAD_REQUEST)
            
            # get video
            video = Video.objects.get(id=video_id)

            if not video:
                return Response(
                    {'message': f'No video found for: video_id = {video_id}'}, 
                    status=status.HTTP_400_BAD_REQUEST)
            
            # get user
            user = User.objects.get(id=user_id)

            if not user:
                return Response(
                    {'message': f'No user found for: user_id = {user_id}'}, 
                    status=status.HTTP_400_BAD_REQUEST)

            # check if nerf has name
            if not nerf.name:
                return Response(
                    {'message': f'No name found for: nerf_id = {nerf_id}'}, 
                    status=status.HTTP_400_BAD_REQUEST)
            
            # check if video has file
            if not video.video_file:
                return Response(
                    {'message': f'No file found for: video_id = {video_id}'}, 
                    status=status.HTTP_400_BAD_REQUEST)

            # create model
            try:
                
                nerf_model = NerfModel.objects.create(
                    video=video,
                    user=user,
                    nerf=nerf
                )

            except Exception as err:
                # internal error
                print('[GENERATE_NERF_MODEL]: Create Model Exception')
                print('-- GENERATE_NERF_MODEL EXCEPTION START --')
                print(err)
                print('-- GENERATE_NERF_MODEL EXCEPTION END --')
                return Response(
                    {'message': 'Error creating nerf_model, try later'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # activate celery task for generating nerf model
            generate_nerf_model.delay(nerf=nerf, video=video, user=user, nerf_model_id=nerf_model.id)

            return Response(
                {
                    'message': f'Generating {nerf.name} model',
                    'nerf_model_id': nerf_model.id
                }, 
                status=status.HTTP_202_ACCEPTED)
        
        except Exception as err:
            # internal error
            print('[GENERATE_NERF_MODEL]: General Exception')
            print('-- GENERATE_NERF_MODEL EXCEPTION START --')
            print(err)
            print('-- GENERATE_NERF_MODEL EXCEPTION END --')
            return Response(
                {'message': 'Unknown serverside error, try later'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserNerfModelsView(generics.ListAPIView):
    serializer_class = NerfModelListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna la lista de modelos del usuario actual
        return Modelo.objects.filter(video__usuario=self.request.user)

# EXPORT METHODS

class AllExportMethodsView(generics.ListAPIView):
    pass

# OBJECTS

from .utils import generate_nerf_object

class GenerateNerfObjectView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        try:
            # get request values
            nerf_model_id = request.data.get('nerf_model_id')
            user_id = request.data.get('user_id')

            # TODO: add support to multiple extract methods
            export_method = request.data.get('export_method')

            # check that there is both nerf_model_id and user_id
            if not (nerf_model_id and user_id and export_method):
                return Response(
                    {'message': 'Need nerf_model_id, user_id and export_method'}, 
                    status=status.HTTP_400_BAD_REQUEST)
            
            # check that model_id and user_id are integers
            try:
                nerf_model_id = int(nerf_model_id)
                user_id = int(user_id)
            except:
                return Response(
                    {'message': 'nerf_model_id and user_id must be integers'}, 
                    status=status.HTTP_400_BAD_REQUEST)

            # check supported extract method
            # TODO: add support to multiple extract methods
            try:
                assert(export_method == 'TSDF')
            except:
                return Response(
                    {'message': 'nerf_model_id and user_id must be integers'}, 
                    status=status.HTTP_400_BAD_REQUEST)

            # get nerf_model
            nerf_model = NerfModel.objects.get(id=nerf_model_id)

            if not nerf_model:
                return Response(
                    {'message': f'No nerf_model found for: nerf_model = {nerf_model_id}'}, 
                    status=status.HTTP_400_BAD_REQUEST)
            
            # get user
            user = User.objects.get(id=user_id)

            if not user:
                return Response(
                    {'message': f'No user found for: user = {user_id}'}, 
                    status=status.HTTP_400_BAD_REQUEST)
            
            # check if nerf_model has model file
            if not nerf_model.model_file:
                return Response(
                    {'message': f'No model_file found for: nerf_model = {nerf_model_id}'}, 
                    status=status.HTTP_400_BAD_REQUEST)

            # check if model in progress for this user
            user_nerf_models = NerfModel.objects.filter(user=user)
            user_in_progress_nerf_models = user_nerf_models.filter(status='in_progress')
            if user_in_progress_nerf_models:
                return Response(
                    {'message': f'Nerf Model is already in progress for: user_id = {user_id}'}, 
                    status=status.HTTP_400_BAD_REQUEST)


            # create object
            try:
                
                nerf_object = NerfModel.objects.create(
                    nerf_model=nerf_model,
                    user=user
                )

            except Exception as err:
                # internal error
                print('[GENERATE_NERF_OBJECT]: Create Object Exception')
                print('-- GENERATE_NERF_OBJECT EXCEPTION START --')
                print(err)
                print('-- GENERATE_NERF_OBJECT EXCEPTION END --')
                return Response(
                    {'message': 'Error creating nerf_model, try later'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # no issues with model, generate object
            generate_nerf_object.delay(nerf_model=nerf_model, user=user, nerf_object_id=nerf_object.id, mnethod='TSDF')
            return Response(
                {
                    'message': 'Generating model with TSDF',
                    'nerf_object_id': nerf_object.id
                },
                status=status.HTTP_202_ACCEPTED)
        
        except:
            # internal error
            return Response({'message': 'Serverside error, try later'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserNerfObjectsView(generics.ListAPIView):
    serializer_class = NerfObjectListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Objeto.objects.filter(modelo__video__usuario=self.request.user)

# REVIEWS

class AddReviewView(generics.CreateAPIView):
    pass

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