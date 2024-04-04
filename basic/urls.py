from django.urls import path
from . import views

app_name = 'basic'

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
    path("login/", views.login, name="login"),
    path("landingpage/", views.landingpage, name="landingpage"),
    path("new-employee/", views.new_employee_form, name= "new-employee"),
    path("save-new-employee/", views.save_new_employee, name= "save-new-employee"),
    path("view-employee/", views.view_employee, name= "view-employee"),
    path("remove-employee/", views.remove_employee, name="remove-employee"),
    path("edit-employee-form/", views.edit_employee, name= "edit-employee-form"),
    path("edit-employee-save/", views.save_existing_employee, name= "edit-employee-save"),
    path("view-all-employees/", views.view_all_employees, name= "view-all-employees"),
    path("view-shifts/", views.view_shifts, name="view-shifts"),
    path("save-new-shift/", views.save_new_shift, name="save-new-shift"),
    path("save-existing-shift/", views.save_existing_shift, name="save-existing-shift"),
    path("edit-shift/", views.edit_shift, name="edit-shift"),
    path("remove-shift/", views.remove_shift, name="remove-shift"),
    path("add-shift/", views.add_shift, name="add-shift"),
    path("edit-shifts/", views.edit_shifts, name = "edit-shifts"),
]