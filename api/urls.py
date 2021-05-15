from django.urls import path
from . import views

urlpatterns = [
    path('posts', views.posts),
    path('new_post', views.newPost),
]