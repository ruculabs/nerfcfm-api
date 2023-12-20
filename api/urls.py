from django.urls import path

# login - register
from .views import UserRegistrationView, UserLoginView
# data
from .views import DataUploadView, UserDataView, DataDetailView
# datatypes
from .views import AllDataTypesView
# processed data
from .views import GenerateProcessedDataView, UserProcessedDataView, ProcessedDataDetailView
# nerfs
from .views import AllNerfsView
# nerf model
from .views import GenerateNerfModelView, UserNerfModelsView, NerfModelDetailView
# export method
from .views import AllExportMethodsView
# nerf object
from .views import GenerateNerfObjectView, UserNerfObjectsView, NerfObjectDetailView
from .views import MeshNerfObjectView, TextureNerfObjectView, MaterialNerfObjectView
# reviews
from .views import AddReviewView, AllReviewsView, DataTypeReviewsView, DataReviewsView, NerfReviewsView, NerfModelReviewsView, ExportMethodReviewsView, NerfObjectReviewsView 

urlpatterns = [

    # users
    path('user/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('user/login/', UserLoginView.as_view(), name='user-login'),

    # data
    path('data/upload/', DataUploadView.as_view(), name='upload-data'),
    path('data/user/', UserDataView.as_view(), name='user-data'),
    path('data/<int:id>/', DataDetailView.as_view(), name='id-data'),

    # data types
    path('data-types/all/', AllDataTypesView.as_view(), name='all-data-types'),

    # processed-data
    path('processed-data/generate/', GenerateProcessedDataView.as_view(), name='generate-processed-data'),
    path('processed-data/user/', UserProcessedDataView.as_view(), name='user-processed-data'),
    path('processed-data/<int:id>/', ProcessedDataDetailView.as_view(), name='id-processed-data'),

    # nerfs
    path('nerfs/all/', AllNerfsView.as_view(), name='all-nerfs'),

    # nerf models
    path('nerf-models/generate/', GenerateNerfModelView.as_view(), name='generate-nerf-model'),
    path('nerf-models/user/', UserNerfModelsView.as_view(), name='user-nerf-models'),
    path('nerf-models/<int:id>/', NerfModelDetailView.as_view(), name='id-nerf-objects'),

    # export methods
    path('export-methods/all/', AllExportMethodsView.as_view(), name='all-export-methods'),

    # nerf objects
    path('nerf-objects/generate/', GenerateNerfObjectView.as_view(), name='generate-nerf-object'),
    path('nerf-objects/user/', UserNerfObjectsView.as_view(), name='user-nerf-objects'),
    path('nerf-objects/<int:id>/', NerfObjectDetailView.as_view(), name='id-nerf-objects'),
    path('nerf-objects/<int:nerf_object_id>/object/', MeshNerfObjectView.as_view(), name='object-nerf-objects'),
    path('nerf-objects/<int:nerf_object_id>/texture/', TextureNerfObjectView.as_view(), name='texture-nerf-objects'),
    path('nerf-objects/<int:nerf_object_id>/material/', MaterialNerfObjectView.as_view(), name='material-nerf-objects'),

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