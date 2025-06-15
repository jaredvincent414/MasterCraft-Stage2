import paypalrestsdk
from django.conf import settings
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class PayPalService:
    def __init__(self):
        try:
            paypalrestsdk.configure({
                "mode": settings.PAYPAL_MODE,  # sandbox or live
                "client_id": settings.PAYPAL_CLIENT_ID,
                "client_secret": settings.PAYPAL_CLIENT_SECRET
            })
        except Exception as e:
            logger.error(f"Failed to configure PayPal SDK: {str(e)}")
            raise

    def create_payment(self, amount, currency="USD", description="Payment for goods/services"):
        try:
            # Create payment with proper URLs
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": settings.PAYPAL_RETURN_URL,
                    "cancel_url": settings.PAYPAL_CANCEL_URL
                },
                "transactions": [{
                    "amount": {
                        "total": str(amount),
                        "currency": currency
                    },
                    "description": description
                }]
            })

            if payment.create():
                logger.info(f"Successfully created PayPal payment: {payment.id}")
                return {
                    "success": True,
                    "payment_id": payment.id,
                    "approval_url": payment.links[1].href
                }
            
            logger.error(f"Failed to create PayPal payment: {payment.error}")
            return {
                "success": False,
                "error": payment.error
            }
        except Exception as e:
            logger.error(f"Exception while creating PayPal payment: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def execute_payment(self, payment_id, payer_id):
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            if payment.execute({"payer_id": payer_id}):
                logger.info(f"Successfully executed PayPal payment: {payment_id}")
                return {
                    "success": True,
                    "payment_id": payment.id,
                    "status": payment.state
                }
            
            logger.error(f"Failed to execute PayPal payment {payment_id}: {payment.error}")
            return {
                "success": False,
                "error": payment.error
            }
        except Exception as e:
            logger.error(f"Exception while executing PayPal payment {payment_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_payment_details(self, payment_id):
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            logger.info(f"Successfully retrieved PayPal payment details: {payment_id}")
            return {
                "success": True,
                "payment_id": payment.id,
                "status": payment.state,
                "amount": payment.transactions[0].amount.total,
                "currency": payment.transactions[0].amount.currency
            }
        except Exception as e:
            logger.error(f"Exception while getting PayPal payment details {payment_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def cancel_payment(self, payment_id):
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            if payment.state == "created":
                payment.cancel()
                logger.info(f"Successfully cancelled PayPal payment: {payment_id}")
                return {
                    "success": True,
                    "payment_id": payment.id,
                    "status": "cancelled"
                }
            
            logger.warning(f"Cannot cancel PayPal payment {payment_id}: Invalid state {payment.state}")
            return {
                "success": False,
                "error": f"Cannot cancel payment in state: {payment.state}"
            }
        except Exception as e:
            logger.error(f"Exception while cancelling PayPal payment {payment_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            } 