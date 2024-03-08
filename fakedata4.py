import random
from faker import Faker
from django.utils import timezone
from datetime import timedelta
from basic.models import Employee, Shift

fake = Faker()

for employee in Employee.objects.all():
    for x in range(3):
        start_time = fake.date_time_between(start_date='-30d', end_date='now', tzinfo=timezone.get_current_timezone())
        end_time = start_time + timedelta(hours=random.randint(4, 12))
        try:
            shift = Shift.objects.create(start=start_time, end=end_time, employee=employee)
        except Exception as e:
            print(f"Error creating shift: {e}")

