import paypalrestsdk
from django.conf import settings
from decimal import Decimal

class PayPalService:
    def __init__(self):
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,  # sandbox or live
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })

    def create_payment(self, amount, currency="USD", description="Payment for goods/services"):
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
            return {
                "success": True,
                "payment_id": payment.id,
                "approval_url": payment.links[1].href
            }
        return {
            "success": False,
            "error": payment.error
        }

    def execute_payment(self, payment_id, payer_id):
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            return {
                "success": True,
                "payment_id": payment.id,
                "status": payment.state
            }
        return {
            "success": False,
            "error": payment.error
        }

    def get_payment_details(self, payment_id):
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            return {
                "success": True,
                "payment_id": payment.id,
                "status": payment.state,
                "amount": payment.transactions[0].amount.total,
                "currency": payment.transactions[0].amount.currency
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            } 