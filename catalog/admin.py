from django.contrib import admin

from catalog.models import Product, ProductImage, ProductParameter

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    ordering = ('sort_order',)

class ProductParameterInline(admin.TabularInline):
    model = ProductParameter
    extra = 0
    ordering = ('sort_order',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'base_price', 'sort_order')
    search_fields = (
        'name',
        'description',
        'images__caption',
        'parameters__name',
        'parameters__value',
    )
    ordering = ('sort_order', 'name')
    inlines = [ProductImageInline, ProductParameterInline]
