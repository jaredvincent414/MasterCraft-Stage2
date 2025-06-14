from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer
from .services import PayPalService

# Create your views here.

def payment_page(request):
    return render(request, 'payments/payment.html')

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    paypal_service = PayPalService()

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create payment in PayPal
        paypal_response = self.paypal_service.create_payment(
            amount=serializer.validated_data['amount'],
            currency=request.data.get('currency', 'USD')
        )
        
        if not paypal_response['success']:
            return Response({
                'status': 'error',
                'message': 'Failed to create PayPal payment',
                'error': paypal_response['error']
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create payment in our database
        payment = serializer.save(
            payment_id=paypal_response['payment_id'],
            approval_url=paypal_response['approval_url']
        )
        
        response_serializer = PaymentSerializer(payment)
        return Response({
            'payment': response_serializer.data,
            'status': 'success',
            'message': 'Payment initiated successfully.',
            'approval_url': paypal_response['approval_url']
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        payment = self.get_object()
        
        # Get updated status from PayPal
        if payment.payment_id:
            paypal_details = self.paypal_service.get_payment_details(payment.payment_id)
            if paypal_details['success']:
                payment.status = 'completed' if paypal_details['status'] == 'approved' else payment.status
                payment.save()
        
        serializer = self.get_serializer(payment)
        return Response({
            'payment': serializer.data,
            'status': 'success',
            'message': 'Payment details retrieved successfully.'
        })

    @action(detail=True, methods=['post'])
    def execute(self, request, *args, **kwargs):
        payment = self.get_object()
        payer_id = request.data.get('payer_id')
        
        if not payer_id:
            return Response({
                'status': 'error',
                'message': 'Payer ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Execute payment in PayPal
        paypal_response = self.paypal_service.execute_payment(
            payment.payment_id,
            payer_id
        )
        
        if not paypal_response['success']:
            return Response({
                'status': 'error',
                'message': 'Failed to execute PayPal payment',
                'error': paypal_response['error']
            }, status=status.HTTP_400_BAD_REQUEST)

        # Update payment status
        payment.status = 'completed'
        payment.payer_id = payer_id
        payment.save()
        
        serializer = self.get_serializer(payment)
        return Response({
            'payment': serializer.data,
            'status': 'success',
            'message': 'Payment executed successfully.'
        })
