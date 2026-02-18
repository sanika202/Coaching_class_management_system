from django.db import models
from core.models import CustomUser, Lecture
from django.apps import apps


class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]
    lecture = models.ForeignKey('core.Lecture', on_delete=models.CASCADE, related_name='attendance_records')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='attendance_records', limit_choices_to={'role': 'student'})
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='absent')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('lecture', 'student')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.date} - {self.status}"