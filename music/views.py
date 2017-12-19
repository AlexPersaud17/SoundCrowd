from django.shortcuts import render
from django.http import Http404
from .models import Album


# Create your views here.
def index(request):
  all_albums = Album.objects.all()
  return render(request, 'music/index.html', {'all_albums': all_albums})


def detail(request, album_id):
  try:
    album = Album.objects.get(id=album_id)
  
  except Album.DoesNotExist:
    raise Http404("Album does not exist.")

  return render(request, 'music/detail.html', {'album': album})
