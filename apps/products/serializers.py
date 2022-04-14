from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from apps.products.models import CartProduct, Product, Cart, Category, Order


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "category",
            "descriptions",
            "amount",
            "price",
        )


class ProductInSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartProduct
        fields = (
            "id",
            "title",
            "amount",
            "price",
            "final_price",
        )


class CartSerializer(serializers.ModelSerializer):
    cart_products = ProductInSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = (
            "id",
            "total_price",
            "cart_products",
        )


class CartProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartProduct
        fields = (
            "id",
            "product",
            "amount",
            "cart",
            "final_price",
            "price",
            "title",
        )
        read_only_fields = ["cart", "price", "final_price", "title"]

    def create(self, validated_data):
        cart = Cart.objects.filter(user=self.context["request"].user.id).first()
        product = validated_data["product"]

        if validated_data["amount"] > product.amount:
            raise ValidationError(detail="items in stock fewer  than you want to buy")

        product.amount -= validated_data["amount"]
        product.save()

        CartProduct = self.Meta.model
        instance = CartProduct.objects.filter(product=product,cart=cart).first()

        if not instance:
            instance = CartProduct._default_manager.create(cart=cart, **validated_data)

        return instance


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "id",
            "title",
            "descriptions",
        )


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            "id",
            "name",
            "number",
            "address",
            "descriptions",
            "status",
            "price",
        )
        read_only_fields = ["price"]

    def create(self, validated_data):
        user = self.context["request"].user
        cart = Cart.objects.filter(user=user.id).first()
        cart_products = cart.cart_products.all()

        if cart_products.first() == None:
            raise ValidationError(detail="your cart is empty, fill her and try again")

        instance = self.Meta.model._default_manager.create(
            price=cart.total_price, user=user, **validated_data
        )
        cart_products.delete()
        return instance
