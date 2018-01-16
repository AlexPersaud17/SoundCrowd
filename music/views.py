from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from .models import Album
from .forms import UserForm
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, generic.ListView):
  login_url = 'login/'
  redirect_field_name = 'redirect_to'
  template_name = 'music/index.html'
  context_object_name = 'all_albums'

  def get_queryset(self):
    return Album.objects.all()

class AlbumDetail(LoginRequiredMixin, generic.DetailView):
  login_url = 'login/'
  redirect_field_name = 'redirect_to'
  model = Album
  template_name = 'music/detail.html'

class AlbumCreate(LoginRequiredMixin, CreateView):
  login_url = 'login/'
  redirect_field_name = 'redirect_to'
  model = Album
  fields = ["artist", "album_title", "genre", "album_logo"]

class AlbumUpdate(LoginRequiredMixin, UpdateView):
  login_url = 'login/'
  redirect_field_name = 'redirect_to'
  model = Album
  fields = ["artist", "album_title", "genre", "album_logo"]


class AlbumDelete(LoginRequiredMixin, DeleteView):
  login_url = 'login/'
  redirect_field_name = 'redirect_to'
  model = Album
  success_url = reverse_lazy("music:index")


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
