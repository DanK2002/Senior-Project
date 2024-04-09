import json
import random
from faker import Faker
from basic.models import Ingredient, Food, Meal, Employee, Shift, Order
from django.contrib.auth.models import User, Group
from datetime import timedelta
from django.utils import timezone

fake = Faker()
Faker.seed(7666777707777886)

# Genterate Groups
#Front of House
newGroup = Group(name = 'foh')
newGroup.save()
# Back of House
newGroup = Group(name = 'boh')
newGroup.save()
# manager
newGroup = Group(name = 'manager')
newGroup.save()

# generate employees (and associated users [and assign groups])
for x in range(5):
    fake_name = fake.name().split()
    first_name = fake_name[0]
    last_name = fake_name[-1]
    wage = round(random.uniform(10.0, 30.0), 2)
    username = f"{last_name.lower()}{random.randint(0, 99):02d}"
    try:
        user = User.objects.create(username=username, password="password123", first_name=first_name, last_name=last_name)
        employee = Employee.objects.create(user=user, wage=wage)
        if x == 1:
            man = Group.objects.get(name="manager")
            man.user_set.add(user)
        elif x < 4:
            foh = Group.objects.get(name="foh")
            foh.user_set.add(user)
        else:
            boh = Group.objects.get(name="foh")
            boh.user_set.add(user)
    except Exception as e:
        print(f"Error creating employee: {e}")

# generate shifts
for employee in Employee.objects.all():
    for x in range(3):
        start_time = fake.date_time_between(start_date='-30d', end_date='now', tzinfo=timezone.get_current_timezone())
        end_time = start_time + timedelta(hours=random.randint(4, 12))
        try:
            shift = Shift.objects.create(start=start_time, end=end_time, employee=employee)
        except Exception as e:
            print(f"Error creating shift: {e}")


# Define ingredients and their quantities using a dictionary
ingredients_data = {
    'Burger Bun': 2000,
    'Hot Dog Bun': 2000,
    'Lettuce': 500,
    'Beef Patty': 1500,
    'Crab Patty': 1000,
    'Sliced American Cheese': 1000,
    'Sliced Cheddar Cheese': 1000,
    'Hot Dog': 1500,
    'Beef Topping': 3000,
    'Onion': 500,
    'Pepper': 5000,
    'Salt': 5000,
    'Frozen Fries': 2000,
    'Frozen Onion Rings': 2000,
    'Seaweed': 1000,
    'Ketchup': 5000,
    'Mustard': 5000,
    'Mayo': 5000,
    'Pizza Dough': 1000,
    'Marinara Sauce': 5000,
    'Shredded Mozarella': 1000,
    'Parmesan Cheese': 1000,
    'Orange Soda': 2500,
    'Dr Kelp': 2500,
    'Diet Dr Kelp': 2500
}

# Loop through the ingredients dictionary and save each ingredient
i = 0
for ingredient_name, quantity in ingredients_data.items():
    ingredient = Ingredient(name=ingredient_name, quantity=quantity, idnumber=i)
    ingredient.save()
    i += 1

# Define foods and their ingredients using dictionaries
foods_data = [
    {
        'menu': True,
        'code': '',
        'name': 'Krabby Patty',
        'price': 5.99,
        'category': 'Sandwich',
        'ingredients': {'Burger Bun': 2, 'Crab Patty': 1, 'Sliced American Cheese': 1, 'Lettuce': 1, 'Onion': 1, 'Ketchup': 2, 'Mustard': 2}
    },
    {
        'menu': True,
        'code': '',
        'name': 'Krusty Dog',
        'price': 3.99,
        'category': 'Sandwich',
        'ingredients': {'Hot Dog Bun': 1, 'Hot Dog': 1, 'Ketchup': 2, 'Mustard': 2}
    },
    {
        'menu': True,
        'code': '',
        'name': 'Steamed Hams',
        'price': 4.99,
        'category': 'Sandwich',
        'ingredients': {'Burger Bun': 2, 'Beef Patty': 1, 'Sliced American Cheese': 1, 'Ketchup': 2, 'Mayo': 2}
    },
    {
        'menu': True,
        'code': '',
        'name': 'Good Burger',
        'price': 4.99,
        'category': 'Sandwich',
        'ingredients': {'Burger Bun': 2, 'Beef Patty': 1, 'Sliced Cheddar Cheese': 1, 'Onion': 1, 'Ketchup': 2, 'Mayo': 2}
    },
    {
        'menu': True,
        'code': '',
        'name': 'Krusty Krab Pizza',
        'price': 10.99,
        'category': 'Pizza',
        'ingredients': {'Pizza Dough': 1, 'Marinara Sauce': 2, 'Shredded Mozarella': 2, 'Parmesan Cheese': 1}
    },
    {
        'menu': True,
        'code': '',
        'name': 'None Pizza With Left Beef',
        'price': 8.99,
        'category': 'Pizza',
        'ingredients': {'Pizza Dough': 1, 'Beef Topping': 2}
    },
    {
        'menu': True,
        'code': '',
        'name': 'Fries',
        'price': 2.99,
        'category': 'Side',
        'ingredients': {'Frozen Fries': 2, 'Salt': 2}
    },
    {
        'menu': True,
        'code': '',
        'name': 'Onion Rings',
        'price': 2.99,
        'category': 'Side',
        'ingredients': {'Frozen Onion Rings': 2}
    },
    {
        'menu': True,
        'code': '',
        'name': 'Seaweed Salad',
        'price': 1.99,
        'category': 'Side',
        'ingredients': {'Seaweed': 2, 'Pepper': 1}
    },
    {
        'menu': True,
        'code': '',
        'name': 'Orange Soda',
        'price': 1.99,
        'category': 'Drink',
        'ingredients': {'Orange Soda': 1}
    },
    {
        'menu': True,
        'code': '',
        'name': 'Dr Kelp',
        'price': 1.99,
        'category': 'Drink',
        'ingredients': {'Dr Kelp': 1}
    },
    {
        'menu': True,
        'code': '',
        'name': 'Diet Dr Kelp',
        'price': 1.99,
        'category': 'Drink',
        'ingredients': {'Diet Dr Kelp': 1}
    }
]

