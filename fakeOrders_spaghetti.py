from basic.models import Food, Meal, Order, Employee, User
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
        'employee_submitted' : 'conner27',
    },
    {
        'number' : 2,
        'time_est' : timedelta(minutes=6),
        'time_submitted' : datetime(2024, 3, 2, 11, 24, 48, 595341),
        'time_completed' : datetime(2024, 3, 2, 11, 45, 13, 762390),
        'foods' : [],
        'meals' : ['Good Meal'],
        'price' : 9.99,
        'employee_submitted' : 'conner27',
    },
    {
        'number' : 3,
        'time_est' : timedelta(minutes=16),
        'time_submitted' : datetime(2024, 3, 6, 12, 5, 47, 178930),
        'time_completed' : datetime(2024, 3, 6, 12, 12, 9, 762904),
        'foods' : ['Steamed Hams', 'Steamed Hams'],
        'meals' : ['Good Meal'],
        'price' : 19.97,
        'employee_submitted' : 'conner27',
    }
]


user_obj = User.objects.get(username='conner27')
print(user_obj)
order = Order(number = 1, time_est = timedelta(minutes=9), time_submitted = datetime(2024, 2, 28, 16, 55), time_completed = datetime(2024, 2, 28, 17, 6), price = 13.97, employee_submitted = Employee.objects.get(user=user_obj))
order.save()