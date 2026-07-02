from django.contrib import admin
from .models import DataPlan, Transaction

@admin.register(DataPlan)
class DataPlanAdmin(admin.ModelAdmin):
    list_display = ['network', 'name', 'volume', 'price', 'validity', 'active']
    list_filter = ['network', 'active']
    search_fields = ['name', 'code']
    list_editable = ['price', 'active']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'transaction_type', 'service', 'amount', 'status', 'created_at']
    list_filter = ['transaction_type', 'service', 'status', 'created_at']
    search_fields = ['reference', 'user__username', 'details']
    readonly_fields = ['reference', 'created_at', 'updated_at']
    ordering = ['-created_at']
