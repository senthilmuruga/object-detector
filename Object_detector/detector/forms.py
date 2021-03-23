from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from .models import Video, Camera


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Enter a valid email address')
    botcatcher = forms.CharField(required=False, widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)])
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]


class VideoForm(forms.ModelForm):

    camera_id = forms.ModelChoiceField(queryset=Camera.objects.all())
    video_name = forms.CharField(label='Video Name', widget=forms.TextInput(attrs={'placeholder': 'Enter the video name'}))
    video = forms.FileField()
    date = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-mm-dd'}))
    hour = forms.CharField(max_length=2, widget=forms.TextInput(attrs={'placeholder': 'Two digits only'}))

    class Meta:
        model = Video
        fields = ["camera_id", "video_name", "video", "date", "hour"]
