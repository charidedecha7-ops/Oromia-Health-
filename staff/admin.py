from django.contrib import admin
from .models import StaffProfile

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['staff_id', 'user', 'department']
    search_fields = ['staff_id', 'user__username', 'user__first_name', 'user__last_name']
    list_filter = ['department', 'user__role']
