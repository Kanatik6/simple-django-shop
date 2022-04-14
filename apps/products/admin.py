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
        'user',
        'status',
    )
    list_filter = [
        ('status',admin.ChoicesFieldListFilter),
        ]
    search_fields = ['price']
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # You need to define a character for splitting your range, in this example I'll use a hyphen (-)
        try:
            # This will get me the range values if there's only 1 hyphen
            print(search_term)
            min_price, max_price = search_term.split('-')
        except ValueError:
            # Otherwise it will do nothing
            pass
        else:
            # If the try was successful, it will proceed to do the range filtering
            queryset |= self.model.objects.filter(price__gte=min_price, price__lte=max_price)
        return queryset, use_distinct



admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Cart)
admin.site.register(Order,OrderAdmin)
admin.site.register(Image)
