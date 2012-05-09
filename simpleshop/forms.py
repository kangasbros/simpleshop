from django import forms
from simpleshop.models import Product

class PurchaseForm(forms.Form):
    # TODO: Add support for multiple products.
    quantity = forms.IntegerField(min_value=1)
    email = forms.EmailField()
    name = forms.CharField(label='Shipping Name', max_length=100, required=False)
    address = forms.CharField(label='Shipping Address (include country)', widget=forms.Textarea(attrs={'rows': 4, 'cols': 30}))
    
    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        # TODO: Add support for multiple products.
        products = Product.objects.all()
        if products.count() == 1 and data > products[0].stock:
            raise forms.ValidationError("Only " + str(products[0].stock) + " in stock. Please set this number no higher than the current stock.")
        
        return data
