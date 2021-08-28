from django.urls import path, include

urlpatterns = [
    path('templates/', include('api.v1.templates.urls')),
    path('users/', include('api.v1.users.urls'))
]
