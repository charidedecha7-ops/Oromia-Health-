from django.contrib import admin
from .models import Drug, DispenseRecord

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'stock', 'unit', 'expiry_date']
    list_filter = ['expiry_date']
    search_fields = ['name']

@admin.register(DispenseRecord)
class DispenseRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'drug', 'quantity', 'pharmacist', 'date']
    list_filter = ['date', 'pharmacist']
    search_fields = ['student__user__username', 'drug__name']
    date_hierarchy = 'date'
