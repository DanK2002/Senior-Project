import json
from faker import Faker
from basic.models import Ingredient, Food, Meal, Order, Employee, User
from datetime import timedelta, datetime
from django.utils import timezone

fake = Faker()

start_times = [fake.date_time_between(start_date='-1d', end_date='now', tzinfo=timezone.get_current_timezone()),
               fake.date_time_between(start_date='-1d', end_date='now', tzinfo=timezone.get_current_timezone()),
               fake.date_time_between(start_date='-1d', end_date='now', tzinfo=timezone.get_current_timezone())]

emp = User.objects.filter().first().username

orders_data = [
    {
        'number' : 1,
        'time_est' : start_times[0] + timedelta(minutes=9),
        'time_submitted' : start_times[0],
        'time_completed' : start_times[0] + timedelta(minutes=9),
        'foods' : ['Krabby Patty', 'Krusty Dog', 'Fries'],
        'meals' : [],
        'price' : 13.97,
        'employee_submitted' : emp,
    },
    {
        'number' : 2,
        'time_est' : start_times[1] + timedelta(minutes=6),
        'time_submitted' : start_times[1],
        'time_completed' : start_times[1] + timedelta(minutes=6),
        'foods' : [],
        'meals' : ['Good Meal'],
        'price' : 9.99,
        'employee_submitted' : emp,
    },
    {
        'number' : 3,
        'time_est' : start_times[2] + timedelta(minutes=16),
        'time_submitted' : start_times[2],
        'time_completed' : start_times[2] + timedelta(minutes=16),
        'foods' : ['Steamed Hams', 'Steamed Hams'],
        'meals' : ['Good Meal'],
        'price' : 19.97,
        'employee_submitted' : emp,
    }
]

for order_data in orders_data:
    order = Order(number = order_data['number'],
                  time_est = order_data['time_est'],
                  time_submitted = order_data['time_submitted'],
                  time_completed = order_data['time_completed'], 
                  price = order_data['price'], 
                  employee_submitted = User.objects.get(username=order_data['employee_submitted']))
    for food_name in order_data['foods']:
        food = Food.objects.filter(name=food_name).first()
        order.foods.add(food)
    for meal_name in order_data['meals']:
        meal = Meal.objects.filter(meal=meal_name).first()
        order.meals.add(meal)
    order.save()