import json
import random
from faker import Faker
from basic.models import Ingredient, Food, Meal, Employee, Shift, Order
from django.contrib.auth.models import User, Group
from datetime import timedelta
from django.utils import timezone
from django.db.models import IntegerField
from django.db.models.functions import Cast, Substr

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
        user = User.objects.create(username=username, password="Django@1", first_name=first_name, last_name=last_name)
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
categories = Food.objects.values_list('category', flat=True).distinct()
foods = Food.objects.values_list('name', flat=True).distinct()
cat_letters = {}
food_letters = {}

# Dictionary to store counts for category - food pair
counts = {}

for food in foods_data:
    category = food['category']
    food_name = food['name']
    # Extract the first letter of the category for the code
    index = 0
    category_letter = category[index].upper() 
    # If the first letter is already used, find the next available letter
    if category not in cat_letters.keys():
        while category_letter in cat_letters.values():
            index += 1
            category_letter = category[index].upper()
    else:
        category_letter = cat_letters[category]    
    # Extract the first letter of the food name for the code
    index = 0
    food_letter = food_name[0].upper()
    # If the first letter is already used, find the next available letter
    if food_name not in food_letters.keys():
        while food_letter in food_letters.values():
            index += 1
            food_letter = food_name[index].upper()
    else:
        food_letter = food_letters[food_name]   
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
    food = Food.objects.create(menu=food_data['menu'], code=food_data['code'], name=food_data['name'], 
                price=food_data['price'], category=food_data['category'], ingred=ingredient_list)

# Define meals and their foods using dictionaries
meals_data = [
    {
        'menu': True,
        'code': '',
        'name': 'Good Meal',
        'price': 9.99,
        'foods': ['Good Burger', 'Fries', 'Orange Soda']
    },
    {
        'menu': True,
        'code': '',
        'name': 'Krabby Patty Combo',
        'price': 10.99,
        'foods': ['Krabby Patty', 'Fries', 'Dr Kelp']
    }
]

meals = Food.objects.values_list('name', flat=True).distinct()
meal_letters = {}

### Code to dynamically generate unique food codes
# Dictionary to store counts for category - food pair
counts = {}
for meal in meals_data:
    meal_name = meal['name']
    # Extract the first letter of the meal name for the code
    index = 0
    meal_letter = meal_name[0].upper()
    # If the first letter is already used, find the next available letter
    if meal_name not in meal_letters.keys():
        while meal_letter in meal_letters.values():
            index += 1
            meal_letter = meal_name[index].upper()
    else:
        meal_letter = meal_letters[meal_name]
    # Update used letters
    if meal_name not in meal_letters.keys():
        meal_letters[meal_name] = meal_letter
    # Update counts dictionary
    counts[meal_letter] = counts.get(meal_letter, 0) + 1
    # Generate code
    code = meal_letter + str(counts[meal_letter])
    # Assign code to the meal itee
    meal['code'] = code
    print(meal)

# Loop through the meals list and save each meal
for meal_data in meals_data:
    meal = Meal.objects.create(menu=meal_data['menu'], code=meal_data['code'], name=meal_data['name'], price=meal_data['price'])
    for food_name in meal_data['foods']:
        # get the menu item
        food = Food.objects.filter(name=food_name, menu=True).first()
        meal.foods.add(food)
        
    meal.save()

fake = Faker()

start_times = [fake.date_time_between(start_date='-3d', end_date='now', tzinfo=timezone.get_current_timezone()),
               fake.date_time_between(start_date='-2d', end_date='now', tzinfo=timezone.get_current_timezone()),
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
        # get the menu item
        food = Food.objects.filter(name=food_name, menu=True).first()
        # Generate a new code from db data #
        code_cat = food.code[:1]
        code_food = food.code[1:2]
        #find the highest number code for this food type
        high_code = Food.objects.filter(
            code__startswith=code_cat + code_food
            ).annotate(
                code_number=Cast(Substr('code', 3), output_field=IntegerField())
            ).values_list('code', flat=True).order_by('-code_number').first()
        # Copy the highest number
        high_number = high_code[2:]
        # copy into a custom item
        food.pk = None
        food.code = f'{code_cat}{code_food}{str(int(high_number) + 1)}'
        food.menu = False
        food.message = "This is a test message"
        food.save()
        order.foods.add(food)
    print('foods saved')
    for meal_name in order_data['meals']:
        # get the menu item
        meal = Meal.objects.filter(name=meal_name, menu=True).first()
        old_meal = Meal.objects.filter(name=meal_name, menu=True).first()
        print(meal)
        # Generate a new code from db data #
        code_meal = meal.code[:1]
        
        high_code = Meal.objects.filter(
            code__startswith=code_meal
            ).annotate(
                code_number=Cast(Substr('code', 2), output_field=IntegerField())
            ).values_list('code', flat=True).order_by('-code_number').first()
        
        high_number = high_code[1:]
        # copy into a custom item
        meal.pk = None
        meal.code = f'{code_meal}{str(int(high_number) + 1)}'
        meal.menu = False
        meal.save()
        print(old_meal.foods.all())
        for food in old_meal.foods.all():
            print(food)
            old_code = food.code
            # Generate a new code from db data #
            code_cat = food.code[:1]
            code_food = food.code[1:2]
            
            high_code = Food.objects.filter(
                code__startswith=code_cat + code_food
                ).annotate(
                code_number=Cast(Substr('code', 3), output_field=IntegerField())
            ).values_list('code', flat=True).order_by('-code_number').first()
            
            high_number = high_code[2:]
            # copy into a custom item
            food.code = f'{code_cat}{code_food}{str(int(high_number) + 1)}'
            food.menu = False
            food.pk = None
            food.message = "This is a test message"
            food.save()
            meal.foods.add(food)
        order.meals.add(meal)
    print('meals saved')
    order.save()

