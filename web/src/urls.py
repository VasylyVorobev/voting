from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
    path('polls/', include('polls.urls')),
]
