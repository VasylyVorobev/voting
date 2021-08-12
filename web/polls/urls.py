from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'polls'

router = DefaultRouter()

urlpatterns = [
    path('create/', views.CreatePollsView.as_view({'post': 'create'}), name='create_polls'),

]

urlpatterns += router.urls
