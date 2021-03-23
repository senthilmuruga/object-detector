from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from .validator import file_size


# Create your models here.
class Camera(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    camera_name = models.CharField(max_length=35)

    def __str__(self):
        return self.camera_name


class Video(models.Model):
    camera_id = models.ForeignKey(Camera, on_delete=models.CASCADE)
    video_name = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos\%Y\%m\%d', validators=[file_size])
    date = models.DateField()
    hour = models.CharField(max_length=2)

    def __str__(self):
        return self.video_name

class Detector(models.Model):
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)
    frame_no = models.IntegerField()
    object_ind = models.CharField(max_length=2083)

class Setting(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	value = models.CharField(max_length=200)

	def __str__(self):
		return self.name



