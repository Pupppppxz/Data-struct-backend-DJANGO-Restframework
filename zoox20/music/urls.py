from django.urls import path, re_path
from django.urls.conf import include

from .views import ListSongsView , PostSongsView, SearchSong, PlaylistView,BestSongsView,ListAlbumView,SearchNameAlbum, songInAlbum,PlayNext,NamePlaylist, UpdateViewSong
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('songs/', ListSongsView.as_view(), name="songs-all"),
    path('album/', ListAlbumView.as_view(), name="album-all"),
    path('bestSongsView/', BestSongsView.as_view(), name="Top-songs"),
    path('songs1/', csrf_exempt(PostSongsView.as_view()), name="songs-all2"),
    path('song-search/', SearchSong.as_view()),
    path('album-search/', SearchNameAlbum.as_view()),
    path('songInAlbum/', songInAlbum.as_view()),
    path('create-playlist/', PlaylistView.as_view()),
    path('get-playlist/', PlaylistView.as_view()),
    path('playnext/', PlayNext.as_view()),
    path('update-view/', csrf_exempt(UpdateViewSong.as_view()), name="update-song"),
    path('getNamePlaylist/', NamePlaylist.as_view()),
]