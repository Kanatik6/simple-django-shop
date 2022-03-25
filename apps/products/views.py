from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, status

from apps.products.models import (
    CartProduct, 
    Category,
    Product, 
    Order, 
    Cart)
from apps.products.serializers import (
    CartProductSerializer,
    OrderSerializer,
    ProductSerializer,
    CartSerializer,
    CategorySerializer,
)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartReadView(
    GenericViewSet
):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    @action(methods=['get',],detail=False)
    def me(self, request, *args, **kwargs):
        cart = self.get_queryset().filter(user=self.request.user.id).first()
        serializer = self.get_serializer(cart)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class CartProductView(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
