from django_filters import rest_framework as filters
from django_filters import FilterSet

from apps.products.models import Category


class ProductFilterSet(FilterSet):
    price_from = filters.NumberFilter(field_name='price',lookup_expr='lt')
    price_to = filters.NumberFilter(field_name='price',lookup_expr='gt')
    categorys = filters.ModelMultipleChoiceFilter(
        # этот параметр означает по какому полю будут фильтроваться, возможно тут можно использовать лукапы
        field_name='category__id',
        # этот параметр означает какое поле будет использоваться для фильтра
        to_field_name='id',
        queryset=Category.objects.all(),
    )
    amount_from = filters.NumberFilter(field_name='amount',lookup_expr='lt')
    amount_to = filters.NumberFilter(field_name='amount',lookup_expr='gt')
