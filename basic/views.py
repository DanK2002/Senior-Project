from django.shortcuts import render, redirect
from django.http import Http404
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
    selected_category = request.POST.get('category') #get selected category
    categories = Food.objects.values_list('category', flat=True).distinct()

    form = AddFoodForm()

    if request.method == 'POST':
        if 'save' in request.POST:  # Check if the form was submitted by the Save button

            form = AddFoodForm(request.POST)
            if form.is_valid():
                #if form is valid, process data
                name = form.cleaned_data['name']
                category = form.cleaned_data['category']
                price = form.cleaned_data['price']
                food = Food.objects.create(name=name, category=category, price=price)
            return redirect('managemenu')
        elif 'cancel' in request.POST:  # Check if the form was submitted by the Cancel button
            return redirect('managemenu')  # Redirect to the managemenu page without processing the form
    if selected_category:
        foods = Food.objects.filter(category=selected_category)
    else:
        foods = Food.objects.all()
    if request.method == 'POST' and 'food_id' in request.POST:
        # Handle AJAX request for food details
        food_id = request.GET.get('food_id')
        food = Food.objects.get(pk=food_id)
        edit_view_food = {
            'name': food.name,
            'category': food.category,
            'price': food.price
        }
        return JsonResponse(edit_view_food)
    
    return render(request, "basic/managemenu.html", 
                  {'categories': categories, 
                   'selected_category': selected_category, 
                   'form': form, 'foods': foods })

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