from datetime import date
from authentication.models import User

from django.db import models

from django.db import models
from django.conf import settings
from django.urls.conf import include


# Create your models here.
class Songs(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    artist = models.CharField(max_length=255, null=False)
    song = models.FileField(upload_to='' , null=True)
    album = models.CharField(max_length=255, null=False)
    release = models.DateField(default=date.today().strftime("%d-%m-%Y"))
    image = models.ImageField(upload_to='cover/', null=True)
    like = models.IntegerField(default=0)
    view = models.IntegerField(default=0)
    
    def __str__(self):
        return "{}".format(self.title)

class NameAlbum(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    artist = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to='cover/', null=True)
    
    def __str__(self):
        return "{}".format(self.title)

class Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    playlist_name = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Songs, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False)
    artist = models.CharField(max_length=255, null=False)
    image = models.CharField(max_length=255, null=True)

    def __str__(self):
        return "{}".format(self.playlist_name)

