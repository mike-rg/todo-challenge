from django.urls import path

from .views import RegisterUserAPIView, UserEmailVerificationAPIView


app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('verify-email/<str:token>/', UserEmailVerificationAPIView.as_view(), name='verify-email'),
]
