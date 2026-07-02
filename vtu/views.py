from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction as db_transaction
from django.utils import timezone
from .models import DataPlan, Transaction
from accounts.models import CustomUser
from decimal import Decimal
import uuid

def seed_data_plans():
    plans = [
        # MTN
        ('MTN', 'MTN 100MB (1 Day)', '100MB', 100.00, '1 Day', 'mtn-100mb-1d'),
        ('MTN', 'MTN 1GB (1 Day)', '1GB', 350.00, '1 Day', 'mtn-1gb-1d'),
        ('MTN', 'MTN 1.5GB (30 Days)', '1.5GB', 1200.00, '30 Days', 'mtn-1.5gb-30d'),
        ('MTN', 'MTN 3GB (30 Days)', '3GB', 1600.00, '30 Days', 'mtn-3gb-30d'),
        ('MTN', 'MTN 5GB (30 Days)', '5GB', 2500.00, '30 Days', 'mtn-5gb-30d'),
        # Airtel
        ('Airtel', 'Airtel 100MB (1 Day)', '100MB', 100.00, '1 Day', 'airtel-100mb-1d'),
        ('Airtel', 'Airtel 1GB (1 Day)', '1GB', 350.00, '1 Day', 'airtel-1gb-1d'),
        ('Airtel', 'Airtel 1.5GB (30 Days)', '1.5GB', 1200.00, '30 Days', 'airtel-1.5gb-30d'),
        ('Airtel', 'Airtel 3GB (30 Days)', '3GB', 1500.00, '30 Days', 'airtel-3gb-30d'),
        # Glo
        ('Glo', 'Glo 1GB (1 Day)', '1GB', 300.00, '1 Day', 'glo-1gb-1d'),
        ('Glo', 'Glo 2.9GB (30 Days)', '2.9GB', 1100.00, '30 Days', 'glo-29gb-30d'),
        ('Glo', 'Glo 5.8GB (30 Days)', '5.8GB', 2000.00, '30 Days', 'glo-58gb-30d'),
        # 9Mobile
        ('9Mobile', '9Mobile 1GB (1 Day)', '1GB', 300.00, '1 Day', '9mobile-1gb-1d'),
        ('9Mobile', '9Mobile 2GB (30 Days)', '2GB', 1200.00, '30 Days', '9mobile-2gb-30d'),
    ]
    for network, name, volume, price, validity, code in plans:
        DataPlan.objects.get_or_create(
            code=code,
            defaults={
                'network': network,
                'name': name,
                'volume': volume,
                'price': price,
                'validity': validity,
                'active': True
            }
        )

@login_required
def dashboard(request):
    if DataPlan.objects.count() == 0:
        seed_data_plans()
    
    # Get last 5 transactions
    recent_transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Calculate stats
    total_spent = Decimal('0.00')
    total_rewards = Decimal('0.00')
    
    for txn in Transaction.objects.filter(user=request.user, status='success'):
        if txn.transaction_type == 'purchase':
            total_spent += txn.amount
        elif txn.transaction_type == 'commission':
            total_rewards += txn.amount
            
    context = {
        'recent_transactions': recent_transactions,
        'total_spent': total_spent,
        'total_rewards': total_rewards,
    }
    return render(request, 'vtu/dashboard.html', context)

@login_required
def buy_data(request):
    if DataPlan.objects.count() == 0:
        seed_data_plans()
        
    networks = ['MTN', 'Airtel', 'Glo', '9Mobile']
    plans = DataPlan.objects.filter(active=True)
    
    if request.method == 'POST':
        plan_id = request.POST.get('plan')
        phone_number = request.POST.get('phone_number')
        network = request.POST.get('network')
        
        if not plan_id or not phone_number:
            messages.error(request, "Please fill in all fields.")
            return redirect('buy_data')
            
        plan = get_object_or_404(DataPlan, id=plan_id)
        user = request.user
        
        if user.wallet_balance < plan.price:
            messages.error(request, "Insufficient wallet balance. Please fund your wallet.")
            return redirect('buy_data')
            
        # Process Purchase
        with db_transaction.atomic():
            # Deduct balance
            user.wallet_balance -= plan.price
            user.save()
            
            # Create transaction record
            txn = Transaction.objects.create(
                user=user,
                transaction_type='purchase',
                service='data',
                amount=plan.price,
                status='success',
                details=f"Data bundle: {plan.name} to {phone_number}"
            )
            
            # Award Cashback (1%)
            cashback = plan.price * Decimal('0.01')
            user.wallet_balance += cashback
            user.save()
            
            Transaction.objects.create(
                user=user,
                transaction_type='commission',
                service='data',
                amount=cashback,
                status='success',
                details=f"1% Cashback Reward for Data Purchase"
            )
            
            # Award Referrer Commission (2%)
            if user.referred_by:
                referrer = user.referred_by
                commission = plan.price * Decimal('0.02')
                referrer.wallet_balance += commission
                referrer.save()
                
                Transaction.objects.create(
                    user=referrer,
                    transaction_type='commission',
                    service='data',
                    amount=commission,
                    status='success',
                    details=f"2% Referral Commission from {user.username}'s purchase"
                )
                
        messages.success(request, f"Data subscription of {plan.name} to {phone_number} was successful! ₦{cashback:.2f} cashback rewarded.")
        return redirect('dashboard')
        
    context = {
        'networks': networks,
        'plans': plans,
    }
    return render(request, 'vtu/buy_data.html', context)

