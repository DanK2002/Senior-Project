import json
from django import forms
from .models import Food, Ingredient

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class AddFoodForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    category = forms.CharField(label='Category', max_length=100)
    price = forms.DecimalField(label='Price', max_digits=10, decimal_places=2)

class AddMealForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    price = forms.DecimalField(label='Price', max_digits=10, decimal_places=2)
    foods = forms.ModelMultipleChoiceField(queryset=Food.objects.all().values_list('name', flat=True), widget=forms.CheckboxSelectMultiple)

class EditFoodForm(forms.Form):
    initial_name = forms.CharField(label='Name', max_length=100)
    initial_category = forms.CharField(label='Category', max_length=100)
    initial_price = forms.DecimalField(label='Price', max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super(EditFoodForm, self).__init__(*args, **kwargs)
        if instance:
            ingred_data = json.loads(instance.ingred)
            for ingredient in Ingredient.objects.all():
                initial_quantity = ingred_data.get(ingredient.name, 0)
                field_name = f"ingredient_{ingredient.id}"
                self.fields[field_name] = forms.IntegerField(label=ingredient.name, min_value=0, initial=initial_quantity)


class EditMealForm(forms.Form):
    initial_name = forms.CharField(label='Name', max_length=100)
    initial_price = forms.DecimalField(label='Price', max_digits=10, decimal_places=2)
    foods = forms.ModelMultipleChoiceField(queryset=Food.objects.all(), widget=forms.SelectMultiple)

    def __init__(self, *args, **kwargs):
        meal_instance = kwargs.pop('meal_instance', None)
        super(EditMealForm, self).__init__(*args, **kwargs)
        if meal_instance:
            self.fields['foods'].initial = meal_instance.foods.all()


class AddIngredientForm(forms.Form):
    ingredient_name = forms.CharField(label='Ingredient Name', max_length=100)
    ingredient_quantity = forms.IntegerField(label='Quantity')

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
    start_date = forms.DateField(
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
    start_time = forms.TimeField(
        required=True,
        widget=forms.TimeInput(format="%H:%i:%s", attrs={"type": "time"}),
        input_formats=["%H:%i:%s"]
    )
    end_date = forms.DateField(
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
    end_time = forms.DateTimeField(
        required=True,
        widget=forms.TimeInput(format="%H:%i:%s", attrs={"type": "time"}),
        input_formats=["%H:%i:%s"]
    )
    