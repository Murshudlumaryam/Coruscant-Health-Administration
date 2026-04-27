from django.contrib import admin
from .models import Department, OrderResult

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')

@admin.register(OrderResult)
class OrderResultAdmin(admin.ModelAdmin):
    list_display = ('order', 'uploaded_by', 'uploaded_at')
