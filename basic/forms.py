from django import forms

class AddFoodForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    category = forms.CharField(label='Category', max_length=100)
    price = forms.DecimalField(label='Price', max_digits=10, decimal_places=2)
    
class EditFoodForm(forms.Form):
    initial_name = forms.CharField(label='Name', max_length=100)
    initial_category = forms.CharField(label='Category', max_length=100)
    initial_price = forms.DecimalField(label='Price', max_digits=10, decimal_places=2)

class AddEmployeeForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    wage = forms.FloatField()
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    GROUP_CHOICES = (
        ("foh","Front of House"),
        ("boh", "Back of House"),
        ("manager", "Manager")
    )
    user_groups = forms.MultipleChoiceField(choices = GROUP_CHOICES, widget=forms.CheckboxSelectMultiple)

class EditEmployeeForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    wage = forms.FloatField()
    GROUP_CHOICES = (
        ("foh","Front of House"),
        ("boh", "Back of House"),
        ("manager", "Manager")
    )
    user_groups = forms.MultipleChoiceField(choices = GROUP_CHOICES, widget=forms.CheckboxSelectMultiple)

class EditEmployeeShifts(forms.Form):
    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()
    