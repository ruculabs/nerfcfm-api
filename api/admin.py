from django.contrib import admin
from .models import Data, ExportMethod, ProcessedData, DataType, Nerf, NerfModel, NerfObject

admin.site.register(Data)
admin.site.register(ProcessedData)
admin.site.register(DataType)
admin.site.register(Nerf)
admin.site.register(ExportMethod)
admin.site.register(NerfModel)
admin.site.register(NerfObject)
