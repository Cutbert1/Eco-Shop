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

        # Convert to string to handle PhoneNumber objects
        phone_str = str(phone_number).strip()

        # Must start with +
        if not phone_str.startswith('+'):
            raise ValidationError(
                "Phone number must include country code "
                "(e.g., +1234567890, +44 7445 363737)."
            )

        # Remove all formatting (spaces, dashes, parentheses) but keep the +
        cleaned_phone = re.sub(r'[^\d+]', '', phone_str)

        # Check E.164 format: +[country code][number]
        # Country codes are 1-3 digits, total length should be 7-15 digits
        e164_regex = r'^\+[1-9]\d{6,14}$'

        if not re.match(e164_regex, cleaned_phone):
            raise ValidationError(
                "Please enter a valid international phone number with "
                "country code (e.g., +1234567890, +44 7445 363737)."
            )

        # Additional length check for cleaned number
        digits = cleaned_phone[1:]  # Remove the +
        if len(digits) < 7 or len(digits) > 14:
            raise ValidationError(
                "Phone number must be between 7-14 digits "
                "including country code."
            )

        # Country code validation (first digit cannot be 0)
        if digits[0] == '0':
            raise ValidationError(
                "Invalid country code. Country codes cannot start with 0."
            )

        return phone_number
