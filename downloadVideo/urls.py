from django.contrib import admin
from django.urls import path
from downloadVideo import views

urlpatterns = [
    path('', views.home, name='download'),
     path('download_media/', views.download_media, name='download'),

]