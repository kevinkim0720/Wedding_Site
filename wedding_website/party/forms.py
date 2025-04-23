from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from .choices import *
from .models import *

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



class RsvpForm(forms.ModelForm):
    class Meta:
        model = invitation_info
        fields = ['invitation', 'address', 'city', 'state', 'zip_code', 'group_type', 'number_of_guests', 'guest_names', 'invite']


    def clean(self):
        cleaned_data = super().clean()
        invitation = cleaned_data.get("invitation")
        address = cleaned_data.get("address")
        city = cleaned_data.get('city')
        state = cleaned_data.get('state')
        zip_code = cleaned_data.get('zip_code')
        group_type = cleaned_data.get("group_type")
        number_of_guests = cleaned_data.get("number_of_guests")
        guest_names = cleaned_data.get("guest_names")
        invite = cleaned_data.get("invite")

        if invitation and not address:
            raise forms.ValidationError("Address is required when Invitation is checked.")
        if invitation and not city:
            raise forms.ValidationError("City is required when Invitation is checked.")
        if invitation and not state:
            raise forms.ValidationError("State is required when Invitation is checked.")
        if invitation and not zip_code:
            raise forms.ValidationError("Zip Code is required when Invitation is checked.")
        
        if group_type == 'other' and not number_of_guests:
            raise forms.ValidationError("Number of guests is required if 'Other' is selected.")
        if group_type == 'family' and not number_of_guests:
            raise forms.ValidationError("Number of guests is required for self or family.")
        if group_type != 'self' and not guest_names:
            raise forms.ValidationError("Guest names is required for family or other.")

        
        return cleaned_data

