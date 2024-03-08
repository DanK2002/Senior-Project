from basic.models import Food, Ingredient
import json

food_data = {
        'name': 'Krabby Patty',
        'price': 5.99,
        'category': 'Sandwich',
        'ingredients': {'Burger Bun': 2, 'Crab Patty': 1, 'Sliced American Cheese': 1, 'Lettuce': 1, 'Onion': 1, 'Ketchup': 2, 'Mustard': 2}
    }

ingredient_list = json.dumps(food_data['ingredients'])
food = Food(name=food_data['name'], price=food_data['price'], category=food_data['category'], ingred=ingredient_list)
print(food.ingred)

food.ingred = {'Burger Bun': 2, 'Crab Patty': 1, 'Sliced American Cheese': 1, 'Lettuce': 1, 'Onion': 1, 'Parmesean': 1, 'Ketchup': 2, 'Mustard': 2}
print(food.ingred)