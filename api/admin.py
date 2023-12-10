from django.contrib import admin
from .models import Video, ExportMethod, Data, DataType, Nerf, NerfModel, NerfObject

admin.site.register(Video)
admin.site.register(Data)
admin.site.register(DataType)
admin.site.register(Nerf)
admin.site.register(ExportMethod)
admin.site.register(NerfModel)
admin.site.register(NerfObject)