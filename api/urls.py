from django.urls import path
from .views import UserRegistrationView, UserLoginView
from .views import VideoUploadView, UserVideosView
from .views import AllDataTypesView
from .views import UserDataView, GenerateDataView
from .views import AllNerfsView
from .views import GenerateNerfModelView, UserNerfModelsView
from .views import AllExportMethodsView
from .views import GenerateNerfObjectView, UserNerfObjectsView
from .views import AddReviewView, DataTypeReviews, DataReviews, NerfReviews, NerfModelReviews, ExportMethodReviews, NerfObjectReviews 

urlpatterns = [

    # users
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),

    # videos
    path('video-upload/', VideoUploadView.as_view(), name='video-upload'),
    path('user/videos/', UserVideosView.as_view(), name='user-videos'),

    # data types
    path('all-data-types/', AllDataTypesView.as_view(), name='all-data-types'),

    # data
    path('generate/data/', GenerateDataView.as_view(), name='generate-data'),
    path('user/data/', UserDataView.as_view(), name='user-data'),

    # nerfs
    path('all-nerfs/', AllNerfsView.as_view(), name='all-nerfs'),

    # nerf models
    path('generate/nerf-model/', GenerateNerfModelView.as_view(), name='generate-nerf-model'),
    path('user/nerf-models/', UserNerfModelsView.as_view(), name='user-nerf-models'),

    # export methods
    path('all-export-methods', AllExportMethodsView.as_view(), name='all-export-methods'),

    # nerf objects
    path('generate/nerf-object/', GenerateNerfObjectView.as_view(), name='generate-nerf-object'),
    path('user/nerf-objects/', UserNerfObjectsView.as_view(), name='user-nerf-objects'),

    # reviews
    path('add-review/', AddReviewView.as_view(), name='add-review'),
    path('reviews/data-type/', DataTypeReviews.as_view(), name='reviews-data-type'),
    path('reviews/data/', DataReviews.as_view(), name='reviews-data'),
    path('reviews/nerf/', NerfReviews.as_view(), name='reviews-nerf'),
    path('reviews/nerf-model/', NerfModelReviews.as_view(), name='reviews-nerf-model'),
    path('reviews/export-method/', ExportMethodReviews.as_view(), name='reviews-export-method'),
    path('reviews/nerf-object/', NerfObjectReviews.as_view(), name='reviews-nerf-objects')

]