from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.TemplateSearch.as_view(), name='template-search'),
    path('', views.TemplateCreate.as_view(), name='template-create'),
    path('<int:pk>/', views.TemplateDetail.as_view(), name='template-detail'),
    path('<int:template_id>/like/', views.TemplateLike.as_view(), name='template-like'),
    path('<int:template_id>/repos/', views.TemplateRepoList.as_view(), name='template-repo-list'),
    path('<int:template_id>/repos/<int:pk>/', views.TemplateRepoDetail.as_view(), name='template-repo-detail'),
    path('<int:template_id>/tags/', views.TemplateTagList.as_view(), name='template-tags-list'),
    path('<int:template_id>/tags/<int:tag_id>/', views.TemplateTagListCreate.as_view(), name='template-tags-list-create'),
    path('<int:template_id>/tags/<int:pk>/', views.TemplateTagDetail.as_view(), name='template-tags-detail'),
]
