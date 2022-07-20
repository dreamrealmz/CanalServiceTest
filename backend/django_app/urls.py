from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="API Shop",
        default_version='v1',
        description="my own service swagger v1",
        terms_of_service="",
        contact=openapi.Contact(email="ad.azarov17@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('google_sheet.urls')),
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
