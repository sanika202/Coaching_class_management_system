import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from core.models import CustomUser, StudentProfile, TeacherProfile, Notification, Lecture, Subject, Batch
from core.forms import StudentProfileForm, TeacherProfileForm, LectureForm, SubjectForm, BatchForm
from datetime import datetime, timedelta

def admin_required(view_func):
    """Decorator to check if user is admin"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required(login_url='login')
@admin_required
def admin_dashboard(request):
    """Admin dashboard home"""
    notifications_qs = Notification.objects.filter(user=request.user,is_read=False).order_by('-created_at')
    unread_count = notifications_qs.count()
    notifications = notifications_qs[:10]  # Show latest 10 notifications
    
    total_students = CustomUser.objects.filter(role='student', status='approved').count()
    total_teachers = CustomUser.objects.filter(role='teacher', status='approved').count()
    pending_approvals = CustomUser.objects.filter(status='pending').count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'pending_approvals': pending_approvals,
    }
    return render(request, 'admin_dashboard/dashboard.html', context)


@login_required(login_url='login')
@admin_required
def pending_registrations(request):
    """View pending registrations"""
    pending_users = CustomUser.objects.filter(status='pending').order_by('-created_at')
    
    context = {
        'pending_users': pending_users,
    }
    return render(request, 'admin_dashboard/pending_registrations.html', context)


@login_required(login_url='login')
@admin_required
def approve_registration(request, user_id):
    """Approve user registration"""
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.status = 'approved'
        user.save()
        messages.success(request, f'{user.get_full_name()} approved successfully!')
        return redirect('pending_registrations')
    
    return render(request, 'admin_dashboard/approve_registration.html', {'user': user})


@login_required(login_url='login')
@admin_required
def reject_registration(request, user_id):
    """Reject user registration"""
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.status = 'rejected'
        user.save()
        messages.success(request, f'{user.get_full_name()} rejected!')
        return redirect('pending_registrations')
    
    return render(request, 'admin_dashboard/reject_registration.html', {'user': user})


@login_required(login_url='login')
@admin_required
def all_students(request):
    """View all students"""
    students = CustomUser.objects.filter(role='student', status='approved')
    search = request.GET.get('search', '')
    
    if search:
        students = students.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(student_profile__enrollment_number__icontains=search) |
            Q(email__icontains=search)
        )
    
    context = {
        'students': students,
        'search': search,
    }
    return render(request, 'admin_dashboard/all_students.html', context)


@login_required(login_url='login')
@admin_required
def edit_student(request, user_id):
    """Edit student details"""
    student_user = get_object_or_404(CustomUser, id=user_id, role='student')
    
    try:
        student_profile = student_user.student_profile
    except StudentProfile.DoesNotExist:
        student_profile = StudentProfile(user=student_user)
    
    if request.method == 'POST':
        # Update user details
        student_user.first_name = request.POST.get('first_name')
        student_user.last_name = request.POST.get('last_name')  
        student_user.email = request.POST.get('email')
        student_user.phone = request.POST.get('phone')
        dob_str = request.POST.get('date_of_birth')
        if dob_str:
            student_user.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
        student_user.save()
        # Update student profile
        form = StudentProfileForm(request.POST, instance=student_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = student_user
            profile.profile_update_status = 'approved'
            
            # Update fees
            total_fees = request.POST.get('total_fees', 0)
            fees_paid = request.POST.get('fees_paid', 0)
            try:
                profile.total_fees = float(total_fees)
                profile.fees_paid = float(fees_paid)
            except:
                pass
            profile.save()
            messages.success(request, 'Student details updated successfully!')
            return redirect('all_students')
        else:
            print(form.errors)  # Debugging line to print form errors in the console
    else:
        form = StudentProfileForm(instance=student_profile)
    
    context = {
        'form': form,
        'student_user': student_user,
        'student_profile': student_profile,
    }
    return render(request, 'admin_dashboard/edit_student.html', context)


@login_required(login_url='login')
@admin_required
def delete_student(request, user_id):
    """Delete student"""
    student_user = get_object_or_404(CustomUser, id=user_id, role='student')
    
    if request.method == 'POST':
        name = student_user.get_full_name()
        student_user.delete()
        messages.success(request, f'{name} has been deleted successfully!')
        return redirect('all_students')
    
    return render(request, 'admin_dashboard/delete_student.html', {'student_user': student_user})


@login_required(login_url='login')
@admin_required
def add_student(request):
    """Add new student"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
        else:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                role='student',
                status='approved'
            )
            messages.success(request, f'{first_name} {last_name} added as student!')
            return redirect('complete_add_student', user_id=user.id)
    
    return render(request, 'admin_dashboard/add_student.html')


