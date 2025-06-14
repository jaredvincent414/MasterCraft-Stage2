from django.db import models
import uuid

class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    PAYMENT_PROVIDER = (
        ('paypal', 'PayPal'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # PayPal specific fields
    payment_provider = models.CharField(max_length=20, choices=PAYMENT_PROVIDER, default='paypal')
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    payer_id = models.CharField(max_length=255, null=True, blank=True)
    approval_url = models.URLField(null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')

    def __str__(self):
        return f"Payment {self.id} - {self.customer_name}"

    class Meta:
        ordering = ['-created_at']
