from django.urls import path
from . import views

urlpatterns = [
    path("registration/", views.registration_view),
    path('posts', views.posts),
    path('new_post', views.newPost),
]