from django.urls import path
from .import views

urlpatterns = [
    path('<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('<int:pk>/follow/', views.UserFollow.as_view(), name='user-follow'),
    path('<int:pk>/unfollow/', views.UserUnfollow.as_view(), name='user-unfollow'),
]
