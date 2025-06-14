from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, payment_page

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', payment_page, name='payment_page'),
    path('', include(router.urls)),
] 