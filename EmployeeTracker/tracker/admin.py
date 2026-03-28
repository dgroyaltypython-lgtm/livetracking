from django.contrib import admin
from .models import Employee, Trip, Stop, VisitReport
from django.contrib.auth.admin import UserAdmin

class EmployeeAdmin(UserAdmin):
    model = Employee

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'phone')}),
    )

admin.site.register(Employee, EmployeeAdmin)

admin.site.register(Trip)
admin.site.register(Stop)
admin.site.register(VisitReport)