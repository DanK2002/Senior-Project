import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.utils import timezone
from .forms import *
from django.contrib.auth import authenticate, login as auth_login
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


# Create your views here.

# Home
def home(request):
    return render(request, "basic/home.html")

# Computation function
def compute(request):
    if request.method == 'POST':
        try:
            input = int(request.POST.get('input'))
            precomputed = Computed.objects.filter(input=input)
            if precomputed.count() != 0:  
                # This was already computed, so look up answer
                answer = precomputed[0].output
                time_computed = precomputed[0].time_computed
            else:
                # Compute the answer
                answer = input**2
                time_computed = timezone.now()
                # Save it into the database
                computed = Computed(
                    input=input, 
                    output=answer,
                    time_computed=time_computed
                )
                computed.save() # Store it into the database
        except:
            raise Http404(f"Invalid input: {request.POST.get('input')}")
        return render (
            request,
            "basic/compute.html",
            {
                'input': input,
                'output': answer,
                'time_computed': time_computed
            }
        )
    else:
        # Return a blank form
        return render(
            request, 
            'basic/compute.html'
        )
            
#Search Function
def search(request):
    if request.method == 'POST':
        try:
            input = int(request.POST.get('input'))
            precomputed = Computed.objects.filter(input=input)
            if precomputed.count() != 0:  
                # This was already computed, so look up answer
                answer = precomputed[0].output
                time_computed = precomputed[0].time_computed
            else:
                # redirect stuff here
                return render(
                    request, 
                    'basic/search.html',
                    {
                        'input': input,
                        'output': None,
                        'searched': True,
                    }
                )       
        except:
            raise Http404(f"Invalid input: {request.POST.get('input')}")
        return render (
            request,
            "basic/search.html",
            {
                'input': input,
                'output': answer,
                'searched': True,
                'time_computed': time_computed
            }
        )
    else:
        # Return a blank form
        return render(
            request, 
            'basic/search.html', 
            {
                'searched': False,
            }
        )

# Billie's Domain -------------------------------------------------------------------------------------
# For managing employees in the managerial section
def manageemployees(request):
    employees = Employee.objects.all()
    users = User.objects.all()      
    list_all_employees = render(
        request,
        "basic/partials/view_all_employees.html",
        {
            'employees' : employees,
            'users' : users,
        }
    ).content.decode('utf-8')
    print("RESET")

    # If no actions have occurred, render the page with just employees
    return render(
        request,
        "basic/manageemployees.html",
        {
            'list_all_employees' : list_all_employees
        }
    )

# User wants to add new employee; displays add employee form
def new_employee_form(request):
    print(request.POST)         # For debugging purposes; logs request in console
    form =  AddEmployeeForm()
    return render(
        request,
        "basic/partials/new_employee.html",
        {
            'add_form' : form,
        }
    )
    
# User wants to add a new employee and has already submitted the form          
def save_new_employee(request):
    employees = Employee.objects.all()
    users = User.objects.all()
    newUser = User.objects.create(                     # Add a new user based on form input
                username = request.POST.get('username'),
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
            )
    newEmployee = Employee.objects.create(user=newUser, wage=request.POST.get('wage'))
    return render(
        request,
        "basic/partials/view_one_employee.html",
        {
            'selectedUser' : newUser,
            'selectedEmployee' : newEmployee,
            'shifts' : []
        }
    )

# User wants to view information about a specific employee
def view_employee(request):
    selectedUsername = request.POST.get('select-employees')     # Get the username requested
    selectedUser = User.objects.get(username=selectedUsername)  # Find that user
    selectedEmployee = Employee.objects.get(user=selectedUser)  # And the employee linked to it
    shifts = Shift.objects.filter(employee = selectedEmployee)  # Find all of their shifts
    return render(
        request,
        "basic/partials/view_one_employee.html",
        {
            'selectedUser' : selectedUser,
            'selectedEmployee' : selectedEmployee,
            'shifts' : shifts,
        }
    )

