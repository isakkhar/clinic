from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'specialization', 'mobile_number', 'email']
    search_fields = ['user__first_name', 'user__last_name', 'specialization']
    list_filter = ['specialization']
