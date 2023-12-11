from django.urls import path
from .views import UserRegistrationView, UserLoginView
from .views import VideoUploadView, UserVideosView
from .views import AllDataTypesView
from .views import UserDataView, GenerateDataView
from .views import AllNerfsView
from .views import GenerateNerfModelView, UserNerfModelsView
from .views import AllExportMethodsView
from .views import GenerateNerfObjectView, UserNerfObjectsView
from .views import AddReviewView, AllReviewsView, DataTypeReviewsView, DataReviewsView, NerfReviewsView, NerfModelReviewsView, ExportMethodReviewsView, NerfObjectReviewsView 

urlpatterns = [

    # users
    path('user/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('user/login/', UserLoginView.as_view(), name='user-login'),

    # videos
    path('videos/upload/', VideoUploadView.as_view(), name='video-upload'),
    path('videos/user/', UserVideosView.as_view(), name='user-videos'),

    # data types
    path('data-types/all/', AllDataTypesView.as_view(), name='all-data-types'),

    # data
    path('data/generate/', GenerateDataView.as_view(), name='generate-data'),
    path('data/user/', UserDataView.as_view(), name='user-data'),

    # nerfs
    path('nerfs/all/', AllNerfsView.as_view(), name='all-nerfs'),

    # nerf models
    path('nerf-models/all/', GenerateNerfModelView.as_view(), name='generate-nerf-model'),
    path('nerf-models/user/', UserNerfModelsView.as_view(), name='user-nerf-models'),

    # export methods
    path('export-methods/all/', AllExportMethodsView.as_view(), name='all-export-methods'),

    # nerf objects
    path('generate/nerf-object/', GenerateNerfObjectView.as_view(), name='generate-nerf-object'),
    path('user/nerf-objects/', UserNerfObjectsView.as_view(), name='user-nerf-objects'),

    # reviews
    path('reviews/add/', AddReviewView.as_view(), name='add-review'),
    path('reviews/all/', AllReviewsView.as_view(), name='all-reviews'),
    path('reviews/data-type/', DataTypeReviewsView.as_view(), name='reviews-data-type'),
    path('reviews/data/', DataReviewsView.as_view(), name='reviews-data'),
    path('reviews/nerf/', NerfReviewsView.as_view(), name='reviews-nerf'),
    path('reviews/nerf-model/', NerfModelReviewsView.as_view(), name='reviews-nerf-model'),
    path('reviews/export-method/', ExportMethodReviewsView.as_view(), name='reviews-export-method'),
    path('reviews/nerf-object/', NerfObjectReviewsView.as_view(), name='reviews-nerf-objects')

]