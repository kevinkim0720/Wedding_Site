from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from .choices import *

class GuestInfoForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = PhoneNumberField(region="US")
    knows = forms.ChoiceField(choices = picks, required=True, help_text="Do you know the Bride, Groom, or both?")


class EmailValidationForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Additional validation logic if needed
        return email