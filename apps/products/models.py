from django.db import models
from django.contrib.auth import get_user_model

import itertools


class Product(models.Model):
    title = models.CharField(max_length=255)
    descriptions = models.CharField(max_length=600)
    amount = models.IntegerField(default=1)
    price = models.IntegerField(default=1)
    created_at = models.DateField(auto_now_add=True)

    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="products"
    )
    users = models.ManyToManyField(get_user_model(), related_name="favorites")


    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to="images")

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )


class Cart(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="cart"
    )
    products = models.ManyToManyField(
        Product, through="CartProduct", related_name="cart"
    )

    @property
    def total_price(self):
        prices = self.cart_products.annotate(
            last_price=models.F("product__price") * models.F("amount")
        ).values_list("last_price")
        return sum(itertools.chain(*prices))

    def __str__(self):
        return f"{self.user.username} - {self.total_price}"


class CartProduct(models.Model):
    amount = models.IntegerField(default=1)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_products"
    )
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cart_products"
    )

    @property
    def final_price(self):
        return self.product.price * self.amount

    @property
    def price(self):
        return self.product.price

    @property
    def title(self):
        return self.product.title

    def __str__(self):
        return f"{self.amount} {self.final_price}"


class Category(models.Model):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=500)

    def __str__(self):
        return self.title


class Order(models.Model):
    class StatusChoice(models.TextChoices):
        ORDER = 'order'
        ACCEPTED = 'accepted'
        FINISHED = 'finished'
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=13)
    address = models.CharField(max_length=100)
    descriptions = models.CharField(max_length=255, null=True)
    price = models.PositiveIntegerField()
    status = models.CharField(max_length=15,choices=StatusChoice.choices,default=StatusChoice.ORDER)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="orders")
