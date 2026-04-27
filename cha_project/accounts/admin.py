from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_approved', 'is_active')
    list_filter = ('role', 'is_approved', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('CHA Info', {'fields': ('role', 'is_approved', 'phone', 'date_of_birth', 'address')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('CHA Info', {'fields': ('role', 'is_approved', 'phone')}),
    )
    actions = ['approve_users', 'reject_users']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True, is_active=True)
    approve_users.short_description = "Approve selected users"

    def reject_users(self, request, queryset):
        queryset.update(is_approved=False, is_active=False)
    reject_users.short_description = "Reject selected users"