@login_required
def buy_airtime(request):
    networks = ['MTN', 'Airtel', 'Glo', '9Mobile']
    
    if request.method == 'POST':
        network = request.POST.get('network')
        phone_number = request.POST.get('phone_number')
        amount_str = request.POST.get('amount')
        
        if not network or not phone_number or not amount_str:
            messages.error(request, "Please fill in all fields.")
            return redirect('buy_airtime')
            
        try:
            amount = Decimal(amount_str)
        except ValueError:
            messages.error(request, "Invalid amount entered.")
            return redirect('buy_airtime')
            
        if amount < Decimal('50.00'):
            messages.error(request, "Minimum airtime purchase is ₦50.")
            return redirect('buy_airtime')
            
        user = request.user
        
        if user.wallet_balance < amount:
            messages.error(request, "Insufficient wallet balance. Please fund your wallet.")
            return redirect('buy_airtime')
            
        # Process Purchase
        with db_transaction.atomic():
            # Deduct balance
            user.wallet_balance -= amount
            user.save()
            
            # Create transaction record
            txn = Transaction.objects.create(
                user=user,
                transaction_type='purchase',
                service='airtime',
                amount=amount,
                status='success',
                details=f"{network} Airtime recharge of ₦{amount:.2f} to {phone_number}"
            )
            
            # Award Cashback (1%)
            cashback = amount * Decimal('0.01')
            user.wallet_balance += cashback
            user.save()
            
            Transaction.objects.create(
                user=user,
                transaction_type='commission',
                service='airtime',
                amount=cashback,
                status='success',
                details=f"1% Cashback Reward for Airtime Purchase"
            )
            
            # Award Referrer Commission (2%)
            if user.referred_by:
                referrer = user.referred_by
                commission = amount * Decimal('0.02')
                referrer.wallet_balance += commission
                referrer.save()
                
                Transaction.objects.create(
                    user=referrer,
                    transaction_type='commission',
                    service='airtime',
                    amount=commission,
                    status='success',
                    details=f"2% Referral Commission from {user.username}'s purchase"
                )
                
        messages.success(request, f"Airtime purchase of ₦{amount:.2f} to {phone_number} was successful! ₦{cashback:.2f} cashback rewarded.")
        return redirect('dashboard')
        
    context = {
        'networks': networks,
    }
    return render(request, 'vtu/buy_airtime.html', context)

@login_required
def fund_wallet(request):
    if request.method == 'POST':
        amount_str = request.POST.get('amount')
        if not amount_str:
            messages.error(request, "Please enter an amount.")
            return redirect('fund_wallet')
            
        try:
            amount = Decimal(amount_str)
        except ValueError:
            messages.error(request, "Invalid amount entered.")
            return redirect('fund_wallet')
            
        if amount < Decimal('100.00'):
            messages.error(request, "Minimum funding amount is ₦100.")
            return redirect('fund_wallet')
            
        # Render the simulated checkout payment gateway
        context = {
            'amount': amount,
            'ref': f"FUND-{uuid.uuid4().hex[:10].upper()}"
        }
        return render(request, 'vtu/checkout_simulator.html', context)
        
    return render(request, 'vtu/fund_wallet.html')

@login_required
def process_funding(request):
    if request.method == 'POST':
        amount_str = request.POST.get('amount')
        ref = request.POST.get('reference')
        card_num = request.POST.get('card_number')
        
        if not amount_str or not ref:
            messages.error(request, "Payment session expired. Please try again.")
            return redirect('fund_wallet')
            
        try:
            amount = Decimal(amount_str)
        except ValueError:
            messages.error(request, "Invalid amount.")
            return redirect('fund_wallet')
            
        user = request.user
        
        with db_transaction.atomic():
            # Update User balance
            user.wallet_balance += amount
            user.save()
            
            # Create transaction
            Transaction.objects.create(
                user=user,
                transaction_type='fund',
                amount=amount,
                status='success',
                reference=ref,
                details=f"Wallet funded via Simulated Card Gateway"
            )
            
        messages.success(request, f"Successfully funded wallet with ₦{amount:.2f}!")
        return redirect('dashboard')
        
    return redirect('fund_wallet')

