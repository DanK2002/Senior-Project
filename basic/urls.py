from django.urls import path
from django.contrib.auth.decorators import login_required
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
    path("back-order/", views.backorder, name="back-order"),
    path("addneworder/", views.addneworder, name="addneworder"),
    path("inprogress/", views.inprogress, name="inprogress"),
    path("back-inprogress/", views.backinprogress, name="back-inprogress"),
    path("ready/", views.ready, name="ready"),
    path("back-ready/", views.backready, name="back-ready"),
    path("completed/", views.completed, name="completed"),
    path("back-completed/", views.backcompleted, name="back-completed"),
    path('mark_ready/<int:order_id>/', views.mark_ready, name='mark_ready'),
    path('mark_completed/<int:order_id>/', views.mark_completed, name='mark_completed'),
    path('remove_completed/<int:order_id>/', views.remove_completed, name='remove_completed'),
    path('remove_ready/<int:order_id>/', views.remove_ready, name='remove_ready'),
    path('get-food-details/<int:order_id>/', views.get_food_details, name='get_food_details'),




    path("clockin-out/", views.clockin_out, name="clockin-out"),
    path("modal/", views.modal, name="modal"),
    path("auth-clockin-out/", views.auth_clockin_out, name="auth-clockin-out"),

    # HTMX url(s)
    path("partials/quantity/", views.quantity, name="quantity"),
    path("partials/searchInventory/", views.searchInventory, name="searchInventory"),
    path("partials/addIngredient/", views.addIngredient, name="addIngredient"),
    path("partials/removeIngredient/", views.removeIngredient, name="removeIngredient"),
    path("partials/sales_summary/", views.salesSummary, name="summary-report"),
    path("csv-report/", views.generateCsv, name="csv-report"),
    
    path("login/", views.login, name="login"),
    path("signout/", views.signout, name="signout"),
    path("landingpage/", login_required(views.landingpage), name="landingpage"),
    path("new-employee/", views.new_employee_form, name= "new-employee"),
    path("save-new-employee/", views.save_new_employee, name= "save-new-employee"),
    path("view-employee/", views.view_employee, name= "view-employee"),
    path("remove-employee/", views.remove_employee, name="remove-employee"),
    path("edit-employee-form/", views.edit_employee, name= "edit-employee-form"),
    path("edit-employee-save/", views.save_existing_employee, name= "edit-employee-save"),
    path("view-all-employees/", views.view_all_employees, name= "view-all-employees"),
    path("login/", views.login, name="login"),
    path("landingpage/", views.landingpage, name="landingpage"),

    path("ordercreation1/", views.ordercreation1, name="ordercreation1"),
    path("ordercreation2/", views.ordercreation2, name="ordercreation2"),
    path("ordercreation3/", views.ordercreation3, name="ordercreation3"),
    path("partials/fooditems/", views.fooditems, name="fooditems"),
    path("partials/customizeFood/", views.customizeFood, name="customizeFood"),
    path("partials/amountchange/", views.amountchange, name="amountchange"),
    path("partials/addFoodToOrder/", views.addFoodToOrder, name="addFoodToOrder"),
    path("partials/meal_items/", views.meal_items, name="meal_items"),
    path("partials/customizeMeal/", views.customizeMeal, name="customizeMeal"),
    path("partials/customizeFoodInMeal/", views.customizeFoodInMeal, name="customizeFoodInMeal"),
    path("partials/editFoodInMeal/", views.editFoodInMeal, name="editFoodInMeal"),
    path("partials/addMealToOrder/", views.addMealToOrder, name="addMealToOrder"),
    path("partials/removedItem/", views.removedItem, name="removedItem"),
    
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
    path('list_categories/', views.list_categories, name='list_categories'),
    path('list_meals/', views.list_meals, name='list_meals'),
    path('save_food_as_new_food/', views.save_food_as_new_food, name='save_food_as_new_food'),


    path("view-shifts/", views.view_shifts, name="view-shifts"),
    path("save-new-shift/", views.save_new_shift, name="save-new-shift"),
    path("save-existing-shift/", views.save_existing_shift, name="save-existing-shift"),
    path("edit-shift/", views.edit_shift, name="edit-shift"),
    path("remove-shift/", views.remove_shift, name="remove-shift"),
    path("add-shift/", views.add_shift, name="add-shift"),
    path("edit-shifts/", views.edit_shifts, name = "edit-shifts"),

    # Price Adjustment
    path("adjust-price/", views.adjust_price, name = "adjust-price"),
    path("adjust-price-filter-order/", views.AP_filter_order, name = "adjust-price-filter-order"),
    path("adjust-price-order-details/", views.AP_order_details, name = "adjust-price-order-details"),
    path("adjust-price-order-comp/", views.AP_order_comp, name = "adjust-price-order-comp"),
    path("adjust-price-order-void/", views.AP_order_void, name = "adjust-price-order-void"),
    path("save-item-price/", views.AP_save_item_price, name="save-item-price"),
    path("adjust-item-price/", views.AP_adjust_item_price, name="adjust-item-price"),
    path("void-item/", views.AP_void_item, name = "void-item"),
    path("save-order-price/", views.AP_save_order_price, name = "save-order-price"),

]