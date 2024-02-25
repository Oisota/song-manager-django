"""Core app urls"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/register', views.register, name='register'),
    path('songs/', views.songs, name='songs'),
    path('songs/<song_id>', views.song, name='song'),
]