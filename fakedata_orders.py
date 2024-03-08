import json
from basic.models import Ingredient, Food, Meal, Order, Employee, User
from datetime import timedelta, datetime

orders_data = [
    {
        'number' : 1,
        'time_est' : timedelta(minutes=9),
        'time_submitted' : datetime(2024, 2, 28, 16, 55, 23, 562368),
        'time_completed' : datetime(2024, 2, 28, 17, 6, 57, 298540),
        'foods' : ['Krabby Patty', 'Krusty Dog', 'Fries'],
        'meals' : [],
        'price' : 13.97,
        'employee_submitted' : 'marks71',
    },
    {
        'number' : 2,
        'time_est' : timedelta(minutes=6),
        'time_submitted' : datetime(2024, 3, 2, 11, 24, 48, 595341),
        'time_completed' : datetime(2024, 3, 2, 11, 45, 13, 762390),
        'foods' : [],
        'meals' : ['Good Meal'],
        'price' : 9.99,
        'employee_submitted' : 'marks71',
    },
    {
        'number' : 3,
        'time_est' : timedelta(minutes=16),
        'time_submitted' : datetime(2024, 3, 6, 12, 5, 47, 178930),
        'time_completed' : datetime(2024, 3, 6, 12, 12, 9, 762904),
        'foods' : ['Steamed Hams', 'Steamed Hams'],
        'meals' : ['Good Meal'],
        'price' : 19.97,
        'employee_submitted' : 'marks71',
    }
]

#Continually get error for user does not exist
for order_data in orders_data:
    user_obj = User.objects.get(username=order_data['employee_submitted'])
    print(user_obj)
    order = Order(number = order_data['number'],
                  time_est = order_data['time_est'],
                  time_submitted = order_data['time_submitted'],
                  time_completed = order_data['time_completed'], 
                  price = order_data['price'], 
                  employee_submitted = Employee.objects.get(user=user_obj))
    for food_name in order_data['foods']:
        food = Food.objects.filter(name=food_name).first()
        order.foods.add(food)
    for meal_name in order_data['meals']:
        meal = Meal.objects.filter(meal=meal_name).first()
        order.meals.add(meal)
    order.save()
