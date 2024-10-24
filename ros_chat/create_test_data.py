import random
from django.core.management import call_command
from django.db import transaction
from django.contrib.auth.models import User
from yourapp.models import YourModel  # replace with your model

def create_test_data():
    # Create test users
    for i in range(10):
        username = f"user{i}"
        email = f"{username}@example.com"
        password = "password123"
        User.objects.create_user(username, email, password)

    # Create test data for YourModel
    for i in range(50):
        your_model = YourModel(
            name=f"Test {i}",
            description=f"This is a test {i}",
            # Add other fields as needed
        )
        your_model.save()

    print("Test data created!")

if __name__ == "__main__":
    create_test_data()