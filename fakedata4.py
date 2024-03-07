from faker import Faker
import random
from basic.models import Employee, Shift
from datetime import timedelta
from django.utils import timezone

fake = Faker()
print(1)

employees = Employee.objects.all()
print(2)
for employee in employees:
    print(3)
    print(employee)
    print(4)