from django.db import models
from django.contrib.auth.models import User, Group, Permission

# Computed objects cache computations that were already performed
# A computation that has already been performed will not be performed again 
class Computed(models.Model):  
    input = models.IntegerField()
    output = models.IntegerField()
    time_computed = models.DateTimeField(null=True)
       
##Project models

#employees
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wage = models.FloatField(null=False)
    
    def __str__(self):
        return self.user.username

class Shift(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"Shift of {self.employee} from {self.start} to {self.end}"

# orders and food
class Order(models.Model):
    number = models.IntegerField()
    time_est = models.DateTimeField()
    time_submitted = models.DateTimeField()
    time_completed = models.DateTimeField(null=True)
    foods = models.ManyToManyField('Food', blank=False)
    meals = models.ManyToManyField('Meal', blank=False)
    price = models.FloatField(null=False)
    employee_submitted = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order #{self.number} submitted by {self.employee_submitted}"

class Meal(models.Model):
    name  = models.CharField(max_length=100)
    foods = models.ManyToManyField('Food', blank=False)
    price = models.FloatField(blank = False)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(null = False)
    category = models.CharField(max_length=100)
    ingred = models.JSONField(default=dict)
#    ingred = models.ManyToManyField('Ingredient', blank=False)
    
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(blank = False)

    def __str__(self):
        return self.name


