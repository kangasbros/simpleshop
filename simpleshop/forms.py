from django import forms

class PurchaseForm(forms.Form):
    # Add in support for checking inventory?
    quantity = forms.IntegerField(min_value=1, max_value=5)
    email = forms.EmailField()
    name = forms.CharField(label='Shipping Name', max_length=100, required=False)
    address = forms.CharField(label='Shipping Address (include country)', widget=forms.Textarea(attrs={'rows': 4, 'cols': 30}))
