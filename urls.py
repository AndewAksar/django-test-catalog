# Copyright 2022 ITCase (info@itcase.pro)

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

from filebrowser.sites import site as fb_site
from rest_framework.authtoken import views as rest_token_views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

admin.autodiscover()

urlpatterns = [
    # admin
    path('admin', RedirectView.as_view(url='/admin/', permanent=False)),
    path(
        'admin/',
        include([
            # third-party
            path('django-rq/', include('django_rq.urls')),
            path('filebrowser/', fb_site.urls),
            path('grappelli/', include('grappelli.urls')),

            # django
            path('', admin.site.urls),
        ])),

    # rest
    path('rest/',
         include([
             path('token/', ObtainAuthToken.as_view(permission_classes=[AllowAny]), name='token'),
             path('schema/', SpectacularAPIView.as_view(
                 permission_classes=[permissions.AllowAny]), name='schema'),
             path('docs/', SpectacularSwaggerView.as_view(
                 url_name='schema',
                 permission_classes=[permissions.AllowAny]),
                 name='swagger-ui'),
             path('', include('catalog.urls')),
         ])),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
