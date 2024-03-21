from django import forms

class AddFoodForm(forms.Form):
    name = forms.CharField(max_length=100)
    category = forms.CharField(max_length=100)
    price = forms.DecimalField(max_digits=10, decimal_places=2)

class AddEmployeeForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    wage = forms.FloatField()
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

class EditEmployeeForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    wage = forms.FloatField()

class EditEmployeeShifts(forms.Form):
    start_time = forms.DateTimeField(widget=forms.DateTimeInput())
    end_time = forms.DateTimeField(widget=forms.DateTimeInput())
    