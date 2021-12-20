from django.contrib import admin

from .models import Songs, Playlist,NameAlbum


admin.site.register(Songs)
admin.site.register(Playlist)
admin.site.register(NameAlbum)
