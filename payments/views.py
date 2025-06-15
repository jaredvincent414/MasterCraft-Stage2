from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer
from .services import PayPalService
import logging

logger = logging.getLogger(__name__)

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
            logger.error(f"Failed to create PayPal payment: {paypal_response['error']}")
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
            logger.error(f"Failed to execute PayPal payment: {paypal_response['error']}")
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

    @action(detail=True, methods=['post'])
    def cancel(self, request, *args, **kwargs):
        payment = self.get_object()
        
        if payment.status != 'pending':
            return Response({
                'status': 'error',
                'message': f'Cannot cancel payment in status: {payment.status}'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Cancel payment in PayPal
        paypal_response = self.paypal_service.cancel_payment(payment.payment_id)
        
        if not paypal_response['success']:
            logger.error(f"Failed to cancel PayPal payment: {paypal_response['error']}")
            return Response({
                'status': 'error',
                'message': 'Failed to cancel PayPal payment',
                'error': paypal_response['error']
            }, status=status.HTTP_400_BAD_REQUEST)

        # Update payment status
        payment.status = 'failed'
        payment.save()
        
        serializer = self.get_serializer(payment)
        return Response({
            'payment': serializer.data,
            'status': 'success',
            'message': 'Payment cancelled successfully.'
        })

@method_decorator(csrf_exempt, name='dispatch')
class PayPalWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Verify webhook signature (implement based on PayPal's documentation)
            # For now, we'll just process the webhook
            
            event_type = request.data.get('event_type')
            resource = request.data.get('resource', {})
            payment_id = resource.get('id')
            
            if not payment_id:
                return Response({
                    'status': 'error',
                    'message': 'No payment ID in webhook'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                payment = Payment.objects.get(payment_id=payment_id)
            except Payment.DoesNotExist:
                logger.error(f"Payment not found for webhook: {payment_id}")
                return Response({
                    'status': 'error',
                    'message': 'Payment not found'
                }, status=status.HTTP_404_NOT_FOUND)

            # Update payment status based on webhook event
            if event_type == 'PAYMENT.SALE.COMPLETED':
                payment.status = 'completed'
            elif event_type == 'PAYMENT.SALE.DENIED':
                payment.status = 'failed'
            elif event_type == 'PAYMENT.SALE.REFUNDED':
                payment.status = 'failed'  # or add a new status for refunded
            
            payment.save()
            
            return Response({
                'status': 'success',
                'message': 'Webhook processed successfully'
            })
            
        except Exception as e:
            logger.error(f"Error processing PayPal webhook: {str(e)}")
            return Response({
                'status': 'error',
                'message': 'Error processing webhook',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
