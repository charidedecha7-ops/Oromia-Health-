from django.contrib import admin
from .models import Bill

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'service', 'amount', 'status', 'date']
    list_filter = ['status', 'date']
    search_fields = ['student__user__username', 'service']
    date_hierarchy = 'date'
