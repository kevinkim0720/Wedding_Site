from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from .choices import *
from .models import *

class GuestInfoForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True, help_text="Enter phone number without dashes")
    knows = forms.ChoiceField(choices = picks, required=True, help_text="Do you know the Bride, Groom, or both?")
    code = forms.CharField(required=True)

    def clean_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) !=10:
            self.add_error('phone_number', "Please enter valid phone number")


class EmailValidationForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Additional validation logic if needed
        return email



class RsvpForm(forms.ModelForm):
    class Meta:
        model = invitation_info
        fields = ['name', 'attend', 'party', 'group_type', 'number_of_guests', 'guest_names', 'invite']
        labels = {
            'attend': 'Will Attend',
            'party': 'Planning on attending after party?',
            'number_of_guests': 'Family size (including yourself)',
            'guest_names': 'Provide full names (excluding yourself)',
            'invite': 'Check for physical invitation if not received',
        }


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        attend = cleaned_data.get("attend")
        party = cleaned_data.get("party")
        group_type = cleaned_data.get("group_type")
        number_of_guests = cleaned_data.get("number_of_guests")
        guest_names = cleaned_data.get("guest_names")
        invite = cleaned_data.get("invite")
        
         # Rule 1: If group_type is "Just Myself", force number_of_guests to 0
        if group_type == "self":
            cleaned_data['number_of_guests'] = 0
            cleaned_data['guest_names'] = None

        # Rule 2: If number_of_guests > 0, guest_names is required
        if number_of_guests > 0:
            if not guest_names:
                self.add_error('guest_names', "Please enter names for each family member.")


        
        return cleaned_data