@login_required
def pay_bills(request):
    if request.method == 'POST':
        bill_type = request.POST.get('bill_type')
        phone_number = request.POST.get('phone_number')
        
        if bill_type == 'electricity':
            provider = request.POST.get('disco')
            meter_num = request.POST.get('meter_number')
            amount_str = request.POST.get('amount')
            details = f"Electricity payment ({provider}) for Meter #{meter_num}"
            service_code = 'electricity'
        elif bill_type == 'tv':
            provider = request.POST.get('tv_provider')
            smartcard = request.POST.get('smartcard_number')
            package = request.POST.get('tv_package')
            
            # Simple package price mapping
            packages_prices = {
                'dstv_yanga': 5100.00,
                'dstv_confam': 9300.00,
                'dstv_premium': 37000.00,
                'gotv_smallie': 1800.00,
                'gotv_max': 7200.00,
                'gotv_supa': 9600.00,
            }
            price = packages_prices.get(package, 1500.00)
            amount_str = str(price)
            details = f"Cable TV ({provider} - {package.replace('_', ' ').upper()}) for Smartcard #{smartcard}"
            service_code = 'tv'
        elif bill_type == 'exam_pin':
            provider = request.POST.get('exam_type')
            qty_str = request.POST.get('quantity', '1')
            qty = int(qty_str) if qty_str.isdigit() else 1
            
            pin_prices = {'WAEC': 3800.00, 'NECO': 1200.00, 'JAMB': 4700.00}
            price = pin_prices.get(provider, 2000.00) * qty
            amount_str = str(price)
            details = f"Exam Pin purchase ({qty}x {provider} Pins) sent to {phone_number}"
            service_code = 'exam_pin'
        else:
            messages.error(request, "Invalid payment type.")
            return redirect('pay_bills')

        try:
            amount = Decimal(amount_str)
        except (ValueError, TypeError):
            messages.error(request, "Invalid amount entered.")
            return redirect('pay_bills')

        user = request.user
        if user.wallet_balance < amount:
            messages.error(request, "Insufficient wallet balance. Please fund your wallet.")
            return redirect('pay_bills')

        # Process bill payment
        with db_transaction.atomic():
            user.wallet_balance -= amount
            user.save()

            Transaction.objects.create(
                user=user,
                transaction_type='purchase',
                service=service_code,
                amount=amount,
                status='success',
                details=details
            )

            # 1% Cashback
            cashback = amount * Decimal('0.01')
            user.wallet_balance += cashback
            user.save()

            Transaction.objects.create(
                user=user,
                transaction_type='commission',
                service=service_code,
                amount=cashback,
                status='success',
                details=f"1% Cashback Reward for Bill Payment"
            )

            # 2% Referrer Commission
            if user.referred_by:
                referrer = user.referred_by
                commission = amount * Decimal('0.02')
                referrer.wallet_balance += commission
                referrer.save()
                
                Transaction.objects.create(
                    user=referrer,
                    transaction_type='commission',
                    service=service_code,
                    amount=commission,
                    status='success',
                    details=f"2% Referral Commission from {user.username}'s purchase"
                )

        messages.success(request, f"Bill payment successful: {details}. ₦{cashback:.2f} cashback rewarded.")
        return redirect('dashboard')

    return render(request, 'vtu/pay_bills.html')

@login_required
def rewards(request):
    user = request.user
    referred_users = CustomUser.objects.filter(referred_by=user)
    
    # Calculate total cashback and commissions
    commission_txns = Transaction.objects.filter(user=user, transaction_type='commission')
    total_rewards = sum(txn.amount for txn in commission_txns)
    
    context = {
        'referred_users': referred_users,
        'total_rewards': total_rewards,
        'commission_txns': commission_txns,
    }
    return render(request, 'vtu/rewards.html', context)

@login_required
def transaction_history(request):
    txns = Transaction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'vtu/transactions.html', {'transactions': txns})

@login_required
def admin_portal(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Only staff/admin accounts can access the Admin Portal.")
        return redirect('dashboard')
        
    all_users = CustomUser.objects.all().order_by('-date_joined')
    all_txns = Transaction.objects.all().order_by('-created_at')
    
    total_users = all_users.count()
    total_funded = sum(t.amount for t in all_txns if t.transaction_type == 'fund' and t.status == 'success')
    total_purchased = sum(t.amount for t in all_txns if t.transaction_type == 'purchase' and t.status == 'success')
    
    context = {
        'all_users': all_users,
        'all_transactions': all_txns,
        'total_users': total_users,
        'total_funded': total_funded,
        'total_purchased': total_purchased,
    }
    return render(request, 'vtu/admin_portal.html', context)

