from django.db import models
from django.contrib.auth.models import AbstractUser


#employees
class Employee(AbstractBaseUser):
    name = models.CharField(max_length=100)     # rewrite to use django User model?
    eid = models.IntegerField(blank = False)    #
    pin = models.IntegerField(blank = False)    #
    wage = models.FloatField(null = False)
    Position = models.CharField(max_length=100) # Groups: A generic way of applying labels and permissions to more than one user.

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
    employee_submitted = models.ManyToManyField('Employee', blank=False) #or is this one to many?

class Meal(models.Model):
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