from django.shortcuts import render, redirect
from django.http import Http404
from .models import *
from django.utils import timezone
from .forms import *

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

# For managing employees in the managerial section
def manageemployees(request):
    employees = Employee.objects.all()
    users = User.objects.all()
    if request.method == 'POST':    # Check for form submission
        print(request.POST)         # For debugging purposes; logs request in console
        if 'New Employee' in request.POST:   # User wants to add new employee; displays add employee form
            form =  AddEmployeeForm()
            return render(
                request,
                "basic/manageemployees.html",
                {
                    'employees' : employees,
                    'users' : users,
                    'add_form' : form,
                }
            )
        elif 'View' in request.POST:  # User wants to view information about a specific employee
            selectedUsername = request.POST.get('select-employees')     # Get the username requested
            selectedUser = User.objects.get(username=selectedUsername)  # Find that user
            selectedEmployee = Employee.objects.get(user=selectedUser)  # And the employee linked to it
            shifts = Shift.objects.filter(employee = selectedEmployee)  # Find all of their shifts
            hours = 0
            for shift in shifts:
                hours += (shift.end - shift.start)
            return render(
                request,
                "basic/manageemployees.html",
                {
                    'employees' : employees,
                    'users' : users,
                    'selectedUser' : selectedUser,
                    'selectedEmployee' : selectedEmployee,
                    'shifts' : shifts,
                    'hours' : hours,
                }
            )
        elif 'Remove' in request.POST:    # User wants to delete employee
            selectedUsername = request.POST.get('select-employees')             # Get the username requested
            selectedUser = User.objects.get(username=selectedUsername)  # Find that user
            selectedEmployee = Employee.objects.get(user=selectedUser)  # And the employee linked to it
            print(selectedUser.first_name + selectedUser.last_name)
            Shift.objects.filter(employee = selectedEmployee).delete()  # Delete their shifts
            Employee.objects.get(user = selectedUser).delete()          # Delete the employee
            User.objects.get(username = selectedUsername).delete()      # Delete the user
            return render(
                request,
                "basic/manageemployees.html",
                {
                    'employees' : employees,
                    'users' : users,
                }
            )
        if 'Add' in request.POST:     # User wants to add a new employee and has already submitted the form
            newUser = User.objects.create(                     # Add a new user based on form input
                username = request.POST.get('username'),
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
            )
            Employee.objects.create(user=newUser, wage=request.POST.get('wage'))
            return render(
                request,
                "basic/manageemployees.html",
                {
                    'employees' : employees,
                    'users' : users,
                }
            )
        if 'Edit' in request.POST:  # User wants to edit an existing employee; display the form
            selectedUsername = request.POST.get('user')                 # Get the username requested
            selectedUser = User.objects.get(username=selectedUsername)  # Find that user
            selectedEmployee = Employee.objects.get(user=selectedUser)  # And the employee linked to it
            shifts = Shift.objects.filter(employee = selectedEmployee)  # And their related shifts

            hours = 0
            for shift in shifts:
                hours += (shift.end - shift.start)

            # Populate the form with pre-existing data
            editEmployee = EditEmployeeForm({"first_name": selectedUser.first_name,
                                            "last_name": selectedUser.last_name,
                                            "wage" : selectedEmployee.wage})
            return render(
                request,
                "basic/manageemployees.html",
                {
                    'selectedUser': selectedUser,
                    'selectedEmployee': selectedEmployee,
                    'hours' : hours,
                    'employees' : employees,
                    'users' : users,
                    'editEmployee' : editEmployee,
                }
            )
        if 'Save' in request.POST:          # User has edited an existing employee and wants to save changes
            selectedUsername = request.POST.get('user')                 # Get the username requested
            selectedUser = User.objects.get(username=selectedUsername)  # Find that user
            selectedEmployee = Employee.objects.get(user=selectedUser)  # And the employee linked to it
            shifts = Shift.objects.filter(employee = selectedEmployee)  # And their related shifts
            if (request.POST.get('first_name') != None):
                selectedUser.first_name = request.POST.get('first_name')
            if (request.POST.get('last_name') != None):
                selectedUser.last_name = request.POST.get('last_name')
            if (request.POST.get('wage') != None):
                selectedUser.wage = request.POST.get('wage')
            selectedUser.save()
            return render(
                request,
                "basic/manageemployees.html",
                {
                    'employees' : employees,
                    'users' : users,
                    'selectedUser' : selectedUser,
                    'selectedEmployee' : selectedEmployee,
                    'shifts' : shifts,
                }
            )
    # If no actions have occurred, render the page with just employees
    return render(
        request,
        "basic/manageemployees.html",
        {
            'employees' : employees,
            'users' : users,
        }
    )

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

    return render(request, "basic/managemenu.html", {'categories': categories, 'selected_category': selected_category, 'form': form})

def inventory(request):
    return render(request, "basic/inventory.html")

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