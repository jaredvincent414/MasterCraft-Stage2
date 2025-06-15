from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Payment
from decimal import Decimal
from unittest.mock import patch

# Create your tests here.

class PaymentAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payment_data = {
            'customer_name': 'John Doe',
            'customer_email': 'john@example.com',
            'amount': '50.00'
        }
        # Mock PayPal response
        self.mock_paypal_response = {
            'success': True,
            'payment_id': 'test-payment-id',
            'approval_url': 'https://www.sandbox.paypal.com/test-approval-url'
        }

    @patch('payments.services.PayPalService.create_payment')
    def test_create_payment(self, mock_create_payment):
        # Configure the mock
        mock_create_payment.return_value = self.mock_paypal_response

        url = reverse('payment-list')
        response = self.client.post(url, self.payment_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(Payment.objects.get().customer_name, 'John Doe')
        
        # Verify the mock was called
        mock_create_payment.assert_called_once()

    def test_retrieve_payment(self):
        payment = Payment.objects.create(
            customer_name='John Doe',
            customer_email='john@example.com',
            amount=Decimal('50.00')
        )
        url = reverse('payment-detail', args=[payment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['payment']['customer_name'], 'John Doe')
