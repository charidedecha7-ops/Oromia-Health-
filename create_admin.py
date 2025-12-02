"""
Automatically create admin user on deployment
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_center.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Admin credentials
username = 'admin'
email = 'admin@haramaya.edu'
password = 'admin123'

# Create admin if doesn't exist
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        role='admin'
    )
    print(f"✅ Admin user created!")
    print(f"Username: {username}")
    print(f"Password: {password}")
else:
    print(f"⚠️ Admin user already exists")
    print(f"Username: {username}")
    print(f"Password: {password}")