# User wants to edit an existing employee; display the form
def edit_employee(request):
    selectedUsername = request.POST.get('user')                 # Get the username requested
    selectedUser = User.objects.get(username=selectedUsername)  # Find that user
    selectedEmployee = Employee.objects.get(user=selectedUser)  # And the employee linked to it
    shifts = Shift.objects.filter(employee = selectedEmployee)  # And their related shifts

    # Populate the form with pre-existing data
    editEmployee = EditEmployeeForm({"first_name": selectedUser.first_name,
                                    "last_name": selectedUser.last_name,
                                    "wage" : selectedEmployee.wage})
    return render(
        request,
        "basic/partials/edit_employee.html",
        {
            'selectedUser': selectedUser,
            'selectedEmployee': selectedEmployee,
            'editEmployee' : editEmployee,
        }
    )

# User has edited an existing employee and wants to save changes
def save_existing_employee(request):
    print("Saving employee...")
    print(request.POST)
    selectedUsername = request.POST.get('user')                 # Get the username requested
    selectedUser = User.objects.get(username=selectedUsername)  # Find that user
    selectedEmployee = Employee.objects.get(user=selectedUser)  # And the employee linked to it
    shifts = Shift.objects.filter(employee = selectedEmployee)  # And their related shifts
    if (request.POST.get('first_name') != None):
        selectedUser.first_name = request.POST.get('first_name')
    if (request.POST.get('last_name') != None):
        selectedUser.last_name = request.POST.get('last_name')
    if (request.POST.get('wage') != None):
        selectedEmployee.wage = request.POST.get('wage')
    selectedUser.save()
    selectedEmployee.save()
    return render(
        request,
        "basic/partials/view_one_employee.html",
        {
            'selectedUser' : selectedUser,
            'selectedEmployee' : selectedEmployee,
            'shifts' : shifts,
        }
    )

# User wants to remove an employee
def remove_employee(request):
    print("Removing Employee...")
    print(request.POST)
    employees = Employee.objects.all()
    users = User.objects.all()
    selectedUsername = request.POST.get('select-employees')     # Get the username requested
    selectedUser = User.objects.get(username=selectedUsername)  # Find that user
    selectedEmployee = Employee.objects.get(user=selectedUser)  # And the employee linked to it
    employeeName = selectedUser.first_name + selectedUser.last_name
    print(selectedUser.first_name + selectedUser.last_name)
    Shift.objects.filter(employee = selectedEmployee).delete()  # Delete their shifts
    Employee.objects.get(user = selectedUser).delete()          # Delete the employee
    User.objects.get(username = selectedUsername).delete()      # Delete the user
    return render(
        request,
        "basic/partials/remove_employee.html",
        {
            'name' : employeeName
        }
    )

def view_all_employees (request):
    users = User.objects.all()      
    print("Updating employee list")
    return render(
        request,
        "basic/partials/view_all_employees.html",
        {
            'users' : users
        }
    )

# End Billie's Domain ------------------------------------------------------

def managemenu(request):
    categories = Food.objects.values_list('category', flat=True).distinct()
    meals = Meal.objects.all()
    selected_category = None
    selected_food = None
    add_food_form = AddFoodForm()
    add_meal_form = AddMealForm()
    if request.method == 'POST':
        selected_category = request.POST.get('category')
        selected_food = request.POST.get('food')
    
    if selected_category:
        foods = Food.objects.filter(category=selected_category)
    else:
        foods = None
    
    return render(request, "basic/managemenu.html", 
                  {'categories': categories, 
                   'selected_category': selected_category,
                   'selected_food': selected_food,
                   'foods': foods,
                    'meals':meals, 'add_food_form': add_food_form, 'add_meal_form': add_meal_form})


def edit_category_form(request):
    # Retrieve the selected category from the POST data
    selected_category = request.GET.get('selected_category')

    return render(
        request,
        "basic/partials/edit_category_form.html",
        {'selected_category': selected_category}
    )


def edit_category(request):
    if request.method == 'POST':
        new_category_name = request.POST.get('new_category_name')
        selected_category = request.POST.get('selected_category')  # Retrieve from POST data, not from query parameters

        # Retrieve the food items with the selected category
        foods_to_update = Food.objects.filter(category=selected_category)
        # Update the category name for each food item
        for food in foods_to_update:
            food.category = new_category_name
            food.save()
        selected_category = new_category_name
        return JsonResponse({'Category name successfully changed': True})
    else:
        # Return a JSON response indicating failure
        return JsonResponse({'success': False, 'error': 'Invalid request'})

