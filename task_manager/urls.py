from django.contrib import admin
from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('redocs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
