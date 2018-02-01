from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SongForm, UserForm
from .models import Album, Song
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import JsonResponse


AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

class LandingView(View):
  template_name = 'music/landing.html'
  def get(self, request):
    return render(request, self.template_name)
  
class AlbumIndex(LoginRequiredMixin, generic.ListView):
  login_url = '/music/login/'
  redirect_field_name = 'redirect_to'
  template_name = 'music/index.html'
  context_object_name = 'all_albums'

  def get_queryset(self):
    return Album.objects.all()

class AlbumDetail(LoginRequiredMixin, generic.DetailView):
  login_url = '/music/login/'
  redirect_field_name = 'redirect_to'
  model = Album
  template_name = 'music/detail.html'

class AlbumCreate(LoginRequiredMixin, CreateView):
  login_url = '/music/login/'
  redirect_field_name = 'redirect_to'
  model = Album
  fields = ["artist", "album_title", "genre", "album_logo"]

class AlbumUpdate(LoginRequiredMixin, UpdateView):
  login_url = '/music/login/'
  redirect_field_name = 'redirect_to'
  model = Album
  fields = ["artist", "album_title", "genre", "album_logo"]


class AlbumDelete(LoginRequiredMixin, DeleteView):
  login_url = '/music/login/'
  redirect_field_name = 'redirect_to'
  model = Album
  success_url = reverse_lazy("music:album-index")


class LogoutView(View):
  def get(self, request):
    logout(request)
    form = UserForm(request.POST or None)
    return render(request, 'music/login.html', {"form": form})


class LoginView(View):
  def get(self, request):
    return render(request, 'music/login_form.html')

  def post(self, request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        # albums = Album.objects.filter(user=request.user)
        # return render(request, 'music/index.html', {'albums': albums})
        return render(request, 'music/index.html')

      else:
        return render(request, 'music/login_form.html', {'error_message': 'Your account has been disabled'})
    else:
      return render(request, 'music/login_form.html', {'error_message': 'Invalid login'})


class RegisterView(View):
  form_class = UserForm
  template_name = 'music/registration_form.html'

  def get(self, request):
    form = self.form_class(None)
    return render(request, self.template_name, {'form': form})

  def post(self, request):
    form = self.form_class(request.POST)

    if form.is_valid():
      user = form.save(commit=False)
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user.set_password(password)
      user.save()
      user = authenticate(username=username, password=password)

      if user is not None:
        if user.is_active:
          login(request, user)
          # albums = Album.objects.filter(user=request.user)
          # return render(request, 'music/index.html', {'albums': albums})
          return render(request, 'music/index.html')          

    return render(request, self.template_name, {'form': form})



def create_song(request, album_id):
	form = SongForm(request.POST or None, request.FILES or None)
	album = get_object_or_404(Album, pk=album_id)

	if form.is_valid():
		albums_songs = album.song_set.all()
		for s in albums_songs:
			if s.song_title == form.cleaned_data.get("song_title"):
				context = {
					'album': album,
					'form': form,
					'error_message': 'You already added that song',
				}
				return render(request, 'music/create_song.html', context)

		song = form.save(commit=False)
		song.album = album
		song.audio_file = request.FILES['audio_file']
		file_type = song.audio_file.url.split('.')[-1]
		file_type = file_type.lower()
		if file_type not in AUDIO_FILE_TYPES:
			context = {
				'album': album,
				'form': form,
				'error_message': 'Audio file must be WAV, MP3, or OGG',
			}
			return render(request, 'music/create_song.html', context)

		song.save()
		return render(request, 'music/detail.html', {'album': album})
	context = {
		'album': album,
		'form': form,
	}
	return render(request, 'music/create_song.html', context)

def favorite_song(request, song_id):
  song = get_object_or_404(Song, pk=song_id)
  try:
    if song.is_favorite:
      song.is_favorite = False
    else:
      song.is_favorite = True
    song.save()
  except (KeyError, Song.DoesNotExist):
    return JsonResponse({'success': False})
  else:
    return render(request, 'music/detail.html', {'album': song.album})

# def songs(request, filter_by):
#   if not request.user.is_authenticated():
#     return render(request, 'music/login.html')
#   else:
#     try:
#       song_ids = []
#       for album in Album.objects.filter(user=request.user):
#         for song in album.song_set.all():
#           song_ids.append(song.pk)
#           users_songs = Song.objects.filter(pk__in=song_ids)
#       if filter_by == 'favorites':
#         users_songs = users_songs.filter(is_favorite=True)
#     except Album.DoesNotExist:
#       users_songs = []
#     return render(request, 'music/songs.html', {
#       'song_list': users_songs,
# 			'filter_by': filter_by,
# 		})


class SongIndex(LoginRequiredMixin, generic.ListView):
  login_url = '/music/login/'
  redirect_field_name = 'redirect_to'
  template_name = 'music/songs.html'
  context_object_name = 'song_list'

  def get_queryset(self):
    return Song.objects.all()