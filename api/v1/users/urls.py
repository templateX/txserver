from django.urls import path
from .import views

urlpatterns = [
    # path('followers/', views.Followers.as_view(), name='user-followers'),
    # path('followings/', views.Followings.as_view(), name='user-followings'),
    path('<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('<int:pk>/follow/', views.UserFollow.as_view(), name='user-follow'),
    path('<int:pk>/unfollow/', views.UserUnfollow.as_view(), name='user-unfollow'),
]
