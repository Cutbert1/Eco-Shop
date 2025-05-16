from django import forms
from .models import AccountProfile


class AccountProfileForm(forms.ModelForm):
    class Meta:
        model = AccountProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with placeholders, classes, and autofocus.
        """
        super().__init__(*args, **kwargs)
        self._set_placeholders_and_classes()
        self._set_widget_attributes()

    def _set_placeholders_and_classes(self):
        """Set placeholders for the form fields."""
        placeholders = {
            'primary_phone_number': 'Phone Number',
            'primary_address': 'Street Address',
            'primary_city': 'City',
            'primary_postcode': 'Postal or Zip Code',
            'primary_county': 'County or State',
            'primary_country': 'Country',
        }

        for field, placeholder in placeholders.items():
            if self.fields[field].required:
                self.fields[field].widget.attrs['placeholder'] = f'{placeholder} *'  # noqa
            else:
                self.fields[field].widget.attrs['placeholder'] = placeholder

    def _set_widget_attributes(self):
        """Set common widget attributes for the form fields."""
        self.fields['primary_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'  # noqa
            self.fields[field].label = False
