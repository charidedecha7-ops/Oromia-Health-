from django.db import models
from students.models import StudentProfile

class Bill(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    )

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='bills')
    service = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Bill #{self.id} - {self.student.user.username} - {self.amount}"
