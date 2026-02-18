from django.contrib import admin
from .models import AttendanceRecord


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'lecture', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('student__user__first_name', 'student__user__last_name')
