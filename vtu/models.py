from django.db import models
from django.conf import settings
import uuid

class DataPlan(models.Model):
    NETWORK_CHOICES = [
        ('MTN', 'MTN'),
        ('Airtel', 'Airtel'),
        ('Glo', 'Globacom (Glo)'),
        ('9Mobile', '9Mobile'),
    ]
    
    network = models.CharField(max_length=20, choices=NETWORK_CHOICES)
    name = models.CharField(max_length=100)
    volume = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    validity = models.CharField(max_length=50, default='30 Days')
    code = models.CharField(max_length=50, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.network} - {self.name} (₦{self.price})"

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('fund', 'Wallet Funding'),
        ('purchase', 'Service Purchase'),
        ('refund', 'Failed Order Refund'),
        ('commission', 'Referral Commission'),
    ]
    
    SERVICE_CHOICES = [
        ('airtime', 'Airtime Top-Up'),
        ('data', 'Data Subscription'),
        ('electricity', 'Electricity Payment'),
        ('tv', 'Cable TV Subscription'),
        ('exam_pin', 'Exam Pin Purchase'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='transactions'
    )
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reference = models.CharField(max_length=100, unique=True, blank=True)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} - {self.transaction_type} - ₦{self.amount} ({self.status})"
