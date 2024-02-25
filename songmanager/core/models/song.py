"""Song Models"""

from django.db import models
from .user import User

#class Genre(models.Model):
#    name = models.CharField(max_length=255, unique=True)
#
#class Artist(models.Model):
#    name = models.CharField(max_length=255, unique=True)

#class Band(models.Model):
#    name = models.CharField(max_length=255, unique=True)
#    users = models.ManyToManyField(User)


# how well you know the song
class Status(models.Model):
    name = models.CharField(max_length=255, unique=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=255)
    duration = models.IntegerField(default=0) # duration in seconds
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)
    #artist = models.ForeignKey(Artist)
    #genre = models.ForeignKey(Genre)

    def __str__(self):
        return self.name

#class SetList(models.Model):
#    name = models.CharField(max_length=255, unique=True)
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    songs = models.ManyToManyField(Song)