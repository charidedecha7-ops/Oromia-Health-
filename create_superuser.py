"""
Create a superuser for Django admin
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_center.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser
username = 'admin'
email = 'admin@haramaya.edu'
password = 'admin123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        role='admin'
    )
    print(f"✅ Superuser created successfully!")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Login at: http://127.0.0.1:8000/admin/")
else:
    print(f"⚠️ User '{username}' already exists")
    print(f"Username: {username}")
    print(f"Password: {password}")
