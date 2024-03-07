from faker import Faker
from basic.models import Employee, Shift
from datetime import timedelta
import random
from django.utils import timezone

fake = Faker()

for employee in Employee.objects.all():
    for _ in range(3):  # Generate 3 shifts for each employee
            start_time = fake.date_time_between(start_date='-30d', end_date='now', tzinfo=timezone.get_current_timezone())  # Random start time within the last 30 days
            end_time = start_time + timedelta(hours=random.randint(4, 12))  # End time is within 4-12 hours after start time
            shift = Shift.objects.create(start=start_time, end=end_time, employee=employee)