from django.urls import path

# login - register
from .views import UserRegistrationView, UserLoginView
# data
from .views import DataUploadView, UserDataView
# datatypes
from .views import AllDataTypesView
# processed data
from .views import GenerateProcessedDataView, UserProcessedDataView
# nerfs
from .views import AllNerfsView
# nerf model
from .views import GenerateNerfModelView, UserNerfModelsView
# export method
from .views import AllExportMethodsView
# nerf object
from .views import GenerateNerfObjectView, UserNerfObjectsView
# reviews
from .views import AddReviewView, AllReviewsView, DataTypeReviewsView, DataReviewsView, NerfReviewsView, NerfModelReviewsView, ExportMethodReviewsView, NerfObjectReviewsView 

urlpatterns = [

    # users
    path('user/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('user/login/', UserLoginView.as_view(), name='user-login'),

    # data
    path('data/upload/', DataUploadView.as_view(), name='upload-data'),
    path('data/user/', UserVideosView.as_view(), name='user-data'),

    # data types
    path('data-types/all/', AllDataTypesView.as_view(), name='all-data-types'),

    # processed-data
    path('processed-data/generate/', GenerateDataView.as_view(), name='generate-processed-data'),
    path('processed-data/user/', UserDataView.as_view(), name='user-processed-data'),

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