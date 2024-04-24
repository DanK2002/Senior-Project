# Import required models
from django.contrib.auth.models import User
from basic.models import Employee, Shift, Order, Ingredient, Food, Meal, Group

# Retrieve the superuser by username
superusers = ['weldon49', 'senato68', 'bryan',
             'dan', 'billie', 'ktswy', 'hgare']

# Clear all tables except the superuser
User.objects.exclude(username__in=superusers).delete()
Employee.objects.all().delete()
Group.objects.all().delete()
Shift.objects.all().delete()
Order.objects.all().delete()
Ingredient.objects.all().delete()
Food.objects.all().delete()
Meal.objects.all().delete()

