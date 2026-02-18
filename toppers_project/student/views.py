from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import CustomUser, StudentProfile, Lecture, Notification, Subject, Batch
from core.forms import CustomUserChangeForm
from functools import wraps
from core.forms import StudentProfileForm


def student_required(view_func):
    """Decorator to check if user is student"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'student':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required(login_url='login')
@student_required
def student_dashboard(request):
    """Student dashboard"""
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('complete_profile_student')
    
    # Get lectures for student's batch
    batch = student_profile.batch
    upcoming_lectures = Lecture.objects.filter(
        batch=batch
    ).order_by('day', 'start_time')[:10]
    
    # Get attendance for this student
    from attendance.models import AttendanceRecord
    attendance_records = AttendanceRecord.objects.filter(student=request.user).order_by('-date')
    
    attendance_count = attendance_records.filter(status='present').count()
    total_classes = attendance_records.count()
    attendance_percentage = (attendance_count / total_classes * 100) if total_classes > 0 else 0
    
    context = {
        'student_profile': student_profile,
        'upcoming_lectures': upcoming_lectures,
        'attendance_percentage': attendance_percentage,
        'total_classes': total_classes,
        'attendance_count': attendance_count,
    }
    return render(request, 'student/dashboard.html', context)


@login_required(login_url='login')
@student_required
def student_profile(request):
    """View student profile"""
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('complete_profile_student')
    
    context = {
        'student_profile': student_profile,
        'user': request.user,
    }
    return render(request, 'student/profile.html', context)


@login_required(login_url='login')
@student_required
def student_attendance(request):
    """View student attendance"""
    from attendance.models import AttendanceRecord
    
    attendance_records = AttendanceRecord.objects.filter(student=request.user).order_by('-date')
    
    attendance_summary = {
        'present': attendance_records.filter(status='present').count(),
        'absent': attendance_records.filter(status='absent').count(),
        'total': attendance_records.count(),
    }
    
    if attendance_summary['total'] > 0:
        attendance_summary['percentage'] = (attendance_summary['present'] / attendance_summary['total'] * 100)
    else:
        attendance_summary['percentage'] = 0
    
    context = {
        'attendance_records': attendance_records,
        'attendance_summary': attendance_summary,
    }
    return render(request, 'student/attendance.html', context)


@login_required(login_url='login')
@student_required
def student_fees(request):
    """View student fees"""
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('complete_profile_student')
    
    context = {
        'student_profile': student_profile,
    }
    return render(request, 'student/fees.html', context)


@login_required(login_url='login')
@student_required
def student_lectures(request):
    """View upcoming lectures"""
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('complete_profile_student')
    
    lectures = Lecture.objects.filter(
        batch=student_profile.batch
    ).order_by('day', 'start_time')
    
    context = {
        'lectures': lectures,
    }
    return render(request, 'student/lectures.html', context)


@login_required(login_url='login')
@student_required
def update_student_profile(request):
    """Update student profile"""
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('complete_profile_student')
    
    if request.method == 'POST':
        # Update user details
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.phone = request.POST.get('phone')
        request.user.address = request.POST.get('address')
        request.user.save()

        # Update student profile
        form = StudentProfileForm(request.POST, instance=student_profile)
        
        if form.is_valid():
            student_profile = form.save(commit=False)
            student_profile.user = request.user
            student_profile.profile_update_status = 'pending'
            student_profile.save()
            form.save_m2m()
        else:
            print(form.errors)
            
        # Create notification for admin
        admin = CustomUser.objects.filter(role='admin').first()
        if admin:
                Notification.objects.create(
                    user=admin,
                    notification_type='profile_update',
                    title=f'Student Profile Update - {request.user.get_full_name()}',
                    message=f'{request.user.get_full_name()} has updated their profile and is waiting for approval',
                    related_user=request.user
                )
            
        messages.success(request, 'Profile updated successfully! Waiting for admin approval...')
        return redirect('student_dashboard')
    else:
        form = StudentProfileForm(instance=student_profile)
    
    context = {
        'user': request.user,
        'student_profile': student_profile,
        'form': form,
    }
    return render(request, 'student/update_profile.html', context)
