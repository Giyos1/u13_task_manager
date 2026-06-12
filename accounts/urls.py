from rest_framework.routers import DefaultRouter

from accounts import views

router = DefaultRouter()
router.register('auth', views.AuthViewSet, basename='auth')
router.register('auth-with-token', views.AuthWithTokenViewSet, basename='auth-toke')

urlpatterns = router.urls
