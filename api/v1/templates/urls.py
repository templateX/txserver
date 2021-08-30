from django.urls import path
from . import views

urlpatterns = [
    # path('search/', views.TemplateSearch.as_view(), name='template_search'),
    path('', views.TemplateList.as_view(), name='template-list'),
    path('<int:pk>/', views.TemplateDetail.as_view(), name='template-detail'),
    path('<int:template_id>/repos/', views.TemplateRepoList.as_view(), name='template-repo-list'),
    path('<int:template_id>/repos/<int:pk>/', views.TemplateRepoDetail.as_view(), name='template-repo-detail')
    # path('<int:pk>/tags/', views.TemplateTag.as_view(), name='template_tags'),
    # path('<int:pk>/like/', views.LikeView.as_view(), name='template_like'),
    # path('<int:pk>/like/remove/', views.LikeRemoveView.as_view(), name='template_like_remove'),
]
