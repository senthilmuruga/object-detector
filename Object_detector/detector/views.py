from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from .serializers import UserSerailizer
from datetime import datetime, timedelta
from .decorators import unauthenticated_user
from .forms import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Camera, Detector, Setting, Video
import random
# import necessary modules
import cv2
import numpy as np
import sys

sys.path.append(".")
from .YoloDetector import *
import os

import datetime
from django.http import StreamingHttpResponse

from django.views.decorators import gzip
from django.http import FileResponse

# Create your views here.
def index(request):
    return render(request, "detector/index.html")


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()

            messages.success(request, 'Thank you for complete the registration')
            return redirect('index')

        else:
            form = CreateUserForm()
    return render(request, 'detector/register.html', {'form': form})


@login_required(login_url='login')
def dashboard(request):
    camera_list = Camera.objects.all()
    if camera_list is not None:
        context = {'camera_list': camera_list}
        return render(request, 'detector/dashboard.html', context)

    else:
        messages.warning(request, "No Camera list added")
        return render(request, 'detector/dashboard.html')


def login_view(request):
    user_name = request.POST.get('username')
    password_data = request.POST.get('inputPassword')
    user = authenticate(username=user_name, password=password_data)
    if user is not None and user.is_active:
        login(request, user)
        return redirect('dashboard')
    else:
        data = "username or password incorrect"
        messages.error(request, data)
        return redirect('index')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('index')


names = os.path.join(os.getcwd(), "static\coco.names")
cfg = os.path.join(os.getcwd(), "static\yolov3-tiny.cfg")
weights = os.path.join(os.getcwd(), "static\yolov3-tiny.weights")
current_path = os.getcwd()


class VideoCamera(object):

    def __init__(self, video, video_id, names, cfg, weights, objs):
        self.names = names
        self.cfg = cfg
        self.weights = weights
        self.objs = objs
        self.video = cv2.VideoCapture(video)
        self.selected = {}
        self.detector = None
        self.video_id = video_id
        self.frame_counter = 1


    def __del__(self):
        self.video.release()

    def preProcessor(self):
        with open(self.names, 'r') as f:
            classes = [w.strip() for w in f.readlines()]

        color = [(0, 0, 0), (235, 52, 52), (232, 235, 52), (52, 235, 52), (52, 189, 235), (52, 64, 235), (235, 52, 192),
                 (0, 255, 255)]

        for i, obj in enumerate(self.objs):
            try:
                self.selected[obj] = color[i]
            except:
                self.selected[obj] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.detector = YoloDetector(self.cfg, self.weights, classes)


    def get_frame(self):
        success, frame = self.video.read()
        # video stream.
        detections = self.detector.detect(frame)
        for cls, color in self.selected.items():
            if cls in detections:
                for box in detections[cls]:
                    x1, y1, x2, y2 = box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=1)
                    cv2.putText(frame, cls, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color)


        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()



    def get_frame_processed(self):
        success, frame = self.video.read()
        frame_num = self.frame_counter
        self.frame_counter += 1

        data = {}
        # video stream.
        detections = self.detector.detect(frame)
        for cls, color in self.selected.items():
            if cls in detections:
                count = 1
                for box in detections[cls]:
                    x1, y1, x2, y2 = box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=1)
                    cv2.putText(frame, cls, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color)
                    count += 1

            data[cls] = count
        return self.video_id, frame_num, data


def ori_gen(camera):
    try:

        while True:
            video_id, frame_num, data = camera.get_frame_processed()
            store = Detector.objects.create(video_id=video_id, frame_no=str(frame_num), object_ind=str(json.dumps(data, indent=1)))
            store.save()

    except Exception as e:
        print(str(e))


def gen(camera):
    try:
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    except:
        camera.__del__()


@login_required(login_url='login')
def add_camera(request):
    if request.method == 'POST':

        camera_name = request.POST.get('camera_name')

        camera = Camera.objects.create(user=request.user, camera_name=camera_name)
        camera.save()
        messages.info(request, "Carema created.")
        return redirect('dashboard')

    else:
        messages.warning(request, "your request was incorrect")
        return redirect("dashboard")


@login_required(login_url='login')
def camera_page(request, camera_id):
    camera = get_object_or_404(Camera, pk=camera_id)
    videos = Video.objects.filter(camera_id=camera)
    list_of_files = [video for video in videos]
    with open("./coco.names", 'r') as f:
        classes = [w.strip() for w in f.readlines()]
    context = {'camera': camera, 'list_of_files': list_of_files, 'classes': classes}
    return render(request, 'detector/camera.html', context)



@login_required(login_url='login')
def upload_video(request):
    form = VideoForm()
    if request.method == 'POST':
        form = VideoForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "video added successfully")
            return redirect("dashboard")

        else:
            form = VideoForm()
            messages.warning(request, "Invalid Data")
            context = {'form': form}
            return render(request, 'detector/video.html', context)

    context = {'form': form}
    return render(request, 'detector/video.html', context)


@gzip.gzip_page
@login_required(login_url='login')
def data_processing(request, camera_id):
    if request.method == 'POST':
        objs = request.POST.getlist('objs[]')
        video_name = request.POST.get('file')
        camera = Camera.objects.filter(pk=camera_id)[0]
        video = Video.objects.filter(video_name=video_name, camera_id=camera)[0]
        pre_path = "/".join(names.split('\\')[0: -2])
        video_path = "/".join([pre_path, video.video.url])
        int_camera = VideoCamera(video_path, video, names, cfg, weights, objs)
        int_camera.preProcessor()
        ori_gen(int_camera)
        return redirect('dashboard')

    else:
        messages.warning(request, "your request was incorrect")
        return redirect("dashboard")


@gzip.gzip_page
@login_required(login_url='login')
def video_render(request, camera_id):
    if request.method == 'POST':
        objs = request.POST.getlist('objs[]')
        video_name = request.POST.get('file')
        camera = Camera.objects.filter(pk=camera_id)[0]
        video = Video.objects.filter(video_name=video_name, camera_id=camera)[0]
        pre_path = "/".join(names.split('\\')[0: -2])
        video_path = "/".join([pre_path, video.video.url])
        print(video_path)
        camera = VideoCamera(video_path, video, names, cfg, weights, objs)
        camera.preProcessor()

        return StreamingHttpResponse(gen(camera), content_type='multipart/x-mixed-replace; boundary=frame')

    else:
        messages.warning(request, "your request was incorrect")
        return redirect("dashboard")


def video_delete(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        print(type(day))
        current_date = datetime.date.today()
        print(current_date)
        threshold_day = datetime.date.today() - timedelta(days=int(day))
        print(threshold_day)
        cameras = Camera.objects.filter(user=request.user)
        for camera in cameras:
            videos = Video.objects.filter(camera_id=camera, date__lt=threshold_day)
            for video in videos:
                video.delete()

        messages.warning(request, "Deleted Successfully")
        return redirect("dashboard")

    else:
        messages.warning(request, "No Videos")
        return redirect("dashboard")



def userSettings(request):
    user, created = User.objects.get_or_create(id=request.user.pk)
    setting = user.setting

    seralizer = UserSerailizer(setting, many=False)

    return JsonResponse(seralizer.data, safe=False)


def updateTheme(request):
    data = json.loads(request.body)
    theme = data['theme']

    setting, created = Setting.objects.get_or_create(name='theme', user=request.user)
    setting.value = theme
    setting.name = 'theme'
    setting.save()
    print('Request:', theme)
    return JsonResponse('Updated..', safe=False)

