from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.TemplateSearch.as_view(), name='template_search'),
    path('', views.TemplateCreate.as_view(), name='template_create'),
    path('<int:pk>/', views.TemplateDetail.as_view(), name='template_detail')
]
