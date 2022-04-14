from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)
from rest_framework.routers import SimpleRouter

from django.urls import path

from apps.accounts.views import RegistrationAPIView, UserModelViewSet

router = SimpleRouter()

router.register('users',UserModelViewSet,'users')


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token_refresh/', TokenRefreshView.as_view()),
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
]

urlpatterns +=router.urls