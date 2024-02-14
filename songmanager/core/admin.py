from django.contrib import admin

from core.models import User, Song, Status

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']