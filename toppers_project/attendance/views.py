from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def attendance_list(request):
    """View attendance records"""
    from .models import AttendanceRecord
    
    records = AttendanceRecord.objects.all().order_by('-date')
    context = {
        'records': records,
    }
    return render(request, 'attendance/attendance_list.html', context)
