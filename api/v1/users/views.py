from rest_framework import generics
from rest_framework import permissions
from .serializers import UserSerializer, FollowSerializer
from accounts.models import User
from follows.models import Follow
from api.v1.response import Success, SuccessCreate, SuccessDelete


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserFollow(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            follow = Follow.objects.get(user=instance, follower=request.user)
            raise Success
        except Follow.DoesNotExist:
            Follow.objects.create(user=instance, follower=request.user)
            raise SuccessCreate


class UserUnfollow(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            follow = Follow.objects.get(user=instance, follower=request.user)
            follow.delete()
            raise SuccessDelete
        except Follow.DoesNotExist:
            raise Success


class FollowerView(generics.ListAPIView):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        follows = Follow.objects.filter(user=self.request.user)
        print(follows)
        return follows


class FollowingView(generics.ListAPIView):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        follows = Follow.objects.filter(follower=self.request.user)
        print(follows)
        return follows
