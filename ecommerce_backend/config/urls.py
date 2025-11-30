from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(title="ecommerce-backend API", default_version="v1"),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("store.urls")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
]

# Optionally include GraphQL if graphene-django is available and configured
try:
    urlpatterns.append(path("graphql/", include("graphene_django.urls")))
except Exception:
    pass

# Optionally include ecommerce URLs if the app is available and has URLs
try:
    from ecommerce import urls as ecommerce_urls
    urlpatterns.append(path("ecommerce-api/", include(ecommerce_urls)))
except ImportError:
    pass
