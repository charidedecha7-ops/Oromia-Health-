from django.contrib import admin
from .models import Consultation, Prescription

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'doctor', 'date']
    list_filter = ['date', 'doctor']
    search_fields = ['student__user__username', 'diagnosis', 'symptoms']
    date_hierarchy = 'date'

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'consultation', 'drug_name', 'dosage']
    search_fields = ['drug_name', 'consultation__student__user__username']
