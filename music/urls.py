from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.LandingView.as_view(), name="landing"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login_user"),

    path('album/all/', views.AlbumIndex.as_view(), name="album-index"),
    path('album/<int:pk>/', views.AlbumDetail.as_view(), name="album-detail"),
    path('album/add/', views.AlbumCreate.as_view(), name="album-add" ),
    path('album/<int:pk>/edit/', views.AlbumUpdate.as_view(), name="album-update" ),
    path('album/<int:pk>/delete/', views.AlbumDelete.as_view(), name="album-delete" ),

    path('album/<int:album_id>/add_song/', views.create_song, name="song-add" ),
    path('<int:song_id>/favorite/', views.favorite_song, name="favorite-song" ),
    path('songs/<filter_by>/', views.SongIndex.as_view(), name='song-index'),
    path('songs/<int:pk>/delete/', views.SongDelete.as_view(), name='song-delete'),


]
