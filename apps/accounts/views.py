from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics

from django.contrib.auth import get_user_model

from apps.accounts.serializers import UserSerializer, RegistrationSerializer
from apps.accounts.mixins import AddFavoriteMixin,RemoveFavoriteMixin


User = get_user_model()

class UserModelViewSet(ReadOnlyModelViewSet,AddFavoriteMixin,RemoveFavoriteMixin):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
