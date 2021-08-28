from django.http import Http404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from accounts.models import User
from .permissions import IsOwnerOrReadOnly
from .serializers import AccountSerializer
from .exceptions import ExistingAccount, InvalidCredentials


class Register(generics.CreateAPIView):
    serializer_class = AccountSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        access_token = AccessToken.for_user(user)
        headers = self.get_success_headers(serializer.data)
        data = {
            'user': serializer.data,
            'access_token': str(access_token),
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class Login(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                access_token = str(AccessToken.for_user(user))
                return Response({'access_token': access_token})
            else:
                raise InvalidCredentials
        except User.DoesNotExist:
            raise Http404


class Profile(generics.RetrieveUpdateAPIView):
    serializer_class = AccountSerializer
    queryset = User.objects.all()
    permissions = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class Me(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        instance = request.user
        serializer = AccountSerializer(instance)
        return Response(serializer.data)
