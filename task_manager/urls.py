from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('docs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/vi/auth/', include('apps.accounts.urls'), name='accounts'),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include('apps.assignments.urls'), name='assignments'),
]
