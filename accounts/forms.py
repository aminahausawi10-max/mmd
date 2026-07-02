from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    referred_by_code = forms.CharField(
        max_length=50, 
        required=False, 
        label="Referral Code (Optional)",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. 5D8A3B21'})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'role')

    def clean_referred_by_code(self):
        code = self.cleaned_data.get('referred_by_code')
        if code:
            code = code.strip().upper()
            try:
                referrer = CustomUser.objects.get(referral_code=code)
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Invalid referral code. Please check and try again.")
        return code

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'wallet_balance')
