from django.urls import path

from catalog.views import ProductDetailView, ProductListView, ParameterFilterListView

app_name = 'catalog'

urlpatterns = [
    path("catalog/products/", ProductListView.as_view(), name="product-list"),
    path("catalog/products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("catalog/parameters/", ParameterFilterListView.as_view(), name="parameter-filter"),
]
