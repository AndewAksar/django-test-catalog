from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from catalog.admin import (
    ProductImageInline,
    ProductParameterInline
)
from catalog.models import (
    Product,
    ProductImage,
    ProductParameter
)
from catalog.filters import ProductFilter

class ProductAdminConfigTests(TestCase):
    def test_product_admin_registration_and_configuration(self):
        product_admin = admin.site._registry.get(Product)

        self.assertIsNotNone(product_admin)
        self.assertEqual(product_admin.list_display, ('id', 'name', 'base_price', 'sort_order'))
        self.assertEqual(
            product_admin.search_fields,
            (
                'name',
                'description',
                'images__caption',
                'parameters__name',
                'parameters__value',
            )
        )
        self.assertEqual(product_admin.ordering, ('sort_order', 'name'))
        self.assertEqual(product_admin.inlines, (ProductImageInline, ProductParameterInline))

class ProductModelTests(TestCase):
    def test_product_ordering_and_str(self):
        Product.objects.create(
            name='Test Product One',
            description='Test Description One',
            base_price=100,
            sort_order=1
        )
        two_product = Product.objects.create(
            name='Test Product Two',
            description='Test Description Two',
            base_price=200,
            sort_order=2
        )
        self.assertEqual(list(Product.objects.values_list("name", flat=True)), ["Test Product One", "Test Product Two"])
        self.assertEqual(str(two_product), "Test Product Two")

    def test_related_models_str(self):
        product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            base_price=100,
            sort_order=1
        )
        image = ProductImage.objects.create(
            product=product,
            image=SimpleUploadedFile("test1.jpg", b"file_content", content_type="image/jpeg"),
            caption='Test Image',
            sort_order=1
        )
        full_image = ProductImage.objects.create(
            product=product,
            image=SimpleUploadedFile("test2.jpg", b"file_content", content_type="image/jpeg"),
            caption='Test Full Image',
            sort_order=2
        )
        parameter = ProductParameter.objects.create(
            product=product,
            name='Test Parameter',
            value='Test Value',
            price='100',
            sort_order=1
        )

        self.assertEqual(str(image), "Test Product: Test Image")
        self.assertEqual(str(full_image), "Test Product: Test Full Image")
        self.assertEqual(str(parameter), "Test Product: Test Parameter")

class ProductFilterTests(TestCase):
    def test_filter_by_parameter_name_and_value(self):
        product = Product.objects.create(
            name='Product 1',
            description='Description of Product 1',
            base_price=100,
            sort_order=1
        )
        ProductParameter.objects.create(
            product=product,
            name='Color',
            value='Red',
            price=0,
            sort_order=1
        )
        ProductParameter.objects.create(
            product=product,
            name='Color',
            value='Blue',
            price=0,
            sort_order=2
        )
        product_two = Product.objects.create(
            name='Product 2',
            description='Description of Product 2',
            base_price=200,
            sort_order=2
        )
        ProductParameter.objects.create(
            product=product_two,
            name='Size',
            value='Large',
            price=0,
            sort_order=1
        )
        name_filter = ProductFilter(
            data={'param_name': 'Color'},
            queryset=Product.objects.all()
        )
        value_filter = ProductFilter(
            data={'param_value': 'Blue'},
            queryset=Product.objects.all()
        )

        self.assertEqual(list(name_filter.qs), [product])
        self.assertEqual(list(value_filter.qs), [product])

class ProductAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = get_user_model().objects.create_user(
            username='tester',
            password='pass1234'
        )
        self.client.force_authenticate(user=user)
        Product.objects.all().delete()

    def test_product_list_endpoint(self):
        print("Продуктов в базе перед тестом:", Product.objects.count())
        Product.objects.create(
            name='Test Product 1',
            description='Test Description 1',
            base_price=100,
            sort_order=1
        )
        Product.objects.create(
            name='Test Product 2',
            description='Test Description 2',
            base_price=200,
            sort_order=2
        )

        response = self.client.get('/rest/catalog/products/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertListEqual(
            [item['name'] for item in response.data["results"]],
            ['Test Product 1', 'Test Product 2']
        )
        self.assertSetEqual(
            set(response.data["results"][0].keys()),
            {'id', 'name', 'base_price', 'sort_order'}
        )

    def test_product_detail_endpoint(self):
        product = Product.objects.create(
            name='Product 1',
            description='Description of Product 1',
            base_price=100,
            sort_order=1
        )
        ProductImage.objects.create(
            product=product,
            image=SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg"),
            caption='Test Image',
            sort_order=1
        )
        ProductParameter.objects.create(
            product=product,
            name='Color',
            value='Red',
            price=0,
            sort_order=1
        )

        response = self.client.get(f'/rest/catalog/products/{product.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Product 1')
        self.assertEqual(response.data['description'], 'Description of Product 1')
        self.assertIn('images', response.data)
        self.assertIn('parameters', response.data)
        self.assertEqual(len(response.data['images']), 1)
        self.assertEqual(len(response.data['parameters']), 1)
