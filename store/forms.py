from .models.product import Products
from django import forms


class ProductCreate(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'