def add_food(request):
    if request.method == 'POST':
        form = AddFoodForm(request.POST)
        if form.is_valid():
            # Create a new Food object with form data
            new_food = Food(
                name=form.cleaned_data['name'],
                category=form.cleaned_data['category'],
                price=form.cleaned_data['price']
            )
                
            new_food.save()

            # Generate and assign food code
            food_code = add_food_code(new_food)
            new_food.code = food_code
            new_food.save()

            # Process ingredients and quantities
            ingred_data = {}
            for ingredient_name, quantity in request.POST.items():
                if ingredient_name.startswith('ingredient_'):
                    ingredient_name = ingredient_name.split('_')[1]
                    try:
                        quantity = int(quantity)
                        if quantity > 0:
                            ingred_data[ingredient_name] = quantity
                    except Ingredient.DoesNotExist:
                        pass

            # Update ingred field of the new food item and save
            new_food.ingred = ingred_data
            new_food.save()

            return redirect('basic:managemenu')
    else:
        form = AddFoodForm()
    return render(request, 'basic/partials/add_food.html', {'form': form})

def add_meal(request):
    if request.method == 'POST':
        form = AddMealForm(request.POST)
        if form.is_valid():
            # Create a new Food object with form data
            new_meal = Meal(
                name=form.cleaned_data['name'],
                price=form.cleaned_data['price']
            )
                
            new_meal.save()

            new_meal.foods.set(form.cleaned_data['foods'])
            # Generate and assign meal code
            meal_code = add_meal_code(new_meal)
            new_meal.code = meal_code
            new_meal.save()
            return redirect('basic:managemenu')
    else:
        form = AddMealForm()
    all_food_items = Food.objects.all()
    return render(request, 'basic/partials/add_meal.html', {'form': form, 'all_food_items':all_food_items})

def edit_view_food(request):
    edit_view_food_form = EditFoodForm()
    add_food_form = AddFoodForm()
    if request.method == 'POST':
        edit_view_food_form = EditFoodForm(request.POST)
        if edit_view_food_form.is_valid():
            new_name = edit_view_food_form.cleaned_data['initial_name']
            new_category = edit_view_food_form.cleaned_data['initial_category']
            new_price = edit_view_food_form.cleaned_data['initial_price']

            original_name = request.POST.get('original_name')
            original_food = get_object_or_404(Food, name=original_name)
            original_food.name = new_name
            original_food.category = new_category
            original_food.price = new_price

             # Process ingredients and quantities
            ingred_data = {}
            for ingredient_name, quantity in request.POST.items():
                if ingredient_name.startswith('ingredient_'):
                    ingredient_id = ingredient_name.split('_')[1]
                    try:
                        ingredient = Ingredient.objects.get(id=ingredient_id)
                        quantity = int(quantity)
                        if quantity >= 0:
                            ingred_data[ingredient.name] = quantity
                    except Ingredient.DoesNotExist:
                        return redirect('basic:managemenu')
            
            # Update the ingredients of the food
            original_food.ingred = ingred_data
            original_food.save()
            return render(request, 'basic/partials/edit_view_food.html', {'edit_view_food_form': edit_view_food_form})

    return render(request, 'basic/partials/edit_view_food.html', {'edit_view_food_form': edit_view_food_form})

def edit_view_meal(request):
    form = EditMealForm()
    add_meal_form = AddMealForm()
    if request.method == 'POST':
        form=EditMealForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data['initial_name']
            new_price = form.cleaned_data['initial_price']
            foods_selected = form.cleaned_data['foods']

            original_name = request.POST.get('original_name')
            original_meal = get_object_or_404(Meal, name=original_name)
            original_meal.name = new_name
            original_meal.price = new_price
            original_meal.foods.set(foods_selected)
            original_meal.save()
        return render(request, 'basic/partials/add_meal.html', {'form': form, 'add_meal_form': add_meal_form})
    return render(request, 'basic/partials/edit_view_food.html', {'form': form})

