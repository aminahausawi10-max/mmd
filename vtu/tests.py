from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser
from vtu.models import DataPlan, Transaction
from decimal import Decimal

class VTUPlatformTests(TestCase):

    def setUp(self):
        # Create a referrer user
        self.referrer = CustomUser.objects.create_user(
            username='referrer_user',
            email='referrer@peach.com',
            password='testpassword123',
            role='user'
        )
        
        # Create a user referred by the referrer
        self.user = CustomUser.objects.create_user(
            username='regular_user',
            email='user@peach.com',
            password='testpassword123',
            role='user',
            referred_by=self.referrer
        )
        
        # Fund the user's wallet initially for purchase tests
        self.user.wallet_balance = Decimal('5000.00')
        self.user.save()

        # Seed a test data plan
        self.plan = DataPlan.objects.create(
            network='MTN',
            name='MTN 1.5GB Daily',
            volume='1.5GB',
            price=Decimal('1200.00'),
            validity='30 Days',
            code='mtn-test-15gb',
            active=True
        )

    def test_referral_code_auto_generation(self):
        """Test that referral codes are automatically generated upon user creation."""
        user = CustomUser.objects.create_user(
            username='new_user',
            email='new@peach.com',
            password='testpassword123'
        )
        self.assertIsNotNone(user.referral_code)
        self.assertEqual(len(user.referral_code), 8)

    def test_wallet_funding_flow(self):
        """Test the simulated card funding process."""
        self.client.login(username='regular_user', password='testpassword123')
        
        # Initial balance check
        self.assertEqual(self.user.wallet_balance, Decimal('5000.00'))
        
        # Process mock funding POST
        response = self.client.post(reverse('process_funding'), {
            'amount': '1500.00',
            'reference': 'TEST-FUND-REF-100',
            'card_number': '4012 3456 7890 1234'
        })
        
        # Verification
        self.user.refresh_from_db()
        self.assertEqual(self.user.wallet_balance, Decimal('6500.00'))
        self.assertEqual(response.status_code, 302) # Redirect to dashboard
        
        # Check transaction creation
        txn = Transaction.objects.get(reference='TEST-FUND-REF-100')
        self.assertEqual(txn.transaction_type, 'fund')
        self.assertEqual(txn.amount, Decimal('1500.00'))
        self.assertEqual(txn.status, 'success')

    def test_data_bundle_purchase_rewards_and_commissions(self):
        """Test that buying a data plan deducts the balance, logs the transaction, awards 1% cashback, and credits 2% referral commission."""
        self.client.login(username='regular_user', password='testpassword123')
        
        # Execute purchase POST
        response = self.client.post(reverse('buy_data'), {
            'network': 'MTN',
            'plan': self.plan.id,
            'phone_number': '08031234567'
        })
        
        # 1. Check redirects back to dashboard on success
        self.assertEqual(response.status_code, 302)
        
        # 2. Check regular user balance deduction, plus 1% cashback
        # Price = 1200.00
        # Deduct 1200.00 -> balance becomes 3800.00
        # Cashback = 1% of 1200.00 = 12.00
        # Final balance should be 3800.00 + 12.00 = 3812.00
        self.user.refresh_from_db()
        self.assertEqual(self.user.wallet_balance, Decimal('3812.00'))
        
        # 3. Check referrer commission (2% of 1200.00 = 24.00)
        self.referrer.refresh_from_db()
        self.assertEqual(self.referrer.wallet_balance, Decimal('24.00'))
        
        # 4. Check purchase transaction creation
        purchase_txn = Transaction.objects.filter(user=self.user, transaction_type='purchase').first()
        self.assertIsNotNone(purchase_txn)
        self.assertEqual(purchase_txn.amount, Decimal('1200.00'))
        self.assertEqual(purchase_txn.status, 'success')
        self.assertEqual(purchase_txn.service, 'data')
        
        # 5. Check cashback transaction creation
        cashback_txn = Transaction.objects.filter(user=self.user, transaction_type='commission').first()
        self.assertIsNotNone(cashback_txn)
        self.assertEqual(cashback_txn.amount, Decimal('12.00'))
        self.assertTrue("Cashback" in cashback_txn.details)
        
        # 6. Check referral commission transaction creation
        commission_txn = Transaction.objects.filter(user=self.referrer, transaction_type='commission').first()
        self.assertIsNotNone(commission_txn)
        self.assertEqual(commission_txn.amount, Decimal('24.00'))
        self.assertTrue("Referral Commission" in commission_txn.details)
