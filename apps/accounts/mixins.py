from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from apps.accounts.serializers import FavoriteIDSerializer

class AddFavoriteMixin:
    @action(methods=['post'],detail=False,serializer_class=FavoriteIDSerializer)
    def add_favorite(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.favorites.add(serializer.data['product_id'])
        user.save()
        return Response({'message':'added'})


class RemoveFavoriteMixin:
    @action(methods=['post'],detail=False,serializer_class=FavoriteIDSerializer)
    def remove_favorite(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.favorites.remove(serializer.data['id'])
        user.save()
        return Response({'message':'removed'})


class GetCurrentUserMixin:
    @action(methods=['get',],detail=False)
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
