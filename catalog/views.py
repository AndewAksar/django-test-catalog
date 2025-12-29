from rest_framework import generics

from catalog.models import Product
from catalog.serializers import (
    ProductDetailSerializer,
    ProductListSerializer,
)

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
