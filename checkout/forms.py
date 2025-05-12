from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_name', 'email', 'phone_number',
            'address', 'city', 'postcode', 'zipcode', 'county',
            'country',
        ]

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with placeholders, classes, and autofocus.
        """
        super().__init__(*args, **kwargs)
        self._set_placeholders_and_classes()

    def _set_placeholders_and_classes(self):
        placeholders = {
            'customer_name': 'Customer Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'address': 'Address',
            'city': 'City',
            'postcode': 'Postal Code',
            'zipcode': 'Zip Code',
            'county': 'County or State',
            'country': 'Country',
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
