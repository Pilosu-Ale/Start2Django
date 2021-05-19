from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('posts/', views.posts),
    path('new_post/', views.newPost),
    path('utente/<int:pk>/', views.userPage, name="userPage")
]