from django.contrib import admin
from .models import LabTest

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'test_type', 'is_completed', 'technician', 'date']
    list_filter = ['test_type', 'is_completed', 'date']
    search_fields = ['student__user__username', 'test_type']
    date_hierarchy = 'date'
