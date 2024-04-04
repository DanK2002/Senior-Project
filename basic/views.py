from django.shortcuts import render, redirect
from django.http import Http404
from .models import *
from django.utils import timezone
from .forms import *
from django.contrib.auth import authenticate, login as auth_login
from datetime import timedelta, datetime

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

    form = AddFoodForm()

    if request.method == 'POST':
        if 'save' in request.POST:  # Check if the form was submitted by the Save button
            form = AddFoodForm(request.POST)
            if form.is_valid():
                #if form is valid, process data
                name = form.cleaned_data['name']
                category = form.cleaned_data['category']
                price = form.cleaned_data['price']
                #food = Food.objects.create(name=name, category=category, price=price)
            return redirect('managemenu')
        elif 'cancel' in request.POST:  # Check if the form was submitted by the Cancel button
            return redirect('managemenu')  # Redirect to the managemenu page without processing the form
    if selected_category:
        foods = Food.objects.filter(category=selected_category)
    else:
        foods = Food.objects.all()
    
    edit_mode = False
    if request.method == 'POST' and 'edit_food' in request.POST:
        # Set edit_mode to True when the "Edit Food" link is clicked
        edit_mode = True
    
    return render(request, "basic/managemenu.html", {'categories': categories, 'selected_category': selected_category, 'form': form, 'foods': foods, 'edit_mode': edit_mode})

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