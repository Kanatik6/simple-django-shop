from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from django.contrib.auth import get_user_model

from apps.accounts.serializers import UserSerializer, RegistrationSerializer
from apps.accounts.mixins import AddFavoriteMixin,RemoveFavoriteMixin,GetCurrentUserMixin


User = get_user_model()

class UserModelViewSet(
    GenericViewSet,
    AddFavoriteMixin,
    RemoveFavoriteMixin,
    GetCurrentUserMixin
    ):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]



class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
