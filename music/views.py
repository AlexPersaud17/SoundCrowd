from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
  return HttpResponse("This is the music homepage.")

def detail(request, album_id):
  return HttpResponse("This album number is " + str(album_id))
