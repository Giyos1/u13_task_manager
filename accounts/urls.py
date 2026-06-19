from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Login → access+refresh
    TokenRefreshView,  # Refresh → yangi access
    TokenBlacklistView,  # Logout → blacklist
)

router = DefaultRouter()
router.register('auth', views.AuthViewSet, basename='auth')
router.register('auth-with-token', views.AuthWithTokenViewSet, basename='auth-toke')
router.register('auth-jwt', views.AuthCustomJWTViewSet, basename='auth-jwt')

urlpatterns = [
                  path('login_jwt/', TokenObtainPairView.as_view(), name='jwt_login'),
                  path('refresh/', TokenRefreshView.as_view(), name='refresh'),
                  path('logout_jwt/', TokenBlacklistView.as_view(), name='logout')
              ] + router.urls

# 1 task login jwt -> cutomni create_tokens functionidan foydalanib
# 2 refresh -> refresh_access_token
