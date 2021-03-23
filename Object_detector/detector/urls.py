from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerPage, name="register"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('camera_page/<int:camera_id>', views.camera_page, name="camera_page"),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('add_camera/', views.add_camera, name='add_camera'),
    path('upload_video/',views.upload_video,name='upload_video'),
    path('video_render/<int:camera_id>', views.video_render, name='video_render'),
    path('data_processing/<int:camera_id>', views.data_processing, name='data_processing'),
    path('user_settings/', views.userSettings, name="user_settings"),
	path('update_theme/', views.updateTheme, name="update_theme"),
    path('video_delete/', views.video_delete, name='video_delete'),

]