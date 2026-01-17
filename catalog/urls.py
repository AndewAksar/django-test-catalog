from django.urls import path

from catalog.views import (
    ProductDetailView,
    ProductListView,
    ParameterFilterListView,
    ProductImageListView,
    ProductParameterListView
)

app_name = 'catalog'

urlpatterns = [
    path("catalog/products/", ProductListView.as_view(), name="product-list"),
    path("catalog/products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("catalog/parameters/", ParameterFilterListView.as_view(), name="parameter-filter"),
    path("catalog/products/<int:product_id>/image/", ProductImageListView.as_view()),
    path("catalog/products/<int:product_id>/parameter/", ProductParameterListView.as_view()),
]
