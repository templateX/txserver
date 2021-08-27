from django.urls import path, include

urlpatterns = [
    path('templates/', include('v1.templates.urls')),
    path('users/', include('v1.users.urls'))
]
