from django.contrib import admin
from .models import Video, Nerf, NerfModel, NerfObject

admin.site.register(Video)
admin.site.register(Nerf)
admin.site.register(NerfModel)
admin.site.register(NerfObject)