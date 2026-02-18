from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Lecture, StudentProfile, TeacherProfile, Notification, Subject, Batch

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'get_full_name', 'role', 'status')
    list_filter = ('role', 'status', 'created_at')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'date_of_birth', 'profile_image', 'address', 'status')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'date_of_birth', 'profile_image', 'address', 'status')}),
    )

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('enrollment_number', 'user', 'batch', 'total_fees', 'fees_paid', 'fees_remaining')
    list_filter = ('batch', 'created_at')
    search_fields = ('user__username', 'enrollment_number')

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'experience', 'salary')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'employee_id')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')

#for the timetable app,

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('subject', 'batch', 'teacher', 'class_date', 'start_time')
    list_filter = ('class_date', 'batch')
    search_fields = ('subject', 'batch')
