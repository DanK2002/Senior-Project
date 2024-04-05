from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse, HttpResponse
import json
from .models import *
from django.utils import timezone
from .forms import *
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.http import require_GET, require_POST
import csv
import json

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
    selected_category = request.POST.get('category') #get selected category
    categories = Food.objects.values_list('category', flat=True).distinct()
    selected_category = None
    selected_food = None
    form = AddFoodForm()
    if request.method == 'POST':
        selected_category = request.POST.get('category')
        selected_food = request.POST.get('food')
        form = AddFoodForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            price = form.cleaned_data['price']
            new_food = Food.objects.create(name=name, category=category, price=price)
            new_food.save()
            return redirect('basic:managemenu') 
    
    if selected_category:
        foods = Food.objects.filter(category=selected_category)
    else:
        foods = None
    
    html_content = render(request, "basic/managemenu.html", 
                  {'categories': categories, 
                   'selected_category': selected_category,
                   'selected_food': selected_food,
                   'foods': foods, 'form': form}).content.decode('utf-8')
    css_content = render(request, "basic/inventory_css.html").content.decode('utf-8')
    
    return render(request, "basic/sidenav.html", { 
        'html_content': html_content,
        'css_content': css_content
    })


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
        return redirect('basic:managemenu')


def edit_view_food(request):
    form = EditFoodForm()
    if request.method == 'POST':
        form = EditFoodForm(request.POST)
        if form.is_valid():
            # Retrieve the data submitted in the form
            new_name = form.cleaned_data['initial_name']
            new_category = form.cleaned_data['initial_category']
            new_price = form.cleaned_data['initial_price']
            
            original_name = request.POST.get('original_name')
            original_food = get_object_or_404(Food, name=original_name)
            original_food.name = new_name
            original_food.category = new_category
            original_food.price = new_price
            original_food.save()

            return redirect('basic:managemenu')

    return render(request, 'basic/partials/edit_view_food.html', {'form': form})

def fetch_food_details(request):
    if request.method == 'GET':
        food_name = request.GET.get('food_name')
        food = Food.objects.get(name=food_name)
        form = EditFoodForm(initial={'initial_name': food.name, 'initial_category': food.category, 'initial_price': food.price})

        return render(request, 'basic/partials/edit_view_food.html',  {'form': form})
    

def update_food(request):
    if request.method == 'POST':
        selected_category = request.POST.get('category')
        selected_food = request.POST.get('food')
        print("Selected Category:", selected_category)
        print("Selected Food:", selected_food)
        return redirect('basic:managemenu', category=selected_category, food=selected_food)

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
            # Save the new food item to the database
            new_food.save()
            return redirect('basic:managemenu')
    else:
        form = AddFoodForm()
    return render(request, 'basic/partials/add_food.html', {'form': form})

def edit_food(request, food_name):
    food = get_object_or_404(Food, name='initial_food')

    if request.method == 'POST':
        form = EditFoodForm(request.POST)
        if form.is_valid():
            food.name = form.cleaned_data['initial_food']
            food.category = form.cleaned_data['initial_category']
            food.price = form.cleaned_data['initial_price']
            food.save()
            return redirect('basic:managemenu')
    else:
        form = EditFoodForm(initial={'initial_food': food.name, 'initial_category': food.category, 'initial_price': food.price})

    return render(request, 'basic/partials/edit_food.html', {'form': form})

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
    ing.quantity = ing.quantity + int(request.POST[f'amount{ingredientID}'])
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
    ingredientName = request.POST.get("ingredientTitle")
    ingredientAmount = int(request.POST.get("ingredientAmount"))
    ingredientID = len(Ingredient.objects.distinct())
    ingredient = Ingredient(name=ingredientName, quantity=ingredientAmount, idnumber=ingredientID)
    ingredient.save()
    ingredients = Ingredient.objects.distinct()

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
    return JsonResponse({'success': True})

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
    return JsonResponse({'success': True})

def clockin_out(request):
    employees = Employee.objects.all()
    users = User.objects.all()
    currentShifts = Shift.objects.filter(end=None)
    clockedIn = []
    for shift in currentShifts:
        clockedIn.append(shift.employee.user.username)
    return render(
        request, 
        "basic/clockin-out.html", 
        {
            'employees': employees,
            'users': users,
            'clockedIn': clockedIn
        })
    
def clockin(request):
    return render(request, "partials/clockin.html")
    
def clockout(request):
    return render(request, "partials/clockout.html")
    

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
def ordercreation(request):
    categories = Food.objects.values_list('category', flat=True).distinct()

    fakeUser = User.objects.create(username='username', password="password", first_name='first_name', last_name='last_name')

    orderNumber = len(Order.objects.distinct()) + 1

    order = Order(number = orderNumber, time_est = '0001-01-01', time_submitted = '0001-01-01', time_ready = '0001-01-01',
                time_completed = '0001-01-01', price = 0.0, employee_submitted = fakeUser, message = '')

    order.save()

    return render(request, "basic/ordercreation.html", {'categories': categories})

def fooditems(request):
    categoryName = request.GET.get("categoryName")

    foods = Food.objects.distinct()
    newFoods = []
    for food in foods:
        if food.category.upper() == categoryName.upper():
            newFoods.append(food)

    return render(request, "basic/partials/fooditems.html", {'foods': newFoods, 'category': categoryName})

def customizeFood(request):
    if request.method == 'GET':
        foodName = request.GET.get("foodName")
        foods = Food.objects.distinct()
        for food in foods:
            if food.name.upper() == foodName.upper():
                theFood = food
        allIngredients = Ingredient.objects.distinct()
        ingredientDictionary = json.loads(theFood.ingred)
        ingredientsInFood = list(ingredientDictionary.keys())
        notInFood = []
        inFood = False
        for ingredient in allIngredients:
            for ing in ingredientsInFood:
                if ing.upper() == ingredient.name.upper():
                    inFood = True
            if not inFood:
                notInFood.append(ingredient.name)
            inFood = False
        return render(request, "basic/partials/customizeFood.html", {'food': theFood, 'inFood': ingredientsInFood,
                                                                 'notInFood': notInFood})
    else:
        foodName = request.POST.get("foodName")
        foods = Food.objects.distinct()
        for food in foods:
            if food.name.upper() == foodName.upper():
                theFood = food
        orders = Order.objects.distinct()
        for order in orders:
            if order.number == len(Order.objects.distinct()):
                order.foods.add(theFood)
        order.save()
        allIngredients = Ingredient.objects.distinct()
        ingredientDictionary = json.loads(theFood.ingred)
        ingredientsInFood = list(ingredientDictionary.keys())
        notInFood = []
        inFood = False
        for ingredient in allIngredients:
            for ing in ingredientsInFood:
                if ing.upper() == ingredient.name.upper():
                    inFood = True
            if not inFood:
                notInFood.append(ingredient.name)
            inFood = False
        return render(request, "basic/partials/customizeFood.html", {'food': theFood, 'inFood': ingredientsInFood,
                                                                 'notInFood': notInFood})