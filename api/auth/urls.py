from django.urls import path
from .import views

urlpatterns = [
    path('github/login/callback/', views.github_callback, name='github_callback')
]
