from django.urls import path
from . import views

app_name = 'basic'

urlpatterns = [
    path("home/", views.home, name="home"),
    path("compute/", views.compute, name="compute"),
    path("search/", views.search, name="search"),
    path("manageemployees/", views.manageemployees, name="manageemployees"),
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
    path("login/", views.login, name="login"),
    path("landingpage/", views.landingpage, name="landingpage"),
    
    path("managemenu/", views.managemenu, name="managemenu"),
    path('edit_category_form/', views.edit_category_form, name='edit_category_form'),
    path('edit_category/', views.edit_category, name='edit_category'),
    path('edit_view_food/', views.edit_view_food, name='edit_view_food'),
    path('fetch_food_details/', views.fetch_food_details, name='fetch_food_details'),
    path('update_food/', views.update_food, name='update_food'),
    path('remove_food/', views.remove_food, name='remove_food'),
    path('add_food/', views.add_food, name='add_food'),
    path('ingredient_list/', views.ingredient_list, name='ingredient_list'),
    path('fetch_meal_details/', views.fetch_meal_details, name='fetch_meal_details'),
    path('add_meal/', views.add_meal, name='add_meal'),
    path('edit_view_meal/', views.edit_view_meal, name='edit_view_meal'),
    path('remove_meal/', views.remove_meal, name='remove_meal'),


]