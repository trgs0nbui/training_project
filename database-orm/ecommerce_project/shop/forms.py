from django import forms
from .models import Product
from django.core.exceptions import ValidationError

# validator cho price
def validate_price(value):
    if value < 100:
        raise ValidationError("Price must be at least 100")

class ProductForm(forms.ModelForm):
    # price = forms.DecimalField(validators=[validate_price])
    
    # clean field
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        if "test" in name.lower():
            raise forms.ValidationError("Name can't contain 'test'")
        
        return name
    
    def clean(self):
        cleaned_data = super().clean()

        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        
        if name and price:
            if "free" in name.lower() and price > 0:
                self.add_error('price', "Free product must be 0")
                
        return cleaned_data
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description', 'tags']
        