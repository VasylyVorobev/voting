from django.contrib import admin
from django.urls import path, include

from .yasg import urlpatterns as swagger_url

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
    path('polls/', include('polls.urls')),
]

urlpatterns += swagger_url
