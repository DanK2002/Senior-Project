from faker import Faker
import random
from basic.models import Employee, Shift
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

fake = Faker()

for x in range(5):
    fake_name = fake.name().split()
    first_name = fake_name[0]
    last_name = fake_name[-1]
    wage = round(random.uniform(10.0, 30.0), 2)
    username = f"{last_name.lower()}{random.randint(0, 99):02d}"
    try:
        user = User.objects.create(username=username, password="password123", first_name=first_name, last_name=last_name)
        employee = Employee.objects.create(user=user, wage=wage)
        for _ in range(3):  # Generate 3 shifts for each employee
            start_time = fake.date_time_between(start_date='-30d', end_date='now', tzinfo=timezone.get_current_timezone())  # Random start time within the last 30 days
            end_time = start_time + timedelta(hours=random.randint(4, 12))  # End time is within 4-12 hours after start time
            shift = Shift.objects.create(start=start_time, end=end_time, employee=employee)
    except Exception as e:
        print(f"Error creating employee: {e}")

