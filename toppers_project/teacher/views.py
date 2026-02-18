from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import CustomUser, TeacherProfile, Lecture, Notification, StudentProfile, Subject
from datetime import datetime, timedelta, date
from django import forms
from core.forms import TeacherProfileForm
from functools import wraps

def teacher_required(view_func):
    """Decorator to check if user is teacher"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'teacher':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required(login_url='login')
@teacher_required
def teacher_dashboard(request):
    """Teacher dashboard"""
    try:
        teacher_profile = request.user.teacher_profile
    except TeacherProfile.DoesNotExist:
        return redirect('complete_profile_teacher')
    
    # #upcoming lectures
    today = datetime.today().date()
    upcoming_lectures = Lecture.objects.filter(
        teacher=request.user,
        class_date__gte=today,
        day=today.strftime('%A')  # Filter by current day of the week
    ).order_by('day', 'start_time')[:10]
    
    total_lectures = Lecture.objects.filter(teacher=request.user).count()
    
    context = {
        'teacher_profile': teacher_profile,
        'upcoming_lectures': upcoming_lectures,
        'total_lectures': total_lectures,
    }
    return render(request, 'teacher/dashboard.html', context)


@login_required(login_url='login')
@teacher_required
def teacher_profile(request):
    """View teacher profile"""
    try:
        teacher_profile = request.user.teacher_profile
    except TeacherProfile.DoesNotExist:
        return redirect('complete_profile_teacher')
    
    context = {
        'teacher_profile': teacher_profile,
        'user': request.user,
    }
    return render(request, 'teacher/profile.html', context)


@login_required(login_url='login')
@teacher_required
def teacher_lectures(request):
    """View teacher's lectures"""
    try:
        teacher_profile = request.user.teacher_profile
    except TeacherProfile.DoesNotExist:
        return redirect('complete_profile_teacher')
    
    lectures = Lecture.objects.filter(teacher=request.user).order_by('-day', '-start_time')
    
    context = {
        'lectures': lectures,
    }
    return render(request, 'teacher/lectures.html', context)


@login_required(login_url='login')
@teacher_required
def mark_attendance(request, lecture_id):
    """Mark attendance for a lecture"""
    lecture = get_object_or_404(Lecture, id=lecture_id, teacher=request.user)
    
    # Get all students in this batch
    students = CustomUser.objects.filter(
        role='student',
        student_profile__batch__in=[lecture.batch],
        status='approved'
    ).select_related('student_profile').distinct()
    from attendance.models import AttendanceRecord
    
    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'attendance_{student.id}', 'absent')
            attendence_record, created = AttendanceRecord.objects.get_or_create(
                lecture=lecture,
                student=student,
                defaults={'date': lecture.class_date, 'status': status}
            )
            if not created:
                attendence_record.status = status
                attendence_record.save()
        
        messages.success(request, 'Attendance marked successfully!')
        return redirect('teacher_dashboard')
    
    # Get existing attendance records for this lecture
    for student in students:
        try:
            record = AttendanceRecord.objects.get(lecture=lecture, student=student)
            student.attendance_status = record.status
        except AttendanceRecord.DoesNotExist:
            student.attendance_status = 'absent'
    
    context = {
        'lecture': lecture,
        'students': students,
    }
    return render(request, 'teacher/mark_attendance.html', context)


@login_required(login_url='login')
@teacher_required
def update_teacher_profile(request):
    """Update teacher profile"""
    try:
        teacher_profile = request.user.teacher_profile
    except TeacherProfile.DoesNotExist:
        return redirect('complete_profile_teacher')
    
    if request.method == 'POST':
        # Update user details
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.phone = request.POST.get('phone')
        request.user.address = request.POST.get('address')
        request.user.save()
        
        # Update teacher profile
        form = TeacherProfileForm(request.POST, instance=teacher_profile)
        if form.is_valid():
          teacher_profile = form.save(commit=False)
          teacher_profile.profile_update_status = 'pending'
          teacher_profile.save()
          form.save_m2m()
        
        # Create notification for admin
        admin = CustomUser.objects.filter(role='admin').first()
        if admin:
            Notification.objects.create(
                user=admin,
                notification_type='profile_update',
                title=f'Teacher Profile Update - {request.user.get_full_name()}',
                message=f'{request.user.get_full_name()} has updated their profile and is waiting for approval',
                related_user=request.user
            )
        
        messages.success(request, 'Profile updated successfully! Waiting for admin approval...')
        return redirect('teacher_dashboard')
    else:
        form = TeacherProfileForm(instance=teacher_profile)
    context = {
        'user': request.user,
        'teacher_profile': teacher_profile,
        'form' : form,
    }
    return render(request, 'teacher/update_profile.html', context)


@login_required(login_url='login')
@teacher_required
def teacher_salary(request):
    """View teacher salary"""
    try:
        teacher_profile = request.user.teacher_profile
    except TeacherProfile.DoesNotExist:
        return redirect('complete_profile_teacher')
    
    context = {
        'teacher_profile': teacher_profile,
    }
    return render(request, 'teacher/salary.html', context)
