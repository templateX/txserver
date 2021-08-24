from django.urls import path
from .import views


urlpatterns = [
    path('', views.index, name='index'),
    path('connect/github/', views.github_connect, name='github_connect'),
    path('connect/github/callback/', views.github_connect_callback, name='github_connect_callback'),
    path('github/projects/<str:access_token>/', views.github_projects, name='github_projects'),
]
