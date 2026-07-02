from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Standard User'),
        ('reseller', 'Reseller/Agent'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    referral_code = models.CharField(max_length=50, unique=True, blank=True)
    referred_by = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='referees'
    )
    wallet_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
