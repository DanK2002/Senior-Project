from django import forms

class AddFoodForm(forms.Form):
    name = forms.CharField(max_length=100)
    category = forms.CharField(max_length=100)
    price = forms.DecimalField(max_digits=10, decimal_places=2)