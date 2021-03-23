from django.contrib import admin
from .models import Camera, Detector, Setting, Video

# Register your models here.

admin.site.register(Camera)
admin.site.register(Detector)
admin.site.register(Setting)
admin.site.register(Video)