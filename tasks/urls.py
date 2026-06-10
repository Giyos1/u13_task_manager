from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('tasks', views.TaskModelViewSet, basename='tasks')

urlpatterns = [
                  # path('', views.salom, name='salom'),
                  path('projects/', views.ProjectAPIView.as_view(), name='project_list'),
                  path('projects/<int:pk>/', views.ProjectAPIView.as_view(), name='project_detail'),
                  path('projects/<int:pk>/task/list/', views.ProjectDetailTaskAPIView.as_view(), name='task_list'),
                  # path('tasks/', views.TaskAPIView.as_view(), name='task'),
                  # path('tasks/<int:pk>/', views.TaskDetailAPIView.as_view(), name='task_detail'),
              ] + router.urls
