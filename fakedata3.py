from faker import Faker
import random
from basic.models import Employee
from django.contrib.auth.models import User, Group

fake = Faker()

# Genterate Groups
#Front of House
newGroup = Group(name = 'foh')
newGroup.save()
# Back of House
newGroup = Group(name = 'boh')
newGroup.save()
# manager
newGroup = Group(name = 'manager')
newGroup.save()

for x in range(5):
    fake_name = fake.name().split()
    first_name = fake_name[0]
    last_name = fake_name[-1]
    wage = round(random.uniform(10.0, 30.0), 2)
    username = f"{last_name.lower()}{random.randint(0, 99):02d}"
    try:
        user = User.objects.create(username=username, password="password123", first_name=first_name, last_name=last_name)
        employee = Employee.objects.create(user=user, wage=wage)
        if x == 1:
            man = Group.objects.get(name="manager")
            man.user_set.add(user)
        elif x < 4:
            foh = Group.objects.get(name="foh")
            foh.user_set.add(user)
        else:
            boh = Group.objects.get(name="foh")
            boh.user_set.add(user)
    except Exception as e:
        print(f"Error creating employee: {e}")

