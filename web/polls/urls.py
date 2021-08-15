from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'polls'

router = DefaultRouter()

urlpatterns = [
    path('create/', views.PollsViewSet.as_view({'post': 'create'}), name='create_polls'),
    path('list/', views.PollsViewSet.as_view({'get': 'list'}), name='list_polls'),
    path('<pk>/', views.PollsViewSet.as_view({'get': 'retrieve'}), name='detail_polls'),
    path('update/<pk>/', views.PollsViewSet.as_view({'put': 'update'}), name='update_polls'),
    path('delete/<pk>/', views.PollsViewSet.as_view({'delete': 'destroy'}), name='delete_polls'),

]

urlpatterns += router.urls
