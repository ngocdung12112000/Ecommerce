from django import forms
from .models import PAYMENT_CHOICES
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AddressForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '1234 Main St'}))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Apartment, suite, unit etc. (optional)'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Country'}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Zip'}))
    save_info = forms.BooleanField(required=False)
    default = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', ]