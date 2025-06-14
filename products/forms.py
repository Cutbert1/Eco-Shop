from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """
    - Uses a custom clearable file input widget for the product image.
    - Dynamically sets category choices with user-friendly names.
    - Adds consistent CSS styling to all fields.
    """

    class Meta:
        model = Product
        fields = '__all__'

    product_image = forms.ImageField(
        label='', required=False, widget=CustomClearableFileInput
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_category_choices()
        self._apply_field_styles()

    def _set_category_choices(self):
        """Set the choices for the category field."""
        categories = Category.objects.all()
        friendly_names = [(
            category.id, category.get_friendly_name()
            ) for category in categories]
        self.fields['category'].choices = friendly_names

    def _apply_field_styles(self):
        """Apply CSS classes to all form fields."""
        for field in self.fields.values():
            field.widget.attrs['class'] = 'border-dark rounded-0'
