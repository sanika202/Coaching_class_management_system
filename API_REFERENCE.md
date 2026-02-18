# TOPPERS API Reference

## 🔗 Complete URL Structure

### Authentication URLs
Base: `/auth/`

| URL | Method | View | Purpose |
|-----|--------|------|---------|
| `/` | GET | home() | Route to dashboard based on role |
| `register/` | GET, POST | register() | Student/Teacher registration |
| `login/` | GET, POST | login_view() | Login with role selection |
| `logout/` | POST | logout_view() | Logout and session cleanup |
| `complete-profile/student/` | GET, POST | complete_profile_student() | Finalize student profile |
| `complete-profile/teacher/` | GET, POST | complete_profile_teacher() | Finalize teacher profile |

---

## Admin Dashboard URLs
Base: `/admin-dashboard/`

### Dashboard & Overview
| URL | Method | View | Purpose |
|-----|--------|------|---------|
| `` | GET | admin_dashboard() | Main dashboard with stats |

### Registration Management
| URL | Method | View | Purpose |
|-----|--------|------|---------|
| `pending-registrations/` | GET | pending_registrations() | View pending approvals |
| `approve/<int:user_id>/` | POST | approve_registration() | Approve registration |
| `reject/<int:user_id>/` | POST | reject_registration() | Reject registration |

### Student Management
| URL | Method | View | Purpose |
|-----|--------|------|---------|
| `all-students/` | GET | all_students() | List students (searchable) |
| `edit-student/<int:user_id>/` | GET, POST | edit_student() | Edit student details |
| `delete-student/<int:user_id>/` | GET, POST | delete_student() | Delete student |
| `add-student/` | GET, POST | add_student() | Create student (step 1) |
| `complete-add-student/<int:user_id>/` | GET, POST | complete_add_student() | Complete profile (step 2) |

### Teacher Management
| URL | Method | View | Purpose |
|-----|--------|------|---------|
| `all-teachers/` | GET | all_teachers() | List teachers (searchable) |
| `edit-teacher/<int:user_id>/` | GET, POST | edit_teacher() | Edit teacher details |
| `delete-teacher/<int:user_id>/` | GET, POST | delete_teacher() | Delete teacher |
| `add-teacher/` | GET, POST | add_teacher() | Create teacher (step 1) |
| `complete-add-teacher/<int:user_id>/` | GET, POST | complete_add_teacher() | Complete profile (step 2) |

### Attendance Management
| URL | Method | View | Purpose |
|-----|--------|------|---------|
| `attendance/` | GET | attendance_view() | View all attendance records |

### Profile Updates
| URL | Method | View | Purpose |
|-----|--------|------|---------|
| `profile-updates/` | GET | approve_profile_updates() | Approve profile update requests |
| `approve-student-update/<int:profile_id>/` | POST | approve_student_profile_update() | Approve student profile update |
| `reject-student-update/<int:profile_id>/` | POST | reject_student_profile_update() | Reject student profile update |

### Notifications
| URL | Method | View | Purpose |
|-----|--------|------|---------|
| `notification/<int:notification_id>/read/` | POST | mark_notification_read() | Mark notification as read |

---

## Student Portal URLs
Base: `/student/`

| URL | Method | View | Purpose |
|-----|--------|------|---------|
| `dashboard/` | GET | student_dashboard() | Student dashboard with stats |
| `profile/` | GET | student_profile() | View student profile |
| `attendance/` | GET | student_attendance() | View attendance records |
| `fees/` | GET | student_fees() | View fees information |
| `lectures/` | GET | student_lectures() | View upcoming lectures |
| `update-profile/` | GET, POST | update_student_profile() | Update profile with approval |

---

## Teacher Portal URLs
Base: `/teacher/`

| URL | Method | View | Purpose |
|-----|--------|------|---------|
| `dashboard/` | GET | teacher_dashboard() | Teacher dashboard with stats |
| `profile/` | GET | teacher_profile() | View teacher profile |
| `lectures/` | GET | teacher_lectures() | View assigned lectures |
| `mark-attendance/<int:lecture_id>/` | GET, POST | mark_attendance() | Mark student attendance |
| `salary/` | GET | teacher_salary() | View salary information |
| `update-profile/` | GET, POST | update_teacher_profile() | Update profile with approval |

---

## Attendance URLs
Base: `/attendance/`

| URL | Method | View | Purpose |
|-----|--------|------|---------|
| `list/` | GET | attendance_list() | List all attendance records |

---

## 📤 Form Data Specifications

### Registration Form
```python
{
    'username': str,       # Required, unique
    'email': str,          # Required, unique
    'first_name': str,     # Required
    'last_name': str,      # Required
    'password1': str,      # Required, min 8 chars
    'password2': str,      # Required, must match password1
    'role': 'student'|'teacher',  # Required
    'phone': str,          # Optional
    'date_of_birth': date, # Optional
    'address': str,        # Optional
    'profile_image': file, # Optional
}
```

