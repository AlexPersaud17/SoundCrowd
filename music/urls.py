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
]
