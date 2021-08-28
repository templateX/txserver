from rest_framework import generics
from rest_framework import permissions
from .serializers import UserSerializer
from accounts.models import User
from api.v1.response import SuccessCreate, SuccessDelete


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserFollow(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.followers.add(request.user)
        raise SuccessCreate


class UserUnfollow(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.followers.remove(request.user)
        raise SuccessDelete
