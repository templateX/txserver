from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RepoSerializer, TemplateSerializer, TemplateTagSerializer
from .permissions import IsOwner, IsOwnerOrReadOnly
from templates.models import Template, Repo, TemplateTag, Like
from api.v1.response import Success, SuccessCreate, SuccessDelete, InvalidPermission
from .mixins import TemplateAuthLookUpMixin, TagLookUpMixin, TemplateLookUpMixin, LikeLookupMixix


class TemplateSearch(generics.ListAPIView):
    serializer_class = TemplateSerializer
    queryset = Template.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'q' in self.request.query_params:
            query = self.request.query_params['q']
            queryset = queryset.filter(Q(title__contains=query) | Q(slug__contains=query))
        return queryset


# creates and lists templates
class TemplateCreate(generics.CreateAPIView):
    serializer_class = TemplateSerializer
    queryset = Template.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Template.objects.all()

    def perform_create(self, serializer):
        # assigned authenticated user to the template
        serializer.save(user=self.request.user)


class TemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TemplateSerializer
    queryset = Template.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)


class TemplateRepoList(TemplateAuthLookUpMixin, generics.ListCreateAPIView):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        template = self.get_template()
        return serializer.save(template=template)


class TemplateRepoDetail(TemplateAuthLookUpMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        repo = super().get_object()
        template = self.get_template()

        if not repo.template == template:
            raise InvalidPermission

        return repo


class TemplateTagList(TemplateAuthLookUpMixin, generics.ListAPIView):
    queryset = TemplateTag.objects.all()
    serializer_class = TemplateTagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        template = self.get_template()
        tags = TemplateTag.objects.filter(template=template, user=self.request.user)
        return tags


class TemplateTagListCreate(TemplateAuthLookUpMixin, TagLookUpMixin, generics.CreateAPIView):
    queryset = TemplateTag.objects.all()
    serializer_class = TemplateTagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        template = self.get_template()
        tag = self.get_tag()
        template_tag = TemplateTag.objects.create(template=template, tag=tag)
        serializer = TemplateTagSerializer(template_tag)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TemplateTagDetail(TemplateAuthLookUpMixin, generics.RetrieveDestroyAPIView):
    queryset = TemplateTag.objects.all()
    serializer_class = TemplateTagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        instance = super().get_object()
        template = self.get_template()

        if not instance.template == template:
            raise InvalidPermission

        return instance


class TemplateLike(TemplateLookUpMixin, LikeLookupMixix, APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        template = self.get_template()
        like = self.get_like(request.user, template)
        if like is not None:
            raise Success
        Like.objects.create(template=template, user=request.user)
        raise SuccessCreate

    def delete(self, request, *args, **kwargs):
        template = self.get_template()
        like = self.get_like(request.user, template)
        if like is not None:
            like.delete()
            raise SuccessDelete
        raise Success


# class TemplateBookmark(TemplateLookUpMixin, APIView):
#     pass