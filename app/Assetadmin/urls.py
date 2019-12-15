from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from django.views.generic import TemplateView
from django.http import HttpResponseBadRequest
api_v1_urls = [
    path("", include("assets.urls.api_urls")),
    path("", include("user.urls.api_urls"))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include(api_v1_urls)),
    path("docs/", include_docs_urls(title='ALL Api Docs',permission_classes=[],authentication_classes=[])),
]
