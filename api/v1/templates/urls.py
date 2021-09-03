from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.TemplateSearch.as_view(), name='template-search'),
    path('', views.TemplateCreate.as_view(), name='template-create'),
    path('<uuid:pk>/', views.TemplateDetail.as_view(), name='template-detail'),
    path('<uuid:template_id>/like/', views.TemplateLike.as_view(), name='template-like'),
    path('<uuid:template_id>/repos/', views.TemplateRepoList.as_view(), name='template-repo-list'),
    path('<uuid:template_id>/repos/<uuid:pk>/', views.TemplateRepoDetail.as_view(), name='template-repo-detail'),
    path('<uuid:template_id>/tags/', views.TemplateTagList.as_view(), name='template-tags-list'),
    path('<uuid:template_id>/tags/<uuid:tag_id>/', views.TemplateTagListCreate.as_view(), name='template-tags-list-create'),
    path('<uuid:template_id>/tags/<uuid:pk>/', views.TemplateTagDetail.as_view(), name='template-tags-detail'),
]
