import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.utils import timezone
from .forms import *
from django.contrib.auth import authenticate, login as auth_login

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
    
    return render(request, "basic/managemenu.html", 
                  {'categories': categories, 
                   'selected_category': selected_category,
                   'selected_food': selected_food,
                   'foods': foods, 'form': form})


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