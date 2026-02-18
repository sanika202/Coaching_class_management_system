from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from core.models import CustomUser, StudentProfile, TeacherProfile, Notification
from core.forms import CustomUserCreationForm, LoginForm, StudentProfileForm, TeacherProfileForm


def home(request):
    """Home page view"""
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        elif request.user.role == 'student':
            return redirect('student_dashboard')
        elif request.user.role == 'teacher':
            return redirect('teacher_dashboard')
    
    return render(request, 'authentication/home.html')


def register(request):
    """User registration view"""
    if request.method == 'POST':
        role = request.POST.get('role')
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.role = role
            user.save()
            messages.success(request, f'Registration successful! Please login with your credentials.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'authentication/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.role != role:
                messages.error(request, f'Invalid role selected. You are registered as {user.get_role_display()}')
                return redirect('login')
            
            if user.status == 'pending':
                messages.warning(request, 'Your account is pending approval from admin.')
                return redirect('login')
            
            if user.status == 'rejected':
                messages.error(request, 'Your account has been rejected by admin.')
                return redirect('login')
            
            login(request, user)
            
            # Create login notification for admin
            if user.role != 'admin':
                admin = CustomUser.objects.filter(role='admin').first()
                if admin:
                    Notification.objects.create(
                        user=admin,
                        notification_type='login',
                        title=f'{user.get_full_name()} Logged In',
                        message=f'{user.get_full_name()} has logged in to the system',
                        related_user=user
                    )
            
            messages.success(request, f'Welcome {user.get_full_name()}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    
    form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')


@login_required(login_url='login')
def complete_profile_student(request):
    """Complete student profile after approval"""
    if request.user.role != 'student':
        return redirect('home')
    
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        student_profile = StudentProfile(user=request.user)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.profile_update_status = 'pending'
            profile.save()
            
            # Create notification for admin
            admin = CustomUser.objects.filter(role='admin').first()
            if admin:
                Notification.objects.create(
                    user=admin,
                    notification_type='profile_update',
                    title=f'Student Profile Update - {request.user.get_full_name()}',
                    message=f'{request.user.get_full_name()} has submitted their complete profile details',
                    related_user=request.user
                )
            
            messages.success(request, 'Profile submitted for admin approval!')
            return redirect('student_dashboard')
    else:
        form = StudentProfileForm(instance=student_profile)
    
    return render(request, 'authentication/complete_profile_student.html', {'form': form})


@login_required(login_url='login')
def complete_profile_teacher(request):
    """Complete teacher profile after approval"""
    if request.user.role != 'teacher':
        return redirect('home')
    
    try:
        teacher_profile = request.user.teacher_profile
    except TeacherProfile.DoesNotExist:
        teacher_profile = TeacherProfile(user=request.user)
    
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=teacher_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.profile_update_status = 'pending'
            profile.save()
            form.save_m2m()  # Save many-to-many relationships
            
            # Create notification for admin
            admin = CustomUser.objects.filter(role='admin').first()
            if admin:
                Notification.objects.create(
                    user=admin,
                    notification_type='profile_update',
                    title=f'Teacher Profile Update - {request.user.get_full_name()}',
                    message=f'{request.user.get_full_name()} has submitted their complete profile details',
                    related_user=request.user
                )
            
            messages.success(request, 'Profile submitted for admin approval!')
            return redirect('teacher_dashboard')
    else:
        form = TeacherProfileForm(instance=teacher_profile)
    
    return render(request, 'authentication/complete_profile_teacher.html', {'form': form})
