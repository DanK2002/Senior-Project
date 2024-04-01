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
    path("back-order/", views.backorder, name="back-order"),
    path("addneworder/", views.addneworder, name="addneworder"),
    path("inprogress/", views.inprogress, name="inprogress"),
    path("back-inprogress/", views.backinprogress, name="inprogress"),
    path("ready/", views.ready, name="ready"),
    path("back-ready/", views.backready, name="back-ready"),
    path("completed/", views.completed, name="completed"),
    path("back-completed/", views.backcompleted, name="back-completed"),
    path("clockin-out/", views.clockin_out, name="clockin-out"),

    # HTMX url(s)
    path("clockin/", views.clockin, name="clockin"),
    path("clockout/", views.clockout, name="clockout"),

]