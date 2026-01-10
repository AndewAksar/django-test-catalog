# Copyright 2022 ITCase (info@itcase.pro)

# Django REST Framework
# https://github.com/tomchristie/django-rest-framework

REST_FRAMEWORK = {
    # access
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],

    # filtering
    'DEFAULT_FILTER_BACKENDS': [
        # https://github.com/carltongibson/django-filter
        'django_filters.rest_framework.DjangoFilterBackend'
    ],

    # response
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],

    # pagination
    'DEFAULT_PAGINATION_CLASS': ('rest_framework.pagination'
                                 '.LimitOffsetPagination'),
    'PAGE_SIZE': 100,

    # schema
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Catalog API',
    'DESCRIPTION': 'REST API for catalog products, parameters and images.',
    'VERSION': '1.0.0',
}
