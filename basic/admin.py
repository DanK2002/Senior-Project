from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Computed
from .models import Employee, Shift, Order, Meal, Food, Ingredient
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Computed)

##Project Models
admin.site.register(Employee)
admin.site.register(Shift)
admin.site.register(Order)
admin.site.register(Meal)
admin.site.register(Food)
admin.site.register(Ingredient)