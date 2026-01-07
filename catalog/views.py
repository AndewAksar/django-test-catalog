from rest_framework import generics
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Count

from catalog.models import (
    Product,
    ProductParameter
)
from catalog.filters import ProductFilter
from catalog.serializers import (
    ProductDetailSerializer,
    ProductListSerializer,
    ParameterFilterSerializer
)

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filterset_class = ProductFilter

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

class ParameterFilterListView(generics.ListAPIView):
    serializer_class = ParameterFilterSerializer

    def get_queryset(self):
        return (
            ProductParameter.objects.values('name').annotate(
                values=ArrayAgg('value', distinct=True),
                product_count=Count('product', distinct=True)
            ).order_by('name')
        )
