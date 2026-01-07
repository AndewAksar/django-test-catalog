from rest_framework import serializers

from catalog.models import Product, ProductParameter, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image', 'caption', 'sort_order']
        read_only_fields = ['id', 'product']

class ProductParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductParameter
        fields = ['id', 'product', 'name', 'value', 'price', 'sort_order']
        read_only_fields = ['id', 'product']

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "base_price", "sort_order"]

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'base_price',
            'sort_order',
            'description',
            'images',
            'parameters'
        ]

class ParameterFilterSerializer(serializers.Serializer):
    name = serializers.CharField()
    values = serializers.ListField(child=serializers.CharField())
    product_count = serializers.IntegerField()
