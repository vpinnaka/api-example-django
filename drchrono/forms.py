from django import forms
from django.forms import widgets
import datetime


# Add your forms here
class CheckinForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    date_of_birth = forms.DateField(initial=datetime.date.today)
    social_security_number = forms.RegexField(
        help_text='if you don\'t have SSN, just leave it blank',
        required=False,
        regex='^\d{3}-?\d{2}-?\d{4}$',
        error_messages={
            'invalid': 'Enter a valid SSN in the format XXX-XX-XXXX'
        }
    )

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name.strip() == '':
            raise forms.ValidationError("Please provide first name")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if last_name.strip() == '':
            raise forms.ValidationError("Please provide last name")
        return last_name
