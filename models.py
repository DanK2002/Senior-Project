from django.db import models


#employees
#rewrite to use django User model?
class Employee(models.Model):
    name = models.CharField(max_length=100)
    eid = models.IntegerField(blank = False)
    pin = models.IntegerField(blank = False)
    wage = models.FloatField(null = False)
    Position = models.CharField(max_length=100)

class Shift(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    employee = models.ForeignKey(Employee)


# orders and food
class Order(models.Model):
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