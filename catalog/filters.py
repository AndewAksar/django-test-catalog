from gjango_filters import rest_framework as filters

from catalog.models import Product

class ProductFilter(filters.FilterSet):
    param_name = filters.CharFilter(
        field_name='parameters__name',
        lookup_expr='iexact',
    )
    param_value = filters.CharFilter(
        field_name='parameters__value',
        lookup_expr='iexact',
    )

    class Meta:
        model = Product
        fields = [
            'param_name',
            'param_value',
        ]
        distinct = True
