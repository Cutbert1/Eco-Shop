from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Order


class OrderForm(forms.ModelForm):
    """
    Provides user-friendly placeholders, custom CSS classes,
    and autofocus to enhance the checkout user experience.
    """
    class Meta:
        model = Order
        fields = [
            'customer_name', 'email', 'phone_number',
            'address', 'city', 'postcode', 'county',
            'country', 'delivery_notes'
        ]

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with placeholders, classes, and autofocus.
        """
        super().__init__(*args, **kwargs)
        self._set_placeholders_and_classes()

    def _set_placeholders_and_classes(self):
        """
        Apply placeholders, CSS classes, and other HTML attributes
        to each form field to improve the form's usability.
        """
        placeholders = {
            'customer_name': 'Customer Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number (e.g., +12125551234)',
            'address': 'Street Address',
            'city': 'City',
            'postcode': 'Postal or Zip Code',
            'county': 'County or State',
            'country': 'Country',
            'delivery_notes': 'Delivery instructions (optional)',
        }

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'stripe-style-input'
            field.label = False

            if field_name == 'customer_name':
                field.widget.attrs['autofocus'] = True

            placeholder = placeholders[field_name]
            if field.required:
                placeholder += ' *'
            field.widget.attrs['placeholder'] = placeholder

            if field_name == 'delivery_notes':
                field.widget.attrs['rows'] = 3

    def clean_phone_number(self):
        """
        Custom validation for phone number to ensure it follows
        international format
        """
        phone_number = self.cleaned_data.get('phone_number')

        # If phone number is empty, it's allowed (field is optional)
        if not phone_number:
            return phone_number

        phone_str = str(phone_number).strip()

        if not phone_str.startswith('+'):
            raise ValidationError(
                "Phone number must include country code "
                "(e.g., +1234567890, +44 7445 363737)."
            )

        cleaned_phone = re.sub(r'[^\d+]', '', phone_str)

        # Check E.164 format: +[country code][number]
        # Country codes are 1-3 digits, total length should be 7-15 digits
        e164_regex = r'^\+[1-9]\d{6,14}$'

        if not re.match(e164_regex, cleaned_phone):
            raise ValidationError(
                "Please enter a valid international phone number with "
                "country code (e.g., +1234567890, +44 7445 363737)."
            )

        digits = cleaned_phone[1:]  # Remove the +
        if len(digits) < 7 or len(digits) > 14:
            raise ValidationError(
                "Phone number must be between 7-14 digits "
                "including country code."
            )

        if digits[0] == '0':
            raise ValidationError(
                "Invalid country code. Country codes cannot start with 0."
            )

        return phone_number

    def clean_city(self):
        """
        Validate city field to ensure it's not empty and has minimum length
        """
        city = self.cleaned_data.get('city')
        if not city or not city.strip():
            raise ValidationError("City is required.")

        city = city.strip()
        if len(city) < 2:
            raise ValidationError(
                "City name must be at least 2 characters long."
            )

        return city

    def clean_county(self):
        """
        Validate county/state field to ensure it's not empty and
        has minimum length
        """
        county = self.cleaned_data.get('county')
        if not county or not county.strip():
            raise ValidationError("County/State is required.")

        county = county.strip()
        if len(county) < 2:
            raise ValidationError(
                "County/State must be at least 2 characters long."
            )

        return county

    def clean_country(self):
        """
        Validate country field to ensure a valid country is selected
        """
        country = self.cleaned_data.get('country')
        if not country:
            raise ValidationError("Please select a country.")

        if str(country).strip() in ['', 'Select Country *']:
            raise ValidationError("Please select a valid country.")

        return country