### Code to dynamically generate unique food codes
# Dictionary to store used letters for category and foos
used_letters = {'categories': set(), 'foods': set()}
cat_letters = {}
food_letters = {}

# Dictionary to store counts for category - food pair
counts = {}

for food in foods_data:
    category = food['category']
    food_name = food['name']
    
    # Extract the first letter of the category for the code
    category_letter = category[0].upper()
    
    # If the first letter is already used, find the next available letter
    if category not in cat_letters.keys():
        while category_letter in cat_letters.values():
            category_letter = chr(ord(category_letter) + 1)
        
    # Extract the first letter of the food name for the code
    food_letter = food_name[0].upper()
    
    # If the first letter is already used, find the next available letter
    if food_name not in food_letters.keys():
        while food_letter in food_letters.values():
            food_letter = chr(ord(food_letter) + 1)
        
    # Update used letters
    if category not in cat_letters.keys():
        cat_letters[category] = category_letter
    if food_name not in food_letters.keys():
        food_letters[food_name] = food_letter
    
    # Update counts dictionary
    pair = (category_letter, food_letter)
    counts[pair] = counts.get(pair, 0) + 1
    
    # Generate code
    code = category_letter + food_letter + str(counts[pair])
    
    # Assign code to the food itee
    food['code'] = code

# Loop through the foods list and save each food
for food_data in foods_data:
    print(food_data)
    ingredient_list = json.dumps(food_data['ingredients'])
    food = Food(menu=food_data['menu'], code=food_data['code'], name=food_data['name'], 
                price=food_data['price'], category=food_data['category'], ingred=ingredient_list)
    food.save()

# Define meals and their foods using dictionaries
meals_data = [
    {
        'name': 'Good Meal',
        'price': 9.99,
        'foods': ['Good Burger', 'Fries', 'Orange Soda']
    },
    {
        'name': 'Krabby Patty Combo',
        'price': 10.99,
        'foods': ['Krabby Patty', 'Fries', 'Dr Kelp']
    }
]

# Loop through the meals list and save each meal
for meal_data in meals_data:
    meal = Meal(name=meal_data['name'], price=meal_data['price'])
    meal.save()
    for food_name in meal_data['foods']:
        food = Food.objects.filter(name=food_name).first()
        meal.foods.add(food)
    meal.save()

fake = Faker()

start_times = [fake.date_time_between(start_date='-1d', end_date='now', tzinfo=timezone.get_current_timezone()),
               fake.date_time_between(start_date='-1d', end_date='now', tzinfo=timezone.get_current_timezone()),
               fake.date_time_between(start_date='-1d', end_date='now', tzinfo=timezone.get_current_timezone()),]

emp =  User.objects.exclude(username='senato68').filter().first()
print("Employee submitted: ", emp)

orders_data = [
    {
        'number': 1,
        'time_est': start_times[0] + timedelta(minutes=9),
        'time_submitted': start_times[0],
        'time_completed': start_times[0] + timedelta(minutes=9),
        'foods': ['Krabby Patty', 'Krusty Dog', 'Fries'],
        'meals': [],
        'price': 13.97,
        'employee_submitted': emp,
    },
    {
        'number': 2,
        'time_est': start_times[1] + timedelta(minutes=10),
        'time_submitted': start_times[1],
        'time_completed': start_times[1] + timedelta(minutes=9),
        'foods': [],
        'meals': ['Good Meal'],
        'price': 9.99,
        'employee_submitted': emp,
    },
    {
        'number': 3,
        'time_est': start_times[2] + timedelta(minutes=3),
        'time_submitted': start_times[2],
        'time_completed': start_times[2] + timedelta(minutes=4),
        'foods': ['Steamed Hams', 'Krusty Dog'],
        'meals': ['Good Meal'],
        'price': 19.97,
        'employee_submitted': emp,
    }
]

print("order made")

for order_data in orders_data:
    print("in the loop")
    user_exists = User.objects.get(username=order_data['employee_submitted'])
    print(user_exists)
    print('username valid')
    order = Order(number = order_data['number'],
                  time_est = order_data['time_est'],
                  time_submitted = order_data['time_submitted'],
                  time_ready = None,
                  time_completed = order_data['time_completed'],
                  price = order_data['price'],
                  employee_submitted = user_exists,
                  message = '')
    print('order created')
    order.save()
    print('order saved')
    for food_name in order_data['foods']:
        food = Food.objects.filter(name=food_name).first()
        order.foods.add(food)
    print('foods saved')
    for meal_name in order_data['meals']:
        meal = Meal.objects.filter(name=meal_name).first()
        order.meals.add(meal)
    print('meals saved')
    order.save()

