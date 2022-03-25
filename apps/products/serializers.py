from rest_framework import serializers

from apps.products.models import CartProduct, Product, Cart,Category,Order


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            'category',
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
            'final_price',
        )


class CartSerializer(serializers.ModelSerializer):
    cart_products = ProductInSerializer(many=True,read_only=True)

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
            'id',
            'product',
            'amount',
            'cart',
            'final_price',
            'price',
            'title',
        )
        read_only_fields = ['cart','price','final_price','title']


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'descriptions',
        )


class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = (
            'id',
            'name',
            'number',
            'address',
            'descriptions',
            'status',
            'price',
        )
        read_only_fields = ['price']
