from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RepoSerializer, TemplateSerializer
# from .serializers import TemplateSearchSerializer, TemplateSerializer, TemplateCreateSerializer, RepoSerializer
from .permissions import IsOwner, IsOwnerOrReadOnly
from .exceptions import TemplateUnavailable, TagUnavailable, RepoUnavailable, InvalidData
from templates.models import Template, Tag, Repo
from api.v1.response import Success, SuccessCreate, SuccessUpdate, SuccessDelete, InvalidPermission
from .mixins import TemplateLookUpMixin


class TemplateList(generics.ListCreateAPIView):
    serializer_class = TemplateSerializer
    queryset = Template.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TemplateSerializer
    queryset = Template.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)


class TemplateRepoList(TemplateLookUpMixin, generics.ListCreateAPIView):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        template = self.get_template()
        return serializer.save(template=template)


class TemplateRepoDetail(TemplateLookUpMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        repo = super().get_object()
        template = self.get_template()

        if not repo.template == template:
            raise InvalidPermission

        return repo

# class LikeView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)

#     def get(self, request, pk):
#         try:
#             template = Template.objects.get(pk=pk)
#             template.likes.add(request.user)
#             raise Success
#         except Template.DoesNotExist:
#             raise TemplateUnavailable


# class LikeRemoveView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)

#     def get(self, request, pk):
#         try:
#             template = Template.objects.get(pk=pk)
#             template.likes.remove(request.user)
#             raise Success
#         except Template.DoesNotExist:
#             raise TemplateUnavailable


# class TemplateTag(APIView):
#     permission_classes = (permissions.IsAuthenticated, IsOwner)

#     def get_object(self, pk):
#         try:
#             template = Template.objects.get(pk=pk)
#             return template
#         except Template.DoesNotExist:
#             raise TemplateUnavailable

#     def get_tag(self, tag_id):
#         try:
#             tag = Tag.objects.get(pk=tag_id)
#             return tag
#         except Tag.DoesNotExist:
#             raise TagUnavailable

#     def get(self, request, pk):
#         template = self.get_object(pk)
#         self.check_object_permissions(self.request, template)
#         tag = self.get_tag(request.query_params['tag_id'])
#         template.tags.add(tag)
#         raise Success

#     def delete(self, request, pk):
#         template = self.get_object(pk)
#         self.check_object_permissions(request, template)
#         tag = self.get_tag(request.query_params['tag_id'])
#         template.tags.remove(tag)
#         raise Success


# class TemplateRepo(APIView):
#     permission_classes = (permissions.IsAuthenticated, IsOwner)

#     def get_object(self, pk):
#         try:
#             template = Template.objects.get(pk=pk)
#             return template
#         except Template.DoesNotExist:
#             raise TemplateUnavailable

#     def get_repo(self, repo_id):
#         try:
#             repo = Repo.objects.get(pk=repo_id)
#             return repo
#         except Tag.DoesNotExist:
#             raise RepoUnavailable

#     def post(self, request, pk):
#         template = self.get_object(pk)
#         self.check_object_permissions(request, template)
#         serializer = RepoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(template=template)
#         else:
#             raise InvalidData
#         raise SuccessCreate

#     def delete(self, request, pk):
#         template = self.get_object(pk)
#         self.check_object_permissions(request, template)
#         repo = self.get_repo(request.query_params['repo_id'])
#         if not repo.template == template:
#             raise InvalidPermission
#         repo.delete()
#         raise SuccessDelete
