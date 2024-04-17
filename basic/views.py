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
from datetime import timedelta, datetime
from django.contrib.auth.decorators import login_required

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
            'groups' : groups
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
    shiftForm = EditEmployeeShifts({
        "start_time" : originalShift.start,
        "end_time" : originalShift.end
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
    return render(
        request,
        "basic/partials/remove_shift.html"
    )

# User wants to save changes to an existing shift
def save_existing_shift(request):
    print("Saving shift...")
    print(request.POST.get(''))
    if request.method == "POST":
        selectedUser = User.objects.get(username = request.POST.get('user'))
        selectedEmployee = Employee.objects.get(user = selectedUser)
        originalShift = Shift.objects.get(employee = selectedEmployee, start = request.POST.get('original-shift'))
        originalShift.start = request.POST.get('start_time')
        originalShift.end = request.POST.get('end_time')
        originalShift.save()
        return render(
            request,
            "basic/partials/saved_shift.html"
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
        Shift.objects.create(start = request.POST.get('start_time'),
                          end = request.POST.get('end_time'),
                          employee = selectedEmployee)
        return render(
            request,
            "basic/partials/saved_shift.html"
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

def remove_ready(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.time_ready = None
    order.save()
    return JsonResponse({'success': True})

def remove_completed(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.time_completed = None
    order.time_ready = timezone.now()
    order.save()
    return JsonResponse({'success': True})

def clockin_out(request):
    users = User.objects.all()
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
def ordercreation(request):
    categories = Food.objects.values_list('category', flat=True).distinct()

    #fakeUser = User.objects.create(username='username', password="password", first_name='first_name', last_name='last_name')
    user = request.user

    orderNumber = len(Order.objects.distinct()) + 1

    order = Order(number = orderNumber, time_est = timezone.now(), time_submitted = timezone.now(),
                   price = 0.0, employee_submitted = user, message = '')

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
        return render(request, "basic/partials/customizeFood.html", {'food': theFood, 'inFood': ingredientsInFood,
                                                                 'notInFood': notInFood})

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
        ).values_list('code', flat=True).order_by('-code').first()
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
            elif int(request.POST.get(str(x))) == 1:
                changesToFood = changesToFood + "Add extra " + ingredient.name + ".\n"
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
    order.price = total
    order.save()

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
        ).values_list('code', flat=True).order_by('-code').first()
        
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
            ).values_list('code', flat=True).order_by('-code').first()
            
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
        theFood = Food.objects.filter(code=foodCode).first()

        ingredientDictionary = json.loads(theFood.ingred)

        ingredientsInFood = Ingredient.objects.filter(name__in=ingredientDictionary.keys())
        notInFood = Ingredient.objects.exclude(name__in=ingredientDictionary.keys())

        return render(request, "basic/partials/customizeFoodInMeal.html", {'food': theFood, 'inFood': ingredientsInFood,
                                                                 'notInFood': notInFood})

def editFoodInMeal(request):
    foodCode = request.POST.get("foodCode")
    theFood = Food.objects.filter(code=foodCode).first()

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
            elif int(request.POST.get(str(x))) == 1:
                changesToFood = changesToFood + "Add extra " + ingredient.name + ".\n"
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
    print(foodsInOrder)
    mealsInOrder = order.meals.all()
    total = 0
    for food in foodsInOrder:
        total += food.price
    for meal in mealsInOrder:
        total += meal.price
    order.price = total
    order.save()

    mealInstructions = []
    for meal in mealsInOrder:
        instruction = meal.name + ":\n"
        for food in meal.foods.all():
            instruction = instruction + food.name + "; " + food.message + ". "
        mealInstructions.append(instruction)

    return render(request, "basic/partials/addMealToOrder.html", {"meal": addedMeal, "foods": foodsInOrder,
                                                                  "mealInstructions": mealInstructions, "total": total})

def ordersummary(request):
    return render(request, "basic/partials/ordersummary.html",)


