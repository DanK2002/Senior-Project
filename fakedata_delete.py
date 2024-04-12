# Import required models
from django.contrib.auth.models import User
from basic.models import Employee, Shift, Order, Ingredient, Food, Meal, Group

# Retrieve the superuser by username
superuser = User.objects.get(username='senato68')

# Clear all tables except the superuser
User.objects.exclude(username=superuser.username).delete()
Employee.objects.all().delete()
Group.objects.delete()
Shift.objects.all().delete()
Order.objects.all().delete()
Ingredient.objects.all().delete()
Food.objects.all().delete()
Meal.objects.all().delete()

