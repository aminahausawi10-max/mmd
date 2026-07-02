from django.urls import path
from .views import (
    dashboard, 
    buy_data, 
    buy_airtime, 
    fund_wallet, 
    process_funding, 
    pay_bills, 
    rewards, 
    transaction_history,
    admin_portal
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('buy-data/', buy_data, name='buy_data'),
    path('buy-airtime/', buy_airtime, name='buy_airtime'),
    path('fund-wallet/', fund_wallet, name='fund_wallet'),
    path('process-funding/', process_funding, name='process_funding'),
    path('pay-bills/', pay_bills, name='pay_bills'),
    path('rewards/', rewards, name='rewards'),
    path('transactions/', transaction_history, name='transactions'),
    path('admin-portal/', admin_portal, name='admin_portal'),
]
