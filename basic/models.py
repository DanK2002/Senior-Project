from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Computed objects cache computations that were already performed
# A computation that has already been performed will not be performed again 
class Computed(models.Model):  
    input = models.IntegerField()
    output = models.IntegerField()
    time_computed = models.DateTimeField(null=True)

    def __str__(self):
        return(f"{self.input} -> {self.output}")
    
##Project models

#employees
class Employee(models.Model):
    user = models.OneToOneField(User)
    wage = models.FloatField(null = False)

class Shift(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    employee = models.ForeignKey(Employee)


# orders and food
class Order(models.Model):
    number = models.IntegerField()
    time_est = models.DateTimeField()
    time_submitted = models.DateTimeField()
    time_completed = models.DateTimeField()
    foods = models.ManyToManyField('Food', blank=False)
    meals = models.ManyToManyField('Meal', blank=False)
    price = models.FloatField(null=False)
    employee_submitted = models.ForeignKey(Employee)

class Meal(models.Model):
    name  = models.CharField(max_length=100)
    foods = models.ManyToManyField('Food', blank=False)
    price = models.FloatField(blank = False)

class Food(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(null = False)
    category = models.CharField(max_length=100)
    ingred = models.ManyToManyField('Ingredient', blank=False)

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(blank = False)

    def __str__(self):
        return self.name