def remove_food(request):
    if request.method == 'POST':
        food_name = request.POST.get('original_name')
        food = Food.objects.filter(name=food_name).first()
        if food:
            food.delete()
            return JsonResponse({'message': 'Food item removed successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Food item not found'}, status=404)

def remove_meal(request):
    if request.method == 'POST':
        print("INHERE")
        meal_name = request.POST.get('meal_name')
        print(meal_name)
        meal = get_object_or_404(Meal, name=meal_name)
        meal.delete()
        print("DELETED")
        form = AddMealForm()
        return render(request, 'basic/partials/add_meal.html', {'form': form})
    else:
        print("IN HERE")
        return redirect('basic:managemenu')
    
def fetch_food_details(request):
    if request.method == 'GET':
        food_name = request.GET.get('food_name')
        food = Food.objects.get(name=food_name)
        initial_data = {
            'initial_name': food.name,
            'initial_category': food.category,
            'initial_price': food.price
        }
        form = EditFoodForm(initial = initial_data, instance=food)
        return render(request, 'basic/partials/edit_view_food.html',  {'form': form})

def fetch_meal_details(request):
    if request.method == 'GET':
        meal_name = request.GET.get('meal_name')
        meal = get_object_or_404(Meal, name=meal_name)
        form = EditMealForm(initial={'initial_name': meal.name, 'initial_price': meal.price},  meal_instance=meal)
        return render(request, 'basic/partials/edit_view_meal.html', {'form': form})
    
def update_food(request):
    if request.method == 'POST':
        selected_category = request.POST.get('category')
        selected_food = request.POST.get('food')
        print("Selected Category:", selected_category)
        print("Selected Food:", selected_food)
        return redirect('basic:managemenu', category=selected_category, food=selected_food)


def ingredient_list(request):
    if request.POST.get('original_name'):
        ingredients = Ingredient.objects.all().values_list('name', flat=True)
        selected_food = Food.objects.get(name=request.POST.get('original_name'))
        print(selected_food)
        ingred_list = selected_food.ingred
        print(ingred_list)
        return render(request, 'basic/partials/ingredient_list.html', {'ingredients': ingredients, 'ingred_list': ingred_list})
    else:
        ingredients = Ingredient.objects.all().values_list('name', flat=True)  # Get only the names
        return render(request, 'basic/partials/ingredient_list.html', {'ingredients': ingredients})

def add_food_code(new_food):
    # Dictionary to store used letters for category and foos
    cat_letters = {}
    food_letters = {}

    # Dictionary to store counts for category - food pair
    counts = {}

    foods = Food.objects.all()
    for food in foods:
        category = food.category
        food_name = food.name
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
        if (food == new_food):
            code = category_letter + food_letter + str(counts[pair])
            return code
        
def add_meal_code(new_meal):
    meals = Meal.objects.all()
    meal_letters = {}
    # Dictionary to store counts for category - food pair
    counts = {}
    for meal in meals:
        print("meal:" + meal.name)
        meal_name = meal.name
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
        if(meal == new_meal):
            code = meal_letter + str(counts[meal_letter])
            print("CODE:" + code)
            return code

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('basic:landingpage')
        else:
            error_message = "Invalid username or password."
            return render(request, 'basic/login.html', {'error_message': error_message})
    else:
        return render(request, "basic/login.html")
    
def landingpage(request):
    user = request.user
    groups = []
    for group in user.groups.all():
        groups.append(group.name)
    return render(request, 
                    "basic/landingpage.html",
                    {
                      'user': user,
                      'groups' : groups,
                    }
                )
         
# End Kayla's Domain ------------------------------------------------------


def inventory(request):
    ingredients = Ingredient.objects.distinct()

    return render(request, "basic/inventory.html", {'ingredients': ingredients})

def sales(request):
    return render(request, "basic/sales.html")

def order(request):
    return render(request, "basic/order.html")

def addneworder(request):
    return render(request, "basic/addneworder.html")

def inprogress(request):
    return render(request, "basic/inprogress.html")

def ready(request):
    return render(request, "basic/ready.html")

def completed(request):
    return render(request, "basic/completed.html")

def clockin_out(request):
    employee_list = Employee.objects.all()
    return render(
        request, 
        "basic/clockin-out.html", 
        {
            'employee_list': employee_list
        })

