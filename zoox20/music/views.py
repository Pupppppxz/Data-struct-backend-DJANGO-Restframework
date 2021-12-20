from datetime import date
from functools import partial
from django import http
from django.shortcuts import get_object_or_404, render
from rest_framework.utils.encoders import JSONEncoder
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics ,filters, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Songs, Playlist,NameAlbum
from rest_framework import status
from .serializer import PlaylistSerializer, SongsSerializer,NameAlbumSerializer
import random

class ListSongsView(generics.ListAPIView):
    
    permission_classes = (IsAuthenticated,)
    
    """
    Provides a get method handler.
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    search_fields = ['title']
    filter_backends = (filters.SearchFilter,)
    
class UpdateViewSong(APIView):
    
    permission_classes = (IsAuthenticated,)
    
    def patch(self, request ,*args,**kwargs):
        id = request.GET.get('id')
        print("id", id)
        item = Songs.objects.get(id=id)
        views = item.values('view')['view'] + 1
        print("check", item, views)
        serializer = SongsSerializer(item, data={'view': views}, partial=True)
        if serializer.is_valid():
            return Response({"status": "success"})
        else:
            return Response({"status": "error"})

class ListAlbumView(generics.ListAPIView):
    
    permission_classes = (IsAuthenticated,)
    queryset = NameAlbum.objects.all()
    serializer_class = NameAlbumSerializer
    search_fields = ['title']
    filter_backends = (filters.SearchFilter,)

class PostSongsView(APIView):
    
    permission_classes = (IsAuthenticated,)
    
    def post(self, request , *args, **kwargs):
        serializer = SongsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request , *args, **kwargs):
        id = request.GET.get('id')
        item = Songs.objects.get(id=id)
        item1 = dict()
        views = item.view + 1
        item1['view'] = views
        serializer = SongsSerializer(item, data=item1, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success"})
        else:
            return Response({"status": "error"})

class SearchSong(generics.ListAPIView):
    
    permission_classes = (IsAuthenticated,)
    serializer_class = SongsSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = Songs.objects.all()
            state_name = self.request.GET.get('title', None)
            if state_name is not None:
                queryset = [i for i in queryset if state_name in i.title]
            else : queryset = []
            return queryset

class SearchNameAlbum(generics.ListAPIView):
    
    permission_classes = (IsAuthenticated,)
    serializer_class = NameAlbumSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = NameAlbum.objects.all()
            state_name = self.request.GET.get('title', None)
            if state_name is not None:
                queryset = [i for i in queryset if state_name in i.title]
            else : queryset = []
            return queryset

class songInAlbum(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = SongsSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            
            def mergeSort(arr):
                if len(arr) > 1:
        
                    mid = len(arr)//2
                    L = arr[:mid]
                    R = arr[mid:]
                    mergeSort(L)
                    mergeSort(R)
        
                    i = j = k = 0
                    while i < len(L) and j < len(R):
                        if ordinalCompare(L[i].title,R[j].title) :
                            arr[k] = L[i]
                            i += 1
                        else:
                            arr[k] = R[j]
                            j += 1
                        k += 1
            
                    while i < len(L):
                        arr[k] = L[i]
                        i += 1
                        k += 1
            
                    while j < len(R):
                        arr[k] = R[j]
                        j += 1
                        k += 1

            def ordinalCompare(arr1,arr2):
                for i in range(len(arr1)):
                    if len(arr2)>i:
                        if ord(arr1[i])<ord(arr2[i]):
                            return True
                        elif ord(arr1[i])==ord(arr2[i]):continue
                        else: return False
                    else: return False
                return True

            allSong = Songs.objects.all()
            state_name = self.request.GET.get('album', None)
            if state_name is not None:
                songInAlbum = [i for i in allSong if state_name == i.album]
                mergeSort(songInAlbum) 
                queryset = songInAlbum
            else : queryset = []
            return queryset


class BestSongsView(generics.ListAPIView):
    
    permission_classes = (IsAuthenticated,)
    serializer_class = SongsSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            allSongs = Songs.objects.all()
            state_name = self.request.GET.get('title', None)
            
            def partition(arr, low, high):
                i = (low-1)         
                pivot = arr[high].view
                for j in range(low, high):
                    if arr[j].view >= pivot:
                        i = i+1
                        arr[i], arr[j] = arr[j], arr[i]
                arr[i+1], arr[high] = arr[high], arr[i+1]
                return (i+1)
            
            def quick(arr, low, high):
                if len(arr) == 1:
                    return arr
                if low < high:
                    pi = partition(arr, low, high)
                    quick(arr, low, pi-1)
                    quick(arr, pi+1, high)
            lst=[]
            for i in allSongs: lst.append(i)
            quick(lst,0,len(allSongs)-1)
            top=lst[0:15]
            queryset = top
            return queryset
        
class PlaylistView(generics.ListAPIView):
    
    permission_classes = (IsAuthenticated,)
    serializer_class = PlaylistSerializer
    
    def createplaylist_view(request):
        if request.method == 'POST':
            playlist = PlaylistSerializer(data=request.data)
            if playlist.is_valid():
                playlist.save()
                return Response(status=status.HTTP_201_CREATED)
            print(playlist.user)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Playlist.objects.all()
            print("check", queryset)
            
            playlist_name = self.request.GET.get('name')
            user_id = self.request.GET.get('id')
            if user_id is not None:
                queryset = queryset.filter(user=user_id)
            if playlist_name is not None:
                queryset = queryset.filter(playlist_name=playlist_name)
            return queryset

class PlayNext(generics.ListAPIView):
    
    permission_classes = (IsAuthenticated,)
    serializer_class = SongsSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            obj = Songs.objects.all()
            r = random.randint(0, len(obj)-1)
            queryset = obj[r]
            return {queryset}

class NamePlaylist(generics.ListAPIView):
    
    permission_classes = (IsAuthenticated,)
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            lstAll = Playlist.objects.all()
            state_name = self.request.GET.get('user', None)
            if state_name is not None:
                lst=[]
                playlist = []
                for i in lstAll:
                    if str(i.user.id) == str(state_name):
                        if i.playlist_name not in lst:
                            playlist.append(i)
                            lst.append(i.playlist_name)
                queryset = playlist
            else : queryset = []
            return queryset
