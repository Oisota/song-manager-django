"""Core app urls"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('songs/', views.songs, name='songs'),
    path('songs/<song_id>/edit', views.song_edit, name='song_edit'),
    path('songs/<song_id>/delete', views.song_delete, name='song_delete'),
]