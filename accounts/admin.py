from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'role', 'wallet_balance', 'referral_code', 'referred_by', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('VTU Account Info', {'fields': ('role', 'wallet_balance', 'referral_code', 'referred_by')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('VTU Account Info', {'fields': ('role', 'wallet_balance')}),
    )
    search_fields = ['username', 'email', 'referral_code']
    ordering = ['username']

admin.site.register(CustomUser, CustomUserAdmin)
