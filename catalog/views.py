import logging
from rest_framework import generics
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Count

from catalog.models import (
    Product,
    ProductParameter,
    ProductImage,
    )
from catalog.filters import ProductFilter
from catalog.serializers import (
    ProductDetailSerializer,
    ProductListSerializer,
    ParameterFilterSerializer,
    ProductImageSerializer,
    ProductParameterSerializer,
)

logger = logging.getLogger(__name__)

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
        user_id = getattr(self.request.user, "id", None)

        try:
            return (
                ProductParameter.objects.values('name').annotate(
                    values=ArrayAgg('value', distinct=True),
                    product_count=Count('product', distinct=True)
                ).order_by('name')
            )
        except Exception:
            logger.exception(
                'Parameter filter aggregation failed unexpectedly',
                extra={
                    "action": "parameter_filter_list",
                    "user_id": user_id,
                }
            )
            raise

class ProductImageListView(generics.ListAPIView):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        user_id = getattr(self.request.user, "id", None)

        try:
            if not Product.objects.filter(id=product_id).exists():
                raise NotFound('Product not found')
            return ProductImage.objects.filter(product_id=product_id)
        except NotFound:
            raise
        except Exception:
            logger.exception(
                'Product image list failed unexpectedly',
                extra={
                    "action": "product_image_list",
                    "user_id": user_id,
                    "product_id": product_id,
                }
            )

class ProductParameterListView(generics.ListAPIView):
    serializer_class = ProductParameterSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        user_id = getattr(self.request.user, "id", None)

        try:
            return ProductParameter.objects.filter(product_id=self.kwargs['product_id'])
        except Exception:
            logger.exeption(
                'Product parameter list failed unexpectedly',
                extra={
                    "action": "product_parameter_list",
                    "user_id": user_id,
                    "product_id": product_id,
                }
            )
            raise
