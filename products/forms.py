from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

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
