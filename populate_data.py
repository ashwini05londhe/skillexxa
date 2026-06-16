import os
import django
import random
from faker import Faker

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skill.settings')
django.setup()

from django.contrib.auth.models import User
from main.models import Profile

fake = Faker()

def create_users_and_profiles():
    # Create 10 learners
    for i in range(10):
        username = fake.user_name()
        email = fake.email()
        password = 'password123'  # Simple password for testing

        user = User.objects.create_user(username=username, email=email, password=password)
        profile = Profile.objects.create(
            user=user,
            role='learner',
            name=fake.name(),
            age=random.randint(18, 65),
            gender=random.choice(['Male', 'Female', 'Other']),
            phone=fake.phone_number(),
            bio=fake.text(max_nb_chars=200)
        )
        print(f"Created learner: {username}")

    # Create 10 instructors
    for i in range(10):
        username = fake.user_name()
        email = fake.email()
        password = 'password123'

        user = User.objects.create_user(username=username, email=email, password=password)
        profile = Profile.objects.create(
            user=user,
            role='instructor',
            name=fake.name(),
            age=random.randint(25, 70),
            gender=random.choice(['Male', 'Female', 'Other']),
            phone=fake.phone_number(),
            profession=fake.job(),
            experience=f"{random.randint(1, 20)} years",
            domain=random.choice(['Programming', 'Design', 'Marketing', 'Business', 'Science']),
            bio=fake.text(max_nb_chars=200)
        )
        print(f"Created instructor: {username}")

if __name__ == '__main__':
    create_users_and_profiles()
    print("Data population complete!")
