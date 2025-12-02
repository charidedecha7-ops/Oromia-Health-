from django.db import models
from django.conf import settings
from students.models import StudentProfile

class LabTest(models.Model):
    TEST_TYPES = (
        ('Malaria', 'Malaria'),
        ('Urine', 'Urine Analysis'),
        ('Blood', 'Blood Test'),
        ('TB', 'Tuberculosis'),
        ('CBC', 'Complete Blood Count'),
        ('Other', 'Other'),
    )
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='lab_tests')
    test_type = models.CharField(max_length=50, choices=TEST_TYPES)
    result = models.TextField(blank=True, null=True)
    technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='tests_conducted', limit_choices_to={'role': 'lab_tech'})
    date = models.DateField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.test_type} for {self.student.user.username}"
