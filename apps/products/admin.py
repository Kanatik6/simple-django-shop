from django.contrib import admin

from apps.products.models import (
    Product,
    Category,
    Cart,
    Image,
    Order
)

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'amount',
        'price',
        'category',
        )
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'descriptions'
    )


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'address',
        'descriptions',
        'price',
        'user'
    )


admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Cart)
admin.site.register(Order,OrderAdmin)
admin.site.register(Image)
