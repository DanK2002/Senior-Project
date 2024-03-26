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
            html_content = render(
                request,
                "basic/employees_html.html",
                {
                    'employees' : employees,
                    'users' : users,
                    'add_form' : form,
                }
            ).content.decode('utf-8')
        elif 'View' in request.POST:  # User wants to view information about a specific employee
            selectedUsername = request.POST.get('select-employees')     # Get the username requested
            selectedUser = User.objects.get(username=selectedUsername)  # Find that user
            selectedEmployee = Employee.objects.get(user=selectedUser)  # And the employee linked to it
            shifts = Shift.objects.filter(employee = selectedEmployee)  # Find all of their shifts
            html_content = render(
                request,
                "basic/employees_html.html",
                {
                    'employees' : employees,
                    'users' : users,
                    'selectedUser' : selectedUser,
                    'selectedEmployee' : selectedEmployee,
                    'shifts' : shifts,
                }
            ).content.decode('utf-8')
        elif 'Remove' in request.POST:    # User wants to delete employee
            selectedUsername = request.POST.get('select-employees')             # Get the username requested
            selectedUser = User.objects.get(username=selectedUsername)  # Find that user
            selectedEmployee = Employee.objects.get(user=selectedUser)  # And the employee linked to it
            print(selectedUser.first_name + selectedUser.last_name)
            Shift.objects.filter(employee = selectedEmployee).delete()  # Delete their shifts
            Employee.objects.get(user = selectedUser).delete()          # Delete the employee
            User.objects.get(username = selectedUsername).delete()      # Delete the user
            html_content = render(
                request,
                "basic/employees_html.html",
                {
                    'employees' : employees,
                    'users' : users,
                }
            ).content.decode('utf-8')
        elif 'Add' in request.POST:     # User wants to add a new employee and has already submitted the form
            newUser = User.objects.create(                     # Add a new user based on form input
                username = request.POST.get('username'),
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
            )
            Employee.objects.create(user=newUser, wage=request.POST.get('wage'))
            html_content = render(
                request,
                "basic/employees_html.html",
                {
                    'employees' : employees,
                    'users' : users,
                }
            ).content.decode('utf-8')
        elif 'Edit' in request.POST:  # User wants to edit an existing employee; display the form
            selectedUsername = request.POST.get('user')                 # Get the username requested
            selectedUser = User.objects.get(username=selectedUsername)  # Find that user
            selectedEmployee = Employee.objects.get(user=selectedUser)  # And the employee linked to it
            shifts = Shift.objects.filter(employee = selectedEmployee)  # And their related shifts

            # Populate the form with pre-existing data
            editEmployee = EditEmployeeForm({"first_name": selectedUser.first_name,
                                            "last_name": selectedUser.last_name,
                                            "wage" : selectedEmployee.wage})
            html_content = render(
                request,
                "basic/employees_html.html",
                {
                    'selectedUser': selectedUser,
                    'selectedEmployee': selectedEmployee,
                    'employees' : employees,
                    'users' : users,
                    'editEmployee' : editEmployee,
                }
            ).content.decode('utf-8')
        elif 'Save' in request.POST:          # User has edited an existing employee and wants to save changes
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
            html_content = render(
                request,
                "basic/employees_html.html",
                {
                    'employees' : employees,
                    'users' : users,
                    'selectedUser' : selectedUser,
                    'selectedEmployee' : selectedEmployee,
                    'shifts' : shifts,
                }
            ).content.decode('utf-8')
        else:
            html_content = render(
                request,
                "basic/employees_html.html",
                {
                    'employees' : employees,
                    'users' : users,
                }
            ).content.decode('utf-8')
    else:
            html_content = render(
            request,
            "basic/employees_html.html",
            {
                'employees' : employees,
                'users' : users,
            }
        ).content.decode('utf-8')
                
    css_content = render(request, "basic/employees_css.html").content.decode('utf-8')
    # If no actions have occurred, render the page with just employees

    return render(request, "basic/sidenav.html", { 
        'html_content': html_content,
        'css_content': css_content
    })


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

    html_content = render(request, "basic/menu_html.html", {
        'categories': categories, 
        'selected_category': selected_category, 
        'form': form, 
        'foods': foods, 
        'edit_mode': edit_mode
        }).content.decode('utf-8')
    css_content = render(request, "basic/menu_css.html").content.decode('utf-8')

    return render(request, "basic/sidenav.html", { 
        'html_content': html_content,
        'css_content': css_content
    })


def inventory(request):
    ingredients = Ingredient.objects.distinct()
    html_content = render(request, "basic/inventory_html.html", {'ingredients': ingredients}).content.decode('utf-8')
    css_content = render(request, "basic/inventory_css.html").content.decode('utf-8')
    return render(request, "basic/sidenav.html", { 
        'html_content': html_content,
        'css_content': css_content
    })


def sales(request):
    html_content = render(request, "basic/sales_html.html").content.decode('utf-8')
    css_content = render(request, "basic/sales_css.html").content.decode('utf-8')
    return render(request, "basic/sidenav.html", { 
        'html_content': html_content, # div in sidenav
        'css_content': css_content # div in sidenav
    })


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
    employees = Employee.objects.all()
    users = User.objects.all()
    return render(
        request, 
        "basic/clockin-out.html", 
        {
            'employees': employees,
            'users': users
        })

def in_out(request):
    if request.method == 'POST':
        return render(request, "partials/in-out.html")
    
def clockin(request):
    return render(request, "partials/clockin.html")
    
def clockout(request):
    return render(request, "partials/clockout.html")
    
