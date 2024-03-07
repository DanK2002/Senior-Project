import json
from faker import Faker
from basic.models import Ingredient, Food, Meal

newObject = Ingredient(name='Burger Bun', quantity=2000)
newObject.save()

newObject = Ingredient(name='Hot Dog Bun', quantity=2000)
newObject.save()

newObject = Ingredient(name='Lettuce', quantity=500)
newObject.save()

newObject = Ingredient(name='Beef Patty', quantity=1500)
newObject.save()

newObject = Ingredient(name='Crab Patty', quantity=1000)
newObject.save()

newObject = Ingredient(name='Sliced American Cheese', quantity=1000)
newObject.save()

newObject = Ingredient(name='Sliced Cheddar Cheese', quantity=1000)
newObject.save()

newObject = Ingredient(name='Hot Dog', quantity=1500)
newObject.save()

newObject = Ingredient(name='Beef Topping', quantity=3000)
newObject.save()

newObject = Ingredient(name='Onion', quantity=500)
newObject.save()

newObject = Ingredient(name='Pepper', quantity=5000)
newObject.save()

newObject = Ingredient(name='Salt', quantity=5000)
newObject.save()

newObject = Ingredient(name='Frozen Fries', quantity=2000)
newObject.save()

newObject = Ingredient(name='Frozen Onion Rings', quantity=2000)
newObject.save()

newObject = Ingredient(name='Seaweed', quantity=1000)
newObject.save()

newObject = Ingredient(name='Ketchup', quantity=5000)
newObject.save()

newObject = Ingredient(name='Mustard', quantity=5000)
newObject.save()

newObject = Ingredient(name='Mayo', quantity=5000)
newObject.save()

newObject = Ingredient(name='Pizza Dough', quantity=1000)
newObject.save()

newObject = Ingredient(name='Marinara Sauce', quantity=5000)
newObject.save()

newObject = Ingredient(name='Shredded Mozarella', quantity=1000)
newObject.save()

newObject = Ingredient(name='Parmesan Cheese', quantity=1000)
newObject.save()

newObject = Ingredient(name='Orange Soda', quantity=2500)
newObject.save()

newObject = Ingredient(name='Dr Kelp', quantity=2500)
newObject.save()

newObject = Ingredient(name='Diet Dr Kelp', quantity=2500)
newObject.save()

x = { 
    'Burger Bun': 2,
    'Crab Patty': 1,
    'Sliced American Cheese': 1,
    'Lettuce': 1,
    'Onion': 1,
    'Ketchup': 2,
    'Mustard': 2
}
newIngredientList = json.dumps(x)
newObject1 = Food(name='Krabby Patty', price=5.99, category='Sandwich', ingred=newIngredientList)
newObject1.save()

x = { 
    'Hot Dog Bun': 1,
    'Hot Dog': 1,
    'Ketchup': 2,
    'Mustard': 2
}
newIngredientList = json.dumps(x)
newObject2 = Food(name='Krusty Dog', price=3.99, category='Sandwich', ingred=newIngredientList)
newObject2.save()

x = { 
    'Burger Bun': 2,
    'Beef Patty': 1,
    'Sliced American Cheese': 1,
    'Ketchup': 2,
    'Mayo': 2
}
newIngredientList = json.dumps(x)
newObject3 = Food(name='Steamed Hams', price=4.99, category='Sandwich', ingred=newIngredientList)
newObject3.save()

x = { 
    'Burger Bun': 2,
    'Beef Patty': 1,
    'Sliced Cheddar Cheese': 1,
    'Onion': 1,
    'Ketchup': 2,
    'Mayo': 2
}
newIngredientList = json.dumps(x)
newObject4 = Food(name='Good Burger', price=4.99, category='Sandwich', ingred=newIngredientList)
newObject4.save()

x = { 
    'Pizza Dough': 1,
    'Marinara Sauce': 2,
    'Shredded Mozarella': 2,
    'Parmesan Cheese': 1
}
newIngredientList = json.dumps(x)
newObject5 = Food(name='Krusty Krab Pizza', price=10.99, category='Pizza', ingred=newIngredientList)
newObject5.save()

x = { 
    'Pizza Dough': 1,
    'Beef Topping': 2
}
newIngredientList = json.dumps(x)
newObject6 = Food(name='None Pizza With Left Beef', price=8.99, category='Pizza', ingred=newIngredientList)
newObject6.save()

x = { 
    'Frozen Fries': 2,
    'Salt': 2
}
newIngredientList = json.dumps(x)
newObject7 = Food(name='Fries', price=2.99, category='Side', ingred=newIngredientList)
newObject7.save()

x = { 
    'Frozen Onion Rings': 2
}
newIngredientList = json.dumps(x)
newObject8 = Food(name='Onion Rings', price=2.99, category='Side', ingred=newIngredientList)
newObject8.save()

x = { 
    'Seaweed': 2,
    'Pepper': 1
}
newIngredientList = json.dumps(x)
newObject9 = Food(name='Seaweed Salad', price=1.99, category='Side', ingred=newIngredientList)
newObject9.save()

x = { 
    'Orange Soda': 1
}
newIngredientList = json.dumps(x)
newObject10 = Food(name='Orange Soda', price=1.99, category='Drink', ingred=newIngredientList)
newObject10.save()

x = { 
    'Dr Kelp': 1
}
newIngredientList = json.dumps(x)
newObject11 = Food(name='Dr Kelp', price=1.99, category='Drink', ingred=newIngredientList)
newObject11.save()

x = { 
    'Diet Dr Kelp': 1
}
newIngredientList = json.dumps(x)
newObject12 = Food(name='Diet Dr Kelp', price=1.99, category='Drink', ingred=newIngredientList)
newObject12.save()

newObject = Meal(name='Good Meal', price=9.99)
newObject.save()
newObject.foods.add(newObject4, newObject7, newObject10)
newObject.save()

newObject = Meal(name='Krabby Patty Combo', price=10.99)
newObject.save()
newObject.foods.add(newObject1, newObject7, newObject11)
newObject.save()