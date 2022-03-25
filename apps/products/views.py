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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data["product"]
        if serializer.validated_data["amount"] > product.amount:
            return Response(
                {"message": "items in stock fewer  than you want to buy"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        product.amount -= serializer.validated_data["amount"]
        product.save()

        self.perform_create(serializer=serializer)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        cart = Cart.objects.filter(user=self.request.user.id).first()
        serializer.save(cart=cart)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        cart = Cart.objects.filter(user=user.id).first()
        cart_products = cart.cart_products.all()
        if cart_products.first() == None:
            return Response({"message": "your cart is empty, fill her and try again"})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        order = Order.objects.create(
            name=data.get("name"),
            number=data.get("number"),
            address=data.get("address"),
            descriptions=data.get("descriptions"),
            price=cart.total_price,
            user=user,
        )
        serializer = self.get_serializer(order)
        cart.cart_products.all().delete()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
