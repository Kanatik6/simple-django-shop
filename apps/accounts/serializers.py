from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.products.serializers import ProductSerializer, CartSerializer

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password', ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    favorites = ProductSerializer(many=True)
    cart = CartSerializer()

    class Meta:
        model = User
        fields = ['id', 'username','favorites','cart']


class FavoriteIDSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