### Login Form
```python
{
    'username': str,                    # Required
    'password': str,                    # Required
    'role': 'admin'|'student'|'teacher' # Required
}
```

### Student Profile Completion
```python
{
    'enrollment_number': str,  # Required, unique
    'guardian_name': str,      # Required
    'guardian_phone': str,     # Required
    'batch': str,              # Required
    'subjects': str,           # Required (comma-separated)
    'total_fees': float,       # Required
}
```

### Teacher Profile Completion
```python
{
    'employee_id': str,       # Required, unique
    'qualifications': str,    # Required
    'subjects_taught': str,   # Required (comma-separated)
    'experience': int,        # Required (years)
    'salary': float,          # Required
}
```

### Student Profile Update
```python
{
    'guardian_name': str,      # Optional
    'guardian_phone': str,     # Optional
    'batch': str,              # Optional
    'subjects': str,           # Optional
    # Will create notification for admin approval
}
```

### Teacher Profile Update
```python
{
    'qualifications': str,     # Optional
    'subjects_taught': str,    # Optional
    'experience': int,         # Optional
    # Will create notification for admin approval
}
```

### Student Edit (Admin)
```python
{
    'first_name': str,         # Optional
    'last_name': str,          # Optional
    'email': str,              # Optional
    'phone': str,              # Optional
    'enrollment_number': str,  # Optional
    'batch': str,              # Optional
    'total_fees': float,       # Optional
    'fees_paid': float,        # Optional (admin can update directly)
    'profile_image': file,     # Optional
}
```

### Teacher Edit (Admin)
```python
{
    'first_name': str,         # Optional
    'last_name': str,          # Optional
    'email': str,              # Optional
    'phone': str,              # Optional
    'employee_id': str,        # Optional
    'salary': float,           # Optional (admin can update directly)
    'experience': int,         # Optional
    'profile_image': file,     # Optional
}
```

### Attendance Marking (Teacher)
```python
{
    'student_<id>': 'present'|'absent'  # For each student in batch
}
```

---

## 🔑 Query Parameters

### All Students Search
```
GET /admin-dashboard/all-students/?search=<query>&search_by=name|enrollment|email
```

### All Teachers Search
```
GET /admin-dashboard/all-teachers/?search=<query>&search_by=name|employee_id|email
```

### Attendance Filtering
```
GET /admin-dashboard/attendance/?date=<YYYY-MM-DD>&student=<user_id>
```

---

## 📊 Response Data

### Dashboard (Admin)
```python
{
    'total_students': int,
    'total_teachers': int,
    'pending_approvals': int,
    'recent_notifications': [
        {
            'id': int,
            'title': str,
            'message': str,
            'notification_type': str,
            'created_at': datetime,
            'is_read': bool
        },
        ...
    ]
}
```

### Dashboard (Student)
```python
{
    'total_classes': int,
    'classes_attended': int,
    'attendance_percentage': float,
    'fees_info': {
        'total': float,
        'paid': float,
        'remaining': float
    },
    'upcoming_lectures': [
        {
            'id': int,
            'subject': str,
            'batch': str,
            'teacher': str,
            'class_date': date,
            'start_time': time,
            'end_time': time,
        },
        ...
    ]
}
```

### Dashboard (Teacher)
```python
{
    'total_lectures': int,
    'salary': float,
    'experience': int,
    'upcoming_lectures': [
        {
            'id': int,
            'subject': str,
            'batch': str,
            'class_date': date,
            'start_time': time,
        },
        ...
    ]
}
```

---

## 🔐 Access Control

### Admin-Only Routes
- `/admin-dashboard/*` - Requires `role='admin'` and authenticated
- Admin approval operations
- All management functions

### Student-Only Routes
- `/student/*` - Requires `role='student'` and `status='approved'`
- Own profile/attendance/fees viewing only
- Cannot modify other students' data

### Teacher-Only Routes
- `/teacher/*` - Requires `role='teacher'` and `status='approved'`
- Own profile/salary viewing
- Can mark attendance for own lectures
- Cannot modify other teachers' data

### Public Routes
- `/auth/` (home, register, login) - Unauthenticated users
- Authentication required after login

---

## 🎯 Status Codes & Errors

### Success Responses
```
200 OK - Request successful
201 Created - New resource created
302 Found - Redirect (after form submission)
```

### Error Responses
```
400 Bad Request - Invalid form data
401 Unauthorized - Not authenticated
403 Forbidden - No permission for this role
404 Not Found - Resource doesn't exist
500 Internal Server Error - Server error
```

### Form Validation Errors
Returned as form errors in context:
```python
{
    'field_name': ['Error message 1', 'Error message 2']
}
```

---

## 📝 Authentication Flow

