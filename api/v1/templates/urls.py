from django.urls import path
from . import views

urlpatterns = [
    # path('search/', views.TemplateSearch.as_view(), name='template_search'),
    path('', views.TemplateCreate.as_view(), name='template_create'),
    path('<int:pk>/', views.TemplateDetail.as_view(), name='template_detail'),
    # path('<int:pk>/tags/', views.TemplateTag.as_view(), name='template_tags'),
    # path('<int:pk>/repos/', views.TemplateRepo.as_view(), name='template_repos'),
    # path('<int:pk>/like/', views.LikeView.as_view(), name='template_like'),
    # path('<int:pk>/like/remove/', views.LikeRemoveView.as_view(), name='template_like_remove'),
]
