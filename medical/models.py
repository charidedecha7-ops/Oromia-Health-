from django.db import models
from django.conf import settings
from students.models import StudentProfile
from appointments.models import Appointment

class Consultation(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='consultation')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='consultations')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consultations_conducted')
    symptoms = models.TextField()
    diagnosis = models.TextField()
    notes = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"CONS-{self.id} : {self.student.user.username}"

class Prescription(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='prescriptions')
    drug_name = models.CharField(max_length=200) # Can be linked to Pharmacy Drug later if needed strictly
    dosage = models.CharField(max_length=200)
    instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"RX for {self.consultation.student.user.username} - {self.drug_name}"