### Registration Flow
```
1. POST /auth/register/ with registration data
   ↓
2. CustomUser created with status='pending'
3. Redirect to login page
4. Admin approves /admin-dashboard/approve/<user_id>/
5. User status → 'approved'
6. User visits /auth/login/
7. Redirects to /auth/complete-profile/<role>/
8. User completes profile
9. Redirect to role dashboard
```

### Login Flow
```
1. GET /auth/login/
2. POST with username, password, role
3. Role verification (role in database matches selected role)
4. Status check (must be 'approved', not 'pending' or 'rejected')
5. Session created
6. Auto-redirect to role dashboard or complete profile
7. Notification created (auto-logged login event)
```

### Logout Flow
```
1. POST /auth/logout/
2. Session destroyed
3. Redirect to /auth/ (home)
```

---

## 🔄 Data Update Workflows

### Fees Payment (Admin)
```
1. Admin visits /admin-dashboard/edit-student/<id>/
2. Updates fees_paid field
3. StudentProfile.fees_paid updated
4. fees_remaining calculated automatically
5. Notification auto-created
```

### Salary Update (Admin)
```
1. Admin visits /admin-dashboard/edit-teacher/<id>/
2. Updates salary field
3. TeacherProfile.salary updated
4. Notification auto-created
```

### Student Profile Update (Self)
```
1. Student visits /student/update-profile/
2. Submits changes
3. profile_update_status set to 'pending'
4. Notification → Admin
5. Admin reviews /admin-dashboard/profile-updates/
6. Admin approves/rejects
7. Status updated and notification sent to student
```

### Attendance Marking (Teacher)
```
1. Teacher visits /teacher/mark-attendance/<lecture_id>/
2. Shows all students in batch as radio buttons
3. Selects present/absent for each
4. POST creates/updates AttendanceRecord entries
5. Redirect to mark next/view lectures
6. Student can see in /student/attendance/
```

---

## 🛠️ Helper Functions & Utilities

### Decorators
```python
@login_required  # From Django, checks authentication
@user_passes_test(lambda u: u.role == 'admin')  # Custom role check
```

### Template Tags
```html
{% if user.role == 'admin' %}...{% endif %}
{% if user.status == 'approved' %}...{% endif %}
{% widthratio value max_value 100 %}  # Percentage calculation
```

### Model Methods
```python
StudentProfile.fees_remaining  # Calculated property
```

### Signal Handlers
```
post_save(CustomUser) → Creates Notification automatically
post_save(StudentProfile) → Triggers on profile completion
```

---

## 📋 Search & Filter Examples

### Search Students
```
GET /admin-dashboard/all-students/?search=john&search_by=name
GET /admin-dashboard/all-students/?search=2024001&search_by=enrollment
GET /admin-dashboard/all-students/?search=john@email.com&search_by=email
```

### Filter Attendance
```
GET /admin-dashboard/attendance/?date=2024-01-15
GET /admin-dashboard/attendance/?student=5
GET /admin-dashboard/attendance/?date=2024-01-15&student=5
```

### Search Teachers
```
GET /admin-dashboard/all-teachers/?search=smith&search_by=name
GET /admin-dashboard/all-teachers/?search=EMP001&search_by=employee_id
GET /admin-dashboard/all-teachers/?search=smith@email.com&search_by=email
```

---

## 🔗 Related Resource Links

- [Database Schema](DATABASE_SCHEMA.md) - Model structure and relationships
- [Setup Guide](SETUP_GUIDE.md) - Installation and configuration
- [Features List](FEATURES.md) - Complete feature documentation
- [README](README.md) - Project overview

---

## 💡 Common Workflows

### Complete New Student Registration
```
1. Student: Register at /auth/register/ (role=student)
2. Admin: Review at /admin-dashboard/pending-registrations/
3. Admin: Approve /admin-dashboard/approve/<id>/
4. Student: Login at /auth/login/
5. Student: Complete profile at /auth/complete-profile/student/
6. Student: Access dashboard at /student/dashboard/
```

### Manage Student Fees
```
1. Admin: Navigate to /admin-dashboard/all-students/
2. Admin: Open student's edit page /admin-dashboard/edit-student/<id>/
3. Admin: Update total_fees and/or fees_paid
4. Admin: Save (notification auto-created)
5. Student: Check fees at /student/fees/
6. Student: See fees_remaining = total_fees - fees_paid
```

### Mark Class Attendance
```
1. Teacher: Navigate to /teacher/dashboard/
2. Teacher: Find lecture and click "Mark Attendance"
3. Teacher: Check/uncheck students as present/absent
4. Teacher: Submit (creates AttendanceRecord entries)
5. Student: View at /student/attendance/
6. Admin: View at /admin-dashboard/attendance/
```

### Approve Profile Update
```
1. Student: Update profile at /student/update-profile/
2. Status → pending, notification sent to admin
3. Admin: Review at /admin-dashboard/profile-updates/
4. Admin: Approve or Reject
5. StudentProfile updated, notification sent to student
```

---

**Last Updated:** 2024
**Compatible Version:** Django 4.2.7+
