import json
from faker import Faker
from basic.models import Ingredient, Food, Meal

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
for ingredient_name, quantity in ingredients_data.items():
    ingredient = Ingredient(name=ingredient_name, quantity=quantity)
    ingredient.save()

# Define foods and their ingredients using dictionaries
foods_data = [
    {
        'name': 'Krabby Patty',
        'price': 5.99,
        'category': 'Sandwich',
        'ingredients': {'Burger Bun': 2, 'Crab Patty': 1, 'Sliced American Cheese': 1, 'Lettuce': 1, 'Onion': 1, 'Ketchup': 2, 'Mustard': 2}
    },
    {
        'name': 'Krusty Dog',
        'price': 3.99,
        'category': 'Sandwich',
        'ingredients': {'Hot Dog Bun': 1, 'Hot Dog': 1, 'Ketchup': 2, 'Mustard': 2}
    },
    {
        'name': 'Steamed Hams',
        'price': 4.99,
        'category': 'Sandwich',
        'ingredients': {'Burger Bun': 2, 'Beef Patty': 1, 'Sliced American Cheese': 1, 'Ketchup': 2, 'Mayo': 2}
    },
    {
        'name': 'Good Burger',
        'price': 4.99,
        'category': 'Sandwich',
        'ingredients': {'Burger Bun': 2, 'Beef Patty': 1, 'Sliced Cheddar Cheese': 1, 'Onion': 1, 'Ketchup': 2, 'Mayo': 2}
    },
    {
        'name': 'Krusty Krab Pizza',
        'price': 10.99,
        'category': 'Pizza',
        'ingredients': {'Pizza Dough': 1, 'Marinara Sauce': 2, 'Shredded Mozarella': 2, 'Parmesan Cheese': 1}
    },
    {
        'name': 'None Pizza With Left Beef',
        'price': 8.99,
        'category': 'Pizza',
        'ingredients': {'Pizza Dough': 1, 'Beef Topping': 2}
    },
    {
        'name': 'Fries',
        'price': 2.99,
        'category': 'Side',
        'ingredients': {'Frozen Fries': 2, 'Salt': 2}
    },
    {
        'name': 'Onion Rings',
        'price': 2.99,
        'category': 'Side',
        'ingredients': {'Frozen Onion Rings': 2}
    },
    {
        'name': 'Seaweed Salad',
        'price': 1.99,
        'category': 'Side',
        'ingredients': {'Seaweed': 2, 'Pepper': 1}
    },
    {
        'name': 'Orange Soda',
        'price': 1.99,
        'category': 'Drink',
        'ingredients': {'Orange Soda': 1}
    },
    {
        'name': 'Dr Kelp',
        'price': 1.99,
        'category': 'Drink',
        'ingredients': {'Dr Kelp': 1}
    },
    {
        'name': 'Diet Dr Kelp',
        'price': 1.99,
        'category': 'Drink',
        'ingredients': {'Diet Dr Kelp': 1}
    }
]

# Loop through the foods list and save each food
for food_data in foods_data:
    ingredient_list = json.dumps(food_data['ingredients'])
    food = Food(name=food_data['name'], price=food_data['price'], category=food_data['category'], ingred=ingredient_list)
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

