from django.urls import path
from . import views

app_name = 'basic'

#app_name="htmx"

urlpatterns = [
    path("home/", views.home, name="home"),
    path("compute/", views.compute, name="compute"),
    path("search/", views.search, name="search"),
    path("manageemployees/", views.manageemployees, name="manageemployees"),
    path("managemenu/", views.managemenu, name="managemenu"),
    path("inventory/", views.inventory, name="inventory"),
    path("sales/", views.sales, name="sales"),
    path("order/", views.order, name="order"),
    path("addneworder/", views.addneworder, name="addneworder"),
    path("inprogress/", views.inprogress, name="inprogress"),
    path("ready/", views.ready, name="ready"),
    path("completed/", views.completed, name="completed"),
    path("clockin-out/", views.clockin_out, name="clockin-out"),
    # HTMX url(s)
    path("partials/quantity/", views.quantity, name="quantity"),
    path("partials/searchInventory/", views.searchInventory, name="searchInventory"),
    path("partials/addIngredient/", views.addIngredient, name="addIngredient"),
    path("clockin/", views.clockin, name="clockin"),
    path("clockout/", views.clockout, name="clockout"),
    path("partials/summary/", views.summary, name="summary-report"),
    
    path("login/", views.login, name="login"),
    path("landingpage/", views.landingpage, name="landingpage"),
    path("new-employee/", views.new_employee_form, name= "new-employee"),
    path("save-new-employee/", views.save_new_employee, name= "save-new-employee"),
    path("view-employee/", views.view_employee, name= "view-employee"),
    path("remove-employee/", views.remove_employee, name="remove-employee"),
    path("edit-employee-form/", views.edit_employee, name= "edit-employee-form"),
    path("edit-employee-save/", views.save_existing_employee, name= "edit-employee-save"),
    path("view-all-employees/", views.view_all_employees, name= "view-all-employees"),
    path("login/", views.login, name="login"),
    path("landingpage/", views.landingpage, name="landingpage"),

]