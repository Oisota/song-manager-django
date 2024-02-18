"""Core app urls"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('songs/', views.new_song, name='songs'),
    path('songs/<song_id>/edit', views.song_edit, name='song_edit'),
]