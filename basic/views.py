from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseRedirect
import json
from .models import *
from django.utils import timezone
from .forms import *
from django.contrib.auth import authenticate, login as auth_login, logout
from django.views.decorators.http import require_GET, require_POST
import csv
import json
from datetime import timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.db.models import IntegerField
from django.db.models.functions import Cast, Substr
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt


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
    users = User.objects.all()      
    list_all_employees = render(
        request,
        "basic/partials/view_all_employees.html",
        {
            'users' : users,
        }
    ).content.decode('utf-8')
    html_content = render(request, "basic/employees_html.html", {'list_all_employees' : list_all_employees}).content.decode('utf-8')
    css_content = render(request, "basic/employees_css.html").content.decode('utf-8')
    print("RESET")

    # If no actions have occurred, render the page with just employees
    return render(request, "basic/sidenav.html", { 
        'html_content': html_content,
        'css_content': css_content
    })

# User wants to add new employee; displays add employee form
def new_employee_form(request):
    print(request.POST)         # For debugging purposes; logs request in console
    form =  AddEmployeeForm()
    users = User.objects.all()
    return render(
        request,
        "basic/partials/new_employee.html",
        {
            'add_form' : form
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
    user_groups = request.POST.getlist('user_groups')
    # Add employee to selected groups:
    if "foh" in user_groups:
        foh = Group.objects.get(name="foh")
        foh.user_set.add(newUser)
    if "boh" in user_groups:
        boh = Group.objects.get(name="boh")
        boh.user_set.add(newUser)
    if "manager" in user_groups:
        manager = Group.objects.get(name="manager")
        manager.user_set.add(newUser)
    newEmployee = Employee.objects.create(user=newUser, wage=request.POST.get('wage'))
    inGroups = []
    for group in newUser.groups.all():
        inGroups.append(group.name)
    groups = []
    if "foh" in inGroups:
        groups.append("Front of House")
    if "boh" in inGroups:
        groups.append("Back of House")
    if "manager" in inGroups:
        groups.append("Manager")

    return render(
        request,
        "basic/partials/view_one_employee.html",
        {
            'selectedUser' : newUser,
            'selectedEmployee' : newEmployee,
            'shifts' : [],
            'groups' : groups,
            'users' : users
        }
    )

# User wants to view information about a specific employee
def view_employee(request):
    selectedUsername = request.POST.get('select-employees')     # Get the username requested
    selectedUser = User.objects.get(username=selectedUsername)  # Find that user
    selectedEmployee = Employee.objects.get(user=selectedUser)  # And the employee linked to it
    shifts = Shift.objects.filter(employee = selectedEmployee)  # Find all of their shifts
    inGroups = []
    for group in selectedUser.groups.all():
        inGroups.append(group.name)
    groups = []
    if "foh" in inGroups:
        groups.append("Front of House")
    if "boh" in inGroups:
        groups.append("Back of House")
    if "manager" in inGroups:
        groups.append("Manager")
    return render(
        request,
        "basic/partials/view_one_employee.html",
        {
            'selectedUser' : selectedUser,
            'selectedEmployee' : selectedEmployee,
            'shifts' : shifts,
            'groups' : groups
        }
    )

# User wants to edit an existing employee; display the form
def edit_employee(request):
    selectedUsername = request.POST.get('user')                 # Get the username requested
    selectedUser = User.objects.get(username=selectedUsername)  # Find that user
    selectedEmployee = Employee.objects.get(user=selectedUser)  # And the employee linked to it
    shifts = Shift.objects.filter(employee = selectedEmployee)  # And their related shifts
    inGroups = []
    for group in selectedUser.groups.all():
        inGroups.append(group.name)
    # Populate the form with pre-existing data
    editEmployee = EditEmployeeForm({"first_name": selectedUser.first_name,
                                    "last_name": selectedUser.last_name,
                                    "wage" : selectedEmployee.wage,
                                    "user_groups" : inGroups})
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
    user_groups = request.POST.getlist('user_groups')
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

    # Add employee to selected groups and remove from unselected:
    inGroups = []
    for group in selectedUser.groups.all():
        inGroups.append(group.name)
    foh = Group.objects.get(name="foh")
    boh = Group.objects.get(name="boh")
    manager = Group.objects.get(name="manager")
    if "foh" in user_groups:
        foh.user_set.add(selectedUser)
    elif "foh" in inGroups:
        foh.user_set.remove(selectedUser)
    if "boh" in user_groups:
        boh.user_set.add(selectedUser)
    elif "boh" in inGroups:
        boh.user_set.remove(selectedUser)
    if "manager" in user_groups:
        manager.user_set.add(selectedUser)
    elif "manager" in inGroups:
        manager.user_set.remove(selectedUser)
    
    inGroups = []
    for group in selectedUser.groups.all():
        inGroups.append(group.name)
    groups = []
    if "foh" in inGroups:
        groups.append("Front of House")
    if "boh" in inGroups:
        groups.append("Back of House")
    if "manager" in inGroups:
        groups.append("Manager")

    
    return render(
        request,
        "basic/partials/view_one_employee.html",
        {
            'selectedUser' : selectedUser,
            'selectedEmployee' : selectedEmployee,
            'shifts' : shifts,
            'groups' : groups
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
    first_name = selectedUser.first_name
    last_name = selectedUser.last_name
    print(selectedUser.first_name + selectedUser.last_name)
    Shift.objects.filter(employee = selectedEmployee).delete()  # Delete their shifts
    Employee.objects.get(user = selectedUser).delete()          # Delete the employee
    User.objects.get(username = selectedUsername).delete()      # Delete the user
    return render(
        request,
        "basic/partials/remove_employee.html",
        {
            'first_name' : first_name,
            'last_name' : last_name,
            'users' : users
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

# View employee shifts based on date filters
def view_shifts (request):
    print(request.POST)
    selectedUser = User.objects.get(username = request.POST.get('employee'))
    selectedEmployee = Employee.objects.get(user = selectedUser)
    if (request.POST.get('start') != ""):
        #Show shifts between start and end date
        if (request.POST.get('end') != ""):
            shifts = Shift.objects.filter(employee=selectedEmployee,
                                          start__gte = request.POST.get('start'),
                                          start__lte = request.POST.get('end')).order_by('start')
        #Show shifts after the start date
        else:
            shifts = Shift.objects.filter(employee=selectedEmployee, start__gte = request.POST.get('start')).order_by('start')
    elif (request.POST.get('end') != ""):
        #Show shifts before the end date
        shifts = Shift.objects.filter(employee=selectedEmployee, start__lte = request.POST.get('end')).order_by('start')
    else:
        #Show all shifts
        shifts = Shift.objects.filter(employee=selectedEmployee).order_by('start')
    totalTime = timedelta()
    for shift in shifts:
        duration = shift.end - shift.start
        totalTime += duration
    totalSeconds = totalTime.total_seconds()
    hours = totalSeconds // 3600
    minutes = (totalSeconds%3600) // 60
    return render(
        request,
        "basic/partials/view_shifts.html",
        {
            'shifts' : shifts,
            'hours' : hours,
            'minutes' : minutes
        }
    )

# User wants to view a list of employee's shifts
def edit_shifts(request):
    print("Showing shift list...")
    print(request)
    selectedUser = User.objects.get(username = request.POST.get('user'))
    selectedEmployee = Employee.objects.get(user = selectedUser)
    shifts = Shift.objects.filter(employee = selectedEmployee).order_by('start')
    print(shifts)
    return render(
        request,
        "basic/partials/edit_shifts.html",
        {
            'shifts' : shifts,
            'selectedUser' : selectedUser
        }
    )

# User wants the form to add a new shift
def add_shift(request):
    selectedUser = User.objects.get(username = request.POST.get('user'))
    shiftForm = EditEmployeeShifts()
    return render(
        request,
        "basic/partials/add_new_shift.html",
        {
            'newShiftForm' : shiftForm,
            'selectedUser' : selectedUser,
        }
    )

# User wants the form to edit an existing shift
def edit_shift(request):
    print("Editing shift...")
    print(request.POST.get('user'))
    print(request.POST.get('shift-list'))
    selectedUser = User.objects.get(username = request.POST.get('user'))
    selectedEmployee = Employee.objects.get(user = selectedUser)
    originalShift = Shift.objects.get(employee = selectedEmployee, start = request.POST.get('shift-list'))
    
    start_date = originalShift.start.strftime("%Y-%m-%d")
    start_time = originalShift.start.strftime("%H:%M:%S")
    end_date = originalShift.end.strftime("%Y-%m-%d")
    end_time = originalShift.end.strftime("%H:%M:%S")
    shiftForm = EditEmployeeShifts({
        "start_date" : start_date,
        "start_time" : start_time,
        "end_date" : end_date,
        "end_time" : end_time
    })
    return render(
        request,
        "basic/partials/edit_one_shift.html",
        {
            'editShiftForm' : shiftForm,
            'selectedUser' : selectedUser,
            'originalShift' : originalShift
        }
    )

# User wants to remove an existing shift
def remove_shift(request):
    selectedUser = User.objects.get(username = request.POST.get('user'))
    selectedEmployee = Employee.objects.get(user = selectedUser)
    Shift.objects.get(employee = selectedEmployee, start = request.POST.get('shift-list')).delete()
    shifts = Shift.objects.filter(employee = selectedEmployee).order_by('start')
    return render(
        request,
        "basic/partials/remove_shift.html",
        {
            'shifts' : shifts
        }
    )

# User wants to save changes to an existing shift
def save_existing_shift(request):
    print("Saving shift...")
    print(request.POST.get(''))
    if request.method == "POST":
        selectedUser = User.objects.get(username = request.POST.get('user'))
        selectedEmployee = Employee.objects.get(user = selectedUser)
        originalShift = Shift.objects.get(employee = selectedEmployee, start = request.POST.get('original-shift'))
        start_datetime = request.POST.get('start_date') + ' ' + request.POST.get('start_time')
        end_datetime = request.POST.get('end_date') + ' ' + request.POST.get('end_time')
        originalShift.start = start_datetime
        originalShift.end = end_datetime
        originalShift.save()
        shifts = Shift.objects.filter(employee = selectedEmployee).order_by('start')
        return render(
            request,
            "basic/partials/saved_shift.html",
            {
                "shifts" : shifts
            }
        )
    elif request.method == "GET":
        return render(
            request,
            ""
        )
    
# User wants to save a new shift
def save_new_shift(request):
    if request.method == "POST":
        selectedUser = User.objects.get(username = request.POST.get('user'))
        selectedEmployee = Employee.objects.get(user = selectedUser)
        start_datetime = request.POST.get('start_date') + ' ' + request.POST.get('start_time')
        end_datetime = request.POST.get('end_date') + ' ' + request.POST.get('end_time')
        Shift.objects.create(start = start_datetime,
                          end = end_datetime,
                          employee = selectedEmployee)
        shifts = Shift.objects.filter(employee = selectedEmployee).order_by('start')
        return render(
            request,
            "basic/partials/saved_shift.html",
            {
                'shifts' : shifts
            }
        )
    elif request.method == "GET":
        return render(
            request,
            ""
        )

# End Billie's Domain ------------------------------------------------------

def managemenu(request):
    selected_category = request.POST.get('category') #get selected category
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
        meal_name = request.POST.get('meal_name')
        print(meal_name)
        meal = get_object_or_404(Meal, name=meal_name)
        meal.delete()
        add_meal_form = AddMealForm()
        return render(request, 'basic/partials/add_meal.html', {'add_meal_form': add_meal_form})
    else:
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
    html_content = render(request, "basic/inventory_html.html", {'ingredients': ingredients}).content.decode('utf-8')
    css_content = render(request, "basic/inventory_css.html").content.decode('utf-8')
    return render(request, "basic/sidenav.html", { 
        'html_content': html_content,
        'css_content': css_content
    })

def quantity(request):
    ingredientID = int(request.POST.get("ingredient"))
    ingredients = Ingredient.objects.distinct()
    for ingredient in ingredients:
        if ingredient.idnumber == ingredientID:
            ing = ingredient
    # value = request.POST.get('amount')
    newValue = ing.quantity + int(request.POST[f'amount{ingredientID}'])
    if newValue < 0:
        newValue = 0
    ing.quantity = newValue
    ing.save()

    return render(request, "basic/partials/quantity.html", {'newValue': newValue})

def searchInventory(request):
    ingredientString = request.GET.get("ingredientname").upper()
    ingredients = Ingredient.objects.distinct()
    newIngredients = []
    for ingredient in ingredients:
        if ingredient.name.upper().find(ingredientString) != -1:
            newIngredients.append(ingredient)

    return render(request, "basic/partials/inventoryTable.html", {'ingredients': newIngredients})

def addIngredient(request):
    ingredients = Ingredient.objects.distinct()
    ingredientName = request.POST.get("ingredientTitle").strip()
    
    if ingredientName: # Check to see if the name is not the empty string
        nameExists = False
        for ingredient in ingredients:
            if ingredient.name.upper() == ingredientName.upper():
                nameExists = True
                break
        if not nameExists: # If the name is not already taken, add the ingredient
            ingredientAmount = int(request.POST.get("ingredientAmount"))
            if ingredientAmount < 0: # If trying to add negative amount, set to 0 by default
                ingredientAmount = 0
            ingredientID = ingredients.last().idnumber + 1 # Get the highest taken id and iterate for a new id
            ingredient = Ingredient(name=ingredientName, quantity=ingredientAmount, idnumber=ingredientID)
            ingredient.save()

    ingredients = Ingredient.objects.all()
    return render(request, "basic/partials/inventoryTable.html", {'ingredients': ingredients})

def removeIngredient(request):
    ingredientName = request.POST.get("removedIngredientTitle")
    ingredients = Ingredient.objects.distinct()
    for ingredient in ingredients:
        if ingredient.name.upper() == ingredientName.upper():
            ingredient.delete()
    ingredients = Ingredient.objects.distinct()
    return render(request, "basic/partials/inventoryTable.html", {'ingredients': ingredients})

def sales(request):
    html_content = render(request, "basic/sales_html.html").content.decode('utf-8')
    css_content = render(request, "basic/sales_css.html").content.decode('utf-8')
    return render(request, "basic/sidenav.html", { 
        'html_content': html_content, # div in sidenav
        'css_content': css_content # div in sidenav
    })

def salesSummary(request):
    str_start = request.GET.get('start_date')
    str_end = request.GET.get('end_date')

    if( str_start != '' and str_end != ''):
        start_date = datetime.strptime(str_start, '%Y-%m-%d')
        end_date = datetime.strptime(str_end, '%Y-%m-%d')

        orders = Order.objects.filter(time_completed__date__range=(start_date, end_date))
    else:
        orders = Order.objects.all()
    
    orders_total = 0

    foods_ind = defaultdict(int)
    foods_total = 0

    meals_ind = defaultdict(int)
    meals_total = 0
    
    for order in orders:
        orders_total += order.price
        for meal in order.meals.all():
            meals_ind[meal.name] += meal.price
            meals_total += meal.price
        for food in order.foods.all():
            foods_ind[food.name] += food.price
            foods_total += food.price

    meals_ind = dict(meals_ind)
    foods_ind = dict(foods_ind)
    foods_total = round(foods_total, 2)
    meals_total = round(meals_total, 2)

    return render(request, "basic/partials/sales_summary.html", {
        'orders_total': orders_total,
        'meals_ind': meals_ind,
        'meals_total': meals_total,
        'foods_ind': foods_ind,
        'foods_total': foods_total,
    })

def generateCsv(request):
    orders = Order.objects.all()
    orders_total = 0

    foods_ind = defaultdict(int)
    foods_total = 0

    meals_ind = defaultdict(int)
    meals_total = 0

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
    )
    
    for order in orders:
        orders_total += order.price
        for meal in order.meals.all():
            meals_ind[meal.name] += meal.price
            meals_total += meal.price
        for food in order.foods.all():
            foods_ind[food.name] += food.price
            foods_total += food.price

    meals_ind = dict(meals_ind)
    foods_ind = dict(foods_ind)
    foods_total = round(foods_total, 2)
    meals_total = round(meals_total, 2)

    writer = csv.writer(response)
    # Order Summary
    writer.writerow(['Category', 'Revenue'])
    writer.writerow(['Foods', foods_total])
    writer.writerow(['Meals', meals_total])
    writer.writerow(['Orders Total', orders_total])
    #spacer
    writer.writerow(['', ''])    
    # Meals Summary
    writer.writerow(['Meal', 'Revenue'])
    for meal_name, meal_revenue in meals_ind.items():
        writer.writerow([meal_name, meal_revenue])
    writer.writerow(['Meals Total', meals_total])
    #spacer
    writer.writerow(['', ''])    
    # Foods Summary
    writer.writerow(['Food', 'Revenue'])
    for food_name, food_revenue in foods_ind.items():
        writer.writerow([food_name, food_revenue])
    writer.writerow(['Foods Total', foods_total])

    return response

def order(request):
    return render(request, "basic/order.html")

def backorder(request):
    return render(request, "basic/back-order.html")

def addneworder(request):
    return render(request, "basic/addneworder.html")

def inprogress(request):
    in_progress_orders = Order.objects.filter(time_completed__isnull=True, time_ready__isnull=True)
    return render(
        request, 
        "basic/inprogress.html", 
        {
            'in_progress_orders': in_progress_orders
        })

def backinprogress(request):
    in_progress_orders = Order.objects.filter(time_completed__isnull=True, time_ready__isnull=True)
    return render(
        request, 
        "basic/back-inprogress.html", 
        {
            'in_progress_orders': in_progress_orders
        })

def mark_ready(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    # Update the time_ready field for the order
    order.time_ready = timezone.now()  # Assuming you have imported timezone
    order.save()
    message = "Order marked as ready!"
    return HttpResponse(message)

def ready(request):
    ready_orders = Order.objects.filter(time_completed__isnull=True, time_ready__isnull=False)
    return render(
        request, 
        "basic/ready.html", 
        {
            'ready_orders': ready_orders
        })

def backready(request):
    ready_orders = Order.objects.filter(time_completed__isnull=True, time_ready__isnull=False)
    return render(
        request, 
        "basic/back-ready.html", 
        {
            'ready_orders': ready_orders
        })

def completed(request):
    completed_orders = Order.objects.filter(time_completed__isnull=False)
    return render(
        request, 
        "basic/completed.html", 
        {
            'completed_orders': completed_orders
        })

def backcompleted(request):
    completed_orders = Order.objects.filter(time_completed__isnull=False)
    return render(
        request, 
        "basic/back-completed.html", 
        {
            'completed_orders': completed_orders
        })

def mark_completed(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    # Update the time_ready field for the order
    order.time_completed = timezone.now()  # Assuming you have imported timezone
    order.save()
    message = "Order marked as Completed!"
    return HttpResponse(message)

def remove_ready(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.time_ready = None
    order.save()
    message = "Order Reverted!"
    return HttpResponse(message)

def remove_completed(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.time_completed = None
    order.time_ready = timezone.now()
    order.save()
    message = "Order Reverted!"
    return HttpResponse(message)

def get_food_details(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    foods_list = [food.name for food in order.foods.all()]  # Assuming 'name' is the field you want to display
    food_details = ', '.join(foods_list)
    return JsonResponse(food_details, safe=False)

def clockin_out(request):
    users = User.objects.all().order_by("username")
    employees = Employee.objects.all()
    employeeUsernames = []
    for employee in employees:
        employeeUsernames.append(employee.user.username)
    currentShifts = Shift.objects.filter(end=None)
    clockedIn = []
    for shift in currentShifts:
        clockedIn.append(shift.employee.user.username)
    return render(
        request, 
        "basic/clockin-out.html", 
        {
            'users': users,
            'employeeUsernames': employeeUsernames,
            'clockedIn': clockedIn
        })

def modal(request):
    username = request.POST.get("username")
    return render(
        request, 
        "partials/modal.html",
        {
            'username': username
        })

def auth_clockin_out(request):
    currentShifts = Shift.objects.filter(end=None)
    
    clockedIn = []
    clockedInUsernames = []
    for shift in currentShifts:
        clockedIn.append(shift.employee.user)
        clockedInUsernames.append(shift.employee.user.username)

    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    
    if user is not None: # A backend authenticated the credentials
        employee = Employee.objects.get(user=user)
        if user in clockedIn: # Add an end time to the current Shift for this employee
            shift = currentShifts.get(employee=employee)
            shift.end = timezone.now()
            shift.save()
        else: # Create new Shift for this employee
            start = timezone.now()
            employee = Employee.objects.get(user=user)
            newShift = Shift(
                    start=start, 
                    end=None,
                    employee=employee
                )
            newShift.save() # Store it into the database
        return redirect('basic:clockin-out')
    else: # No backend authenticated the credentials
        return render(
            request, 
            "partials/modal.html",
            {
                'username': username
            })
    
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
@login_required
def ordercreation1(request):
    categories = Food.objects.values_list('category', flat=True).distinct()

    #fakeUser = User.objects.create(username='username', password="password", first_name='first_name', last_name='last_name')
    user = request.user

    orderNumber = len(Order.objects.distinct()) + 1

    order = Order(number = orderNumber, time_est = timezone.now(), time_submitted = timezone.now(),
                    employee_submitted = user, message = 'Order: Dine In')

    order.save()

    return render(request, "basic/ordercreation.html", {'categories': categories})

def ordercreation2(request):
    categories = Food.objects.values_list('category', flat=True).distinct()

    #fakeUser = User.objects.create(username='username', password="password", first_name='first_name', last_name='last_name')
    user = request.user

    orderNumber = len(Order.objects.distinct()) + 1

    order = Order(number = orderNumber, time_est = timezone.now(), time_submitted = timezone.now(),
                   price = 0.0, employee_submitted = user, message = 'Order: Take Out')

    order.save()

    return render(request, "basic/ordercreation.html", {'categories': categories})

def ordercreation3(request):
    categories = Food.objects.values_list('category', flat=True).distinct()

    #fakeUser = User.objects.create(username='username', password="password", first_name='first_name', last_name='last_name')
    user = request.user

    orderNumber = len(Order.objects.distinct()) + 1

    order = Order(number = orderNumber, time_est = timezone.now(), time_submitted = timezone.now(),
                   price = 0.0, employee_submitted = user, message = 'Order: Drive Through')

    order.save()

    return render(request, "basic/ordercreation.html", {'categories': categories})

def fooditems(request):
    categoryName = request.GET.get("categoryName")

    foods = Food.objects.distinct()
    newFoods = []
    for food in foods:
        if food.category.upper() == categoryName.upper():
            if food.menu == True:
                newFoods.append(food)

    return render(request, "basic/partials/fooditems.html", {'foods': newFoods, 'category': categoryName})

def customizeFood(request):
    if request.method == 'GET':
        foodName = request.GET.get("foodName")
        foods = Food.objects.distinct()
        for food in foods:
            if food.name.upper() == foodName.upper():
                if food.menu == True:
                    theFood = food
        allIngredients = Ingredient.objects.distinct()
        ingredientDictionary = json.loads(theFood.ingred)
        ingredientsInFoodNames = list(ingredientDictionary.keys())
        ingredientsInFood = []
        for ingredient in allIngredients:
            for ing in ingredientsInFoodNames:
                if ing.upper() == ingredient.name.upper():
                    ingredientsInFood.append(ingredient)
        notInFood = []
        inFood = False
        for ingredient in allIngredients:
            for ing in ingredientsInFoodNames:
                if ing.upper() == ingredient.name.upper():
                    inFood = True
            if not inFood:
                notInFood.append(ingredient)
            inFood = False
        return render(request, "basic/partials/customizeFood.html", {
            'food': theFood, 
            'inFood': ingredientsInFood,
            'notInFood': notInFood,
            'ingredientDictionary': ingredientDictionary            
            })

def amountchange(request):
    print(request.POST)
    id = request.POST.get("ingredientid")
    amountChange = int(request.POST[f'addition{id}'])

    if amountChange == -2:
        change = "None"
    elif amountChange == -1:
        change = "Less"
    elif amountChange == 0:
        change = "Standard"
    elif amountChange == 1:
        change = "Extra"
    elif amountChange == 2:
        change = "Extra Extra"
    else:
        change = "Invalid"

    return render(request, "basic/partials/amountchange.html", {'change':change})
                                                                 
def addFoodToOrder(request):
    foodName = request.POST.get("foodName")
    foods = Food.objects.distinct()
    for food in foods:
        if food.name.upper() == foodName.upper():
            if food.menu:
                theFood = food
    code_cat = theFood.code[:1]
    code_food = theFood.code[1:2]
    #find the highest number code for this food type
    high_code = Food.objects.filter(
        code__startswith=code_cat + code_food
        ).annotate(
            code_number=Cast(Substr('code', 3), output_field=IntegerField())
        ).values_list('code', flat=True).order_by('-code_number').first()
    # Copy the highest number
    high_number = high_code[2:]
    # copy into a custom item
    theFood.pk = None
    theFood.code = f'{code_cat}{code_food}{str(int(high_number) + 1)}'
    theFood.menu = False

    allIngredients = Ingredient.objects.distinct()
    ingredientDictionary = json.loads(theFood.ingred)
    ingredientsInFoodNames = list(ingredientDictionary.keys())
    ingredientsInFood = []
    for ingredient in allIngredients:
        for ing in ingredientsInFoodNames:
            if ing.upper() == ingredient.name.upper():
                ingredientsInFood.append(ingredient)

    notInFood = []
    inFood = False
    for ingredient in allIngredients:
        for ing in ingredientsInFoodNames:
            if ing.upper() == ingredient.name.upper():
                inFood = True
        if not inFood:
            notInFood.append(ingredient)
        inFood = False
    
    newIngredients = {}
    changesToFood = ''
    totalUpcharge = 0
    for x in request.POST:
        #find the ingredient with the id x that matches addition'x'
        if "addition" in str(x):
            additionID = int(str(x)[8:])
            isInFood = True
            for thisIngredient in ingredientsInFood:
                if additionID == thisIngredient.idnumber:
                    ingredient = thisIngredient
            for thisIngredient in notInFood:
                if additionID == thisIngredient.idnumber:
                    ingredient = thisIngredient
                    isInFood = False
            
            if isInFood:
                newAmount = ingredientDictionary.get(ingredient.name) + int(request.POST.get(str(x)))
            else:
                newAmount = int(request.POST.get(str(x)))
            
            if newAmount < 0 or int(request.POST.get(str(x))) == -1:
                newAmount = 0
            if int(request.POST.get(str(x))) == 2:
                changesToFood = changesToFood + "Add extra extra " + ingredient.name + ".\n"
                totalUpcharge += ingredient.upcharge
            elif int(request.POST.get(str(x))) == 1:
                changesToFood = changesToFood + "Add extra " + ingredient.name + ".\n"
                totalUpcharge += ingredient.upcharge
            elif int(request.POST.get(str(x))) == -1:
                if newAmount == 0:
                    changesToFood = changesToFood + "Remove " + ingredient.name + ".\n"
                else:
                    changesToFood = changesToFood + "Add less " + ingredient.name + ".\n"
            elif int(request.POST.get(str(x))) == -2:
                changesToFood = changesToFood + "Remove " + ingredient.name + ".\n"
            newIngredients[ingredient.name] = newAmount
    theFood.ingred = json.dumps(newIngredients)
    if changesToFood == '':
        changesToFood = "Standard ingredients.\n"
    changesToFood = changesToFood + request.POST.get("message")
    theFood.message = changesToFood
    theFood.price += totalUpcharge
    theFood.save()
    #use json.dumps(some dictionary) to pass json of ingredients

    orders = Order.objects.distinct()
    #note: this method of finding the current order will not work if multiple machines are creating
    #orders at once. This method should be tweaked.
    for currentOrder in orders:
        if currentOrder.number == len(Order.objects.distinct()):
            order = currentOrder
    order.foods.add(theFood)
    order.save()

    foodsInOrder = order.foods.all()
    mealsInOrder = order.meals.all()
    total = 0
    for food in foodsInOrder:
        total += food.price
    for meal in mealsInOrder:
        total += meal.price

    mealInstructions = []
    for meal in mealsInOrder:
        instruction = meal.name + ":\n"
        for food in meal.foods.all():
            instruction = instruction + food.name + "; " + food.message + ". "
        mealInstructions.append(instruction)

    return render(request, "basic/partials/addFoodToOrder.html", {'foodName':foodName, 'foodsInOrder': foodsInOrder,
                                                                  'total': total, 'mealInstructions': mealInstructions})

def meal_items(request):
    allMeals = Meal.objects.distinct()
    meals = []
    for meal in allMeals:
        if meal.menu == True:
            meals.append(meal)

    return render(request, "basic/partials/meal_items.html", {'meals': meals})

def customizeMeal(request):
    mealName = request.GET.get("mealName")
    meal = Meal.objects.filter(name__iexact=mealName, menu=True).first()
    
    foodsInMeal = meal.foods.all()
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

    for food in foodsInMeal:
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
        food.message = ""
        food.save()
        meal.foods.add(food)
    meal.save()

    return render(request, "basic/partials/customizeMeal.html", {'meal': meal, 'foods': meal.foods.all()})

def customizeFoodInMeal(request):
    if request.method == 'GET':
        foodCode = request.GET.get("foodCode")
        mealCode = request.GET.get("mealCode")
        theFood = Food.objects.filter(code=foodCode).first()

        ingredientDictionary = json.loads(theFood.ingred)

        ingredientsInFood = Ingredient.objects.filter(name__in=ingredientDictionary.keys())
        notInFood = Ingredient.objects.exclude(name__in=ingredientDictionary.keys())
 
        return render(request, "basic/partials/customizeFoodInMeal.html", {
            'food': theFood, 
            'inFood': ingredientsInFood,
            'notInFood': notInFood,
            'ingredientDictionary': ingredientDictionary,
            'mealCode': mealCode
            })

def editFoodInMeal(request):
    foodCode = request.POST.get("foodCode")
    mealCode = request.POST.get("mealCode")
    theFood = Food.objects.filter(code=foodCode).first()
    meal = Meal.objects.filter(code=mealCode).first()

    ingredientDictionary = json.loads(theFood.ingred)
    ingredientsInFood = Ingredient.objects.filter(name__in=ingredientDictionary.keys())
    notInFood = Ingredient.objects.exclude(name__in=ingredientDictionary.keys())
    '''
    <!-- min= "-{{ food.ingred[ingredient.name] }}"-->
    newIngredients = ingredientsInFood.copy()
    #compare amounts for message
    
    '''
    newIngredients = {}
    changesToFood = ''
    totalUpcharge = 0
    for x in request.POST:
        #find the ingredient with the id x that matches addition'x'
        if "addition" in str(x):
            additionID = int(str(x)[8:])
            isInFood = True

            for thisIngredient in ingredientsInFood:
                if additionID == thisIngredient.idnumber:
                    ingredient = thisIngredient
            for thisIngredient in notInFood:
                if additionID == thisIngredient.idnumber:
                    ingredient = thisIngredient
                    isInFood = False
            
            if isInFood:
                newAmount = ingredientDictionary.get(ingredient.name) + int(request.POST.get(str(x)))
            else:
                newAmount = int(request.POST.get(str(x)))
            
            if newAmount < 0 or int(request.POST.get(str(x))) == -1:
                newAmount = 0

            if int(request.POST.get(str(x))) == 2:
                changesToFood += f"Add extra extra {ingredient.name}.\n"
                totalUpcharge += ingredient.upcharge
            elif int(request.POST.get(str(x))) == 1:
                changesToFood += f"Add extra {ingredient.name}.\n"
                totalUpcharge += ingredient.upcharge
            elif int(request.POST.get(str(x))) == -1:

                if newAmount == 0:
                    changesToFood += f"Remove {ingredient.name}.\n"
                else:
                    changesToFood += f"Add less {ingredient.name}.\n"

            elif int(request.POST.get(str(x))) == -2:
                changesToFood += f"Remove {ingredient.name}.\n"
                
            newIngredients[ingredient.name] = newAmount

    theFood.ingred = json.dumps(newIngredients)

    if changesToFood == '':
        changesToFood = "Standard ingredients.\n"

    changesToFood = changesToFood + request.POST.get("message")
    theFood.message = changesToFood
    meal.price += totalUpcharge
    meal.save()
    theFood.save()

    return render(request, "basic/partials/editFoodInMeal.html")

def addMealToOrder(request):
    meals = Meal.objects.all()
    for meal in meals:
        if meal.code == request.GET.get("mealCode"):
            addedMeal = meal
    orders = Order.objects.distinct()
    #note: this method of finding the current order will not work if multiple machines are creating
    #orders at once. This method should be tweaked.
    for currentOrder in orders:
        if currentOrder.number == len(Order.objects.distinct()):
            order = currentOrder
    order.meals.add(addedMeal)
    order.save()

    foodsInOrder = order.foods.all()
    mealsInOrder = order.meals.all()
    total = 0
    for food in foodsInOrder:
        total += food.price
    for meal in mealsInOrder:
        total += meal.price

    mealInstructions = []
    for meal in mealsInOrder:
        instruction = meal.name + ":\n"
        for food in meal.foods.all():
            instruction = instruction + food.name + "; " + food.message + ". "
        mealInstructions.append(instruction)

    return render(request, "basic/partials/addMealToOrder.html", {"meal": addedMeal, "foods": foodsInOrder,
                                                                  "mealInstructions": mealInstructions, "total": total})

def removedItem(request):
    orders = Order.objects.distinct()
    #note: this method of finding the current order will not work if multiple machines are creating
    #orders at once. This method should be tweaked.
    for currentOrder in orders:
        if currentOrder.number == len(Order.objects.distinct()):
            order = currentOrder

    foodsInOrder = order.foods.all()
    mealsInOrder = order.meals.all()
    if request.GET.get("code") != None:
        code = request.GET.get("code")
        for food in foodsInOrder:
            if food.code == code:
                order.foods.remove(food)
        for meal in mealsInOrder:
            if meal.code == code:
                order.meals.remove(meal)
    order.save()
    foodsInOrder = order.foods.all()
    mealsInOrder = order.meals.all()
    total = 0
    for food in foodsInOrder:
        total += food.price
    for meal in mealsInOrder:
        total += meal.price
    
    return render(request, "basic/partials/removedItem.html", {"foods": foodsInOrder, "meals": mealsInOrder, "total": total})

def signout(request):
    logout(request)
    return redirect('basic:login')

