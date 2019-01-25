from django import forms
from django.forms import widgets
import datetime


# Add your forms here
class CheckinForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    # date_of_birth = forms.DateField(initial=datetime.date.today)
    social_security_number = forms.RegexField(
        help_text='Please enter your SSN in the format XXX-XX-XXXX',
        required=True,
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


class DemographicsForm(forms.Form):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    date_of_birth = forms.DateField(
        required=False,
        error_messages={
            'invalid': 'Enter a valid date in the format YYYY-MM-DD'
        }
    )
    gender = forms.ChoiceField(required=False, choices=GENDER_CHOICES)
    address = forms.CharField(required=False)
    zip_code = forms.RegexField(
        required=False,
        regex='^(\d{5})(-\d{4})?$',
        error_messages={
            'invalid': 'Enter a zip code in the format XXXXX or XXXXX-XXXX',
        }
    )
    city = forms.CharField(required=False)
    state = forms.RegexField(required=False,
                             regex='^([A-Z]{2})?$',
                             error_messages={
                                 'invalid': 'Enter state in Two-letter abbreviation format',
                             })
    email = forms.EmailField(required=False)
    cell_phone = forms.RegexField(
        required=False,
        regex='^\(\d{3}\)\s*\d{3}-\d{4}$',
        error_messages={
            'invalid': 'U.S. phone numbers must be in (XXX) XXX-XXXX format',
        }
    )
