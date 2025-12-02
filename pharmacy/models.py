from django.db import models
from django.conf import settings
from students.models import StudentProfile

class Drug(models.Model):
    name = models.CharField(max_length=200)
    stock = models.IntegerField(default=0)
    unit = models.CharField(max_length=50, help_text="e.g. tablets, capsules, bottles")
    expiry_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.stock} {self.unit})"

class DispenseRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='dispensed_drugs')
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    pharmacist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='dispensed_records', limit_choices_to={'role': 'pharmacist'})
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} {self.drug.name} to {self.student.user.username}"
