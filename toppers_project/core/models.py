from datetime import date
from django import forms
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('student', 'Student'),
    ('teacher', 'Teacher'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

class CustomUser(AbstractUser):
    """Custom user model with roles"""
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    address = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    class Meta:
        ordering = ['-created_at']


class StudentProfile(models.Model):
    """Student profile with additional details"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    enrollment_number = models.CharField(max_length=50, unique=True)
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=20)
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE, related_name='student_profiles', null=True, blank=True)
    subjects = models.ManyToManyField('Subject', blank=True, related_name='student_profiles')
    total_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fees_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profile_update_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='approved')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.enrollment_number}"

    @property
    def fees_remaining(self):
        return self.total_fees - self.fees_paid
    
        #validatios for the date_of_birth field to ensure students above 15 years of age
    def clean(self):
        today = date.today()
        if self.user.date_of_birth:
            age = today.year - self.user.date_of_birth.year - ((today.month, today.day) < (self.user.date_of_birth.month, self.user.date_of_birth.day))
            if age < 15:
              raise ValidationError('Student must be at least 15 years old.(to be eligible for 11th standard)')


    class Meta:
        ordering = ['enrollment_number']


class TeacherProfile(models.Model):
    """Teacher profile with additional details"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    qualifications = models.TextField()
    subjects_taught = models.ManyToManyField('Subject', related_name='teachers')
    experience = models.IntegerField(help_text="Years of experience")
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    salary_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profile_update_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='approved')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"
    
    @property
    def salary_remaining(self):
        return self.salary - self.salary_paid
    
    def clean(self):
        today = date.today()
        if self.user.date_of_birth:
            age = today.year - self.user.date_of_birth.year - ((today.month, today.day) < (self.user.date_of_birth.month, self.user.date_of_birth.day))
            if age < 21:
                raise ValidationError('Teacher must be at least 21 years old to apply for the position.')


    class Meta:
        ordering = ['employee_id']

class Notification(models.Model):
    """Notifications for dashboard"""
    NOTIFICATION_TYPES = [
        ('registration', 'New Registration'),
        ('profile_update', 'Profile Update'),
        ('login', 'Login'),
        ('fees', 'Fees Updated'),
        ('salary', 'Salary Updated'),
        ('attendance', 'Attendance Marked'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    related_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='related_notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']

def save(self, *args, **kwargs):
    if self.is_superuser:
        self.role = 'admin'
    super().save(*args, **kwargs)
    self.full_clean()  # Call full_clean to trigger model validation

#models of timetable.
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Batch(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
#models for weekly lecture schedule and special classes
class Lecture(models.Model):
    DAYS = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]
    """lecture/class schedule"""
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lectures', limit_choices_to={'role': 'teacher'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    # For timetable
    day = models.CharField(max_length=10, null=True, blank=True, default='Monday', choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    # For special classes
    class_date = models.DateField(null=True, blank=True)
    topic = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Time logic validation
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time")

        # Clash validation (same batch + same day)
        clash = Lecture.objects.filter(
            day=self.day,
            batch=self.batch,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)  # Exclude current lecture when editing

        if clash.exists():
            raise ValidationError(
                "Lecture time clashes with an existing lecture for this batch"
            )

    def __str__(self):
        return f"{self.subject} - {self.batch} ({self.day})"

    class Meta:
        ordering = ['-day', 'start_time']

