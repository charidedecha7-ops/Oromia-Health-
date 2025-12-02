from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'doctor', 'date', 'time', 'status', 'created_at']
    list_filter = ['status', 'date', 'doctor']
    search_fields = ['student__user__username', 'doctor__username', 'reason']
    date_hierarchy = 'date'
