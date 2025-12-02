from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('lab_tech', 'Lab Technician'),
        ('pharmacist', 'Pharmacist'),
        ('receptionist', 'Receptionist'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def is_doctor(self):
        return self.role == 'doctor'

    def is_student(self):
        return self.role == 'student'

    def is_staff_member(self):
        return self.role in ['admin', 'doctor', 'nurse', 'lab_tech', 'pharmacist', 'receptionist']
