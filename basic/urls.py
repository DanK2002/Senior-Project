from django.urls import path
from . import views

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
    path("partials/removeIngredient/", views.removeIngredient, name="removeIngredient"),
    path("clockin/", views.clockin, name="clockin"),
    path("clockout/", views.clockout, name="clockout"),
    path("ordercreation/", views.ordercreation, name="ordercreation"),
    path("partials/fooditems/", views.fooditems, name="fooditems"),
    path("partials/customizeFood/", views.customizeFood, name="customizeFood"),
    path("partials/ordersummary/", views.ordersummary, name="ordersummary")
]