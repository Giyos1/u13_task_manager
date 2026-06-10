from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts import views

router = DefaultRouter()
router.register('auth', views.AuthViewSet, basename='auth')

urlpatterns = router.urls
