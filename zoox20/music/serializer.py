from django.db.models import fields
from rest_framework import serializers
from .models import Playlist, Songs ,NameAlbum

class SongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songs
        fields = ("id" , "title", "artist", "song" , "album","release","image","like","view")

class NameAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = NameAlbum
        fields = ("id" , "title", "artist","image")

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ("id", "playlist_name", "user", "song", "title", "artist", "image")