@login_required(login_url='login')
@admin_required
def complete_add_student(request, user_id):
    """Complete adding student profile"""
    student_user = get_object_or_404(CustomUser, id=user_id, role='student')
    
    try:
        student_profile = student_user.student_profile
    except StudentProfile.DoesNotExist:
        student_profile = StudentProfile(user=student_user)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = student_user
            profile.profile_update_status = 'approved'
            profile.save()
            messages.success(request, 'Student profile created successfully!')
            return redirect('all_students')
    else:
        form = StudentProfileForm(instance=student_profile)
    
    context = {
        'form': form,
        'student_user': student_user,
    }
    return render(request, 'admin_dashboard/complete_add_student.html', context)


@login_required(login_url='login')
@admin_required
def all_teachers(request):
    """View all teachers"""
    teachers = CustomUser.objects.filter(role='teacher', status='approved')
    search = request.GET.get('search', '')
    
    if search:
        teachers = teachers.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(teacher_profile__employee_id__icontains=search) |
            Q(email__icontains=search)
        )
    
    context = {
        'teachers': teachers,
        'search': search,
    }
    return render(request, 'admin_dashboard/all_teachers.html', context)


@login_required(login_url='login')
@admin_required
def edit_teacher(request, user_id):
    """Edit teacher details"""
    teacher_user = get_object_or_404(CustomUser, id=user_id, role='teacher')
    
    try:
        teacher_profile = teacher_user.teacher_profile
    except TeacherProfile.DoesNotExist:
        teacher_profile = TeacherProfile(user=teacher_user)
    
    if request.method == 'POST':
        # Update user details
        teacher_user.first_name = request.POST.get('first_name')
        teacher_user.last_name = request.POST.get('last_name')
        teacher_user.email = request.POST.get('email')
        teacher_user.phone = request.POST.get('phone')
        dob_str = request.POST.get('date_of_birth')
        if dob_str:
            teacher_user.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
        teacher_user.save()
        # Update teacher profile
        form = TeacherProfileForm(request.POST, instance=teacher_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = teacher_user
            profile.profile_update_status = 'approved'
            
            # Update salary
            salary = request.POST.get('salary', 0)
            salary_paid = request.POST.get('salary_paid', 0)
            try:
                profile.salary = float(salary)
                profile.salary_paid = float(salary_paid)
            except:
                pass
            
            profile.save()
            messages.success(request, 'Teacher details updated successfully!')
            return redirect('all_teachers')
        else:
            print(form.errors)  # Debugging line to print form errors in the console
    else:
        form = TeacherProfileForm(instance=teacher_profile)
    
    context = {
        'form': form,
        'teacher_user': teacher_user,
        'teacher_profile': teacher_profile,
    }
    return render(request, 'admin_dashboard/edit_teacher.html', context)


@login_required(login_url='login')
@admin_required
def delete_teacher(request, user_id):
    """Delete teacher"""
    teacher_user = get_object_or_404(CustomUser, id=user_id, role='teacher')
    
    if request.method == 'POST':
        name = teacher_user.get_full_name()
        teacher_user.delete()
        messages.success(request, f'{name} has been deleted successfully!')
        return redirect('all_teachers')
    
    return render(request, 'admin_dashboard/delete_teacher.html', {'teacher_user': teacher_user})


@login_required(login_url='login')
@admin_required
def add_teacher(request):
    """Add new teacher"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
        else:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                role='teacher',
                status='approved'
            )
            messages.success(request, f'{first_name} {last_name} added as teacher!')
            return redirect('complete_add_teacher', user_id=user.id)
    
    return render(request, 'admin_dashboard/add_teacher.html')


@login_required(login_url='login')
@admin_required
def complete_add_teacher(request, user_id):
    """Complete adding teacher profile"""
    teacher_user = get_object_or_404(CustomUser, id=user_id, role='teacher')
    
    try:
        teacher_profile = teacher_user.teacher_profile
    except TeacherProfile.DoesNotExist:
        teacher_profile = TeacherProfile(user=teacher_user)
    
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=teacher_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = teacher_user
            profile.profile_update_status = 'approved'
            profile.save()
            messages.success(request, 'Teacher profile created successfully!')
            return redirect('all_teachers')
    else:
        form = TeacherProfileForm(instance=teacher_profile)
    
    context = {
        'form': form,
        'teacher_user': teacher_user,
    }
    return render(request, 'admin_dashboard/complete_add_teacher.html', context)


@login_required(login_url='login')
@admin_required
def attendance_view(request):
    """View attendance records"""
    filter_type = request.GET.get('filter', 'date')
    
    from attendance.models import AttendanceRecord
    attendance_records = AttendanceRecord.objects.all().order_by('-date')
    
    if filter_type == 'student':
        student_id = request.GET.get('student_id', '')
        if student_id:
            attendance_records = attendance_records.filter(student_id=student_id)
    
    context = {
        'attendance_records': attendance_records,
        'filter_type': filter_type,
    }
    return render(request, 'admin_dashboard/attendance_view.html', context)


@login_required(login_url='login')
@admin_required
def approve_profile_updates(request):
    """Approve pending profile updates"""
    pending_student_updates = StudentProfile.objects.filter(profile_update_status='pending')
    pending_teacher_updates = TeacherProfile.objects.filter(profile_update_status='pending')
    
    context = {
        'pending_student_updates': pending_student_updates,
        'pending_teacher_updates': pending_teacher_updates,
    }
    return render(request, 'admin_dashboard/approve_profile_updates.html', context)


@login_required(login_url='login')
@admin_required
def approve_student_profile_update(request, profile_id):
    """Approve student profile update"""
    profile = get_object_or_404(StudentProfile, id=profile_id)
    if request.method == 'POST':
        profile.profile_update_status = 'approved'
        profile.save()
        messages.success(request, f'{profile.user.get_full_name()} profile update approved!')
        return redirect('approve_profile_updates')
    return render(request, 'admin_dashboard/confirm_approve_profile.html', {'profile': profile})


@login_required(login_url='login')
@admin_required
def reject_student_profile_update(request, profile_id):
    """Reject student profile update"""
    profile = get_object_or_404(StudentProfile, id=profile_id)
    if request.method == 'POST':
        profile.profile_update_status = 'rejected'
        profile.save()
        messages.success(request, f'{profile.user.get_full_name()} profile update rejected!')
        return redirect('approve_profile_updates')
    return render(request, 'admin_dashboard/confirm_reject_profile.html', {'profile': profile})



@login_required(login_url='login')
@admin_required
def approve_teacher_profile_update(request, profile_id):
    """Approve teacher profile update"""
    profile = get_object_or_404(TeacherProfile, id=profile_id)
    if request.method == 'POST':
        profile.profile_update_status = 'approved'
        profile.save()
        messages.success(request, f'{profile.user.get_full_name()} teacher profile update approved!')
        return redirect('approve_profile_updates')
    return render(request, 'admin_dashboard/confirm_approve_profile.html', {'profile': profile})


@login_required(login_url='login')
@admin_required
def reject_teacher_profile_update(request, profile_id):
    """Reject teacher profile update"""
    profile = get_object_or_404(TeacherProfile, id=profile_id)
    if request.method == 'POST':
        profile.profile_update_status = 'rejected'
        profile.save()
        messages.success(request, f'{profile.user.get_full_name()} teacher profile update rejected!')
        return redirect('approve_profile_updates')
    return render(request, 'admin_dashboard/confirm_reject_profile.html', {'profile': profile})


@login_required(login_url='login')
@admin_required
def mark_notification_read(request, notification_id):
    """Mark notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('admin_dashboard')


# for lectures and timetable management, we can have views to add/edit/delete lectures and view timetable.
@login_required
@admin_required
def manage_timetable(request):
    """View and manage timetable"""
    lectures = Lecture.objects.all().order_by('day', 'start_time')
    
    context = {
        'lectures': lectures,
    }
    return render(request, 'admin_dashboard/manage_timetable.html', context)

@login_required
@admin_required
def add_lecture(request):
    if request.method == 'POST':
        form = LectureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lecture added successfully')
            return redirect('manage_timetable')
    else:
        form = LectureForm()
    
    context = {
        'form': form,
    }

    return render(request, 'admin_dashboard/add_lecture.html', context)

@login_required
@admin_required
def edit_lecture(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)

    if request.method == 'POST':
        form = LectureForm(request.POST, instance=lecture)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lecture updated successfully')
            return redirect('manage_timetable')
    else:
        form = LectureForm(instance=lecture)
    
    context = {
        'form': form,
        'lecture': lecture,
    }
    return render(request, 'admin_dashboard/edit_lecture.html', context)

@login_required
@admin_required
def delete_lecture(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)

    if request.method == 'POST':
        lecture.delete()
        messages.success(request, 'Lecture deleted')
        return redirect('manage_timetable')
    context = {
        'lecture': lecture,
    }
    return render(request, 'admin_dashboard/delete_lecture.html', context)

#veiw for managing(creating,deleting) new subjects and batches for timetable

@login_required
@admin_required
def manage_subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'admin_dashboard/manage_subjects.html', {
        'subjects': subjects
    })

@login_required
@admin_required
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added successfully')
            return redirect('manage_subjects')
    else:
        form = SubjectForm()

    return render(request, 'admin_dashboard/add_subject.html', {'form': form})

@login_required
@admin_required
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, 'Subject deleted successfully')
    return redirect('manage_subjects')


"""for the batch start here"""
@login_required
@admin_required
def manage_batches(request):
    batches = Batch.objects.all()
    return render(request, 'admin_dashboard/manage_batches.html', {
        'batches': batches
    })

@login_required
@admin_required
def add_batch(request):
    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Batch added successfully')
            return redirect('manage_batches')
    else:
        form = BatchForm()

    return render(request, 'admin_dashboard/add_batch.html', {'form': form})

@login_required
@admin_required
def delete_batch(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    batch.delete()
    messages.success(request, 'Batch deleted successfully')
    return redirect('manage_batches')





