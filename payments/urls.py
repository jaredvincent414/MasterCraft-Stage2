from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, PayPalWebhookView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('webhooks/paypal/', PayPalWebhookView.as_view(), name='paypal-webhook'),
] 