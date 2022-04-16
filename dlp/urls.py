from django.urls import path

from . import views

urlpatterns = [
    path('list_dir', views.list_dir, name='list_dir'),
    path('read_file/', views.read_file, name='read_file'),
    path('upload', views.upload_file, name='upload_file'),
]