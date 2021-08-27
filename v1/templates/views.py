from rest_framework import generics, permissions
from .serializers import TemplateSearchSerializer, TemplateSerializer, TemplateCreateSerializer
from .permissions import IsOwnerOrReadOnly
from templates.models import Template


class TemplateSearch(generics.ListAPIView):
    serializer_class = TemplateSearchSerializer
    queryset = Template.objects.all()

    def get_queryset(self):
        queryset = Template.objects.all()
        if 'tag' in self.request.query_params:
            tags = self.request.query_params['tag'].split(',')
            for tag in tags:
                queryset = queryset.filter(tags__name=tag)
        return queryset


class TemplateCreate(generics.CreateAPIView):
    serializer_class = TemplateCreateSerializer
    queryset = Template.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TemplateSerializer
    queryset = Template.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
