# TOPPERS - Coaching Class Management System

A comprehensive Django-based management system for coaching classes with role-based access control for Admin, Student, and Teacher.

## Features

### 🎓 Student Features
- Register and await admin approval
- Complete profile after approval
- View upcoming lectures
- Track attendance with percentage
- View fees details (paid/remaining)
- Update profile details (requires admin approval)

### 👨‍🏫 Teacher Features
- Register and await admin approval  
- Complete profile after approval
- View all assigned lectures
- Mark student attendance
- View salary information
- Update profile details (requires admin approval)

### 👨‍💼 Admin Features
- Dashboard with statistics
- View and approve pending registrations
- Manage students (add, edit, delete)
- Manage teachers (add, edit, delete)
- View attendance records (date-wise and student-wise)
- Manage fees for students
- Manage salary for teachers
- Approve/reject profile updates
- View all notifications

### 🔔 Notifications
- All registration and approval activities generate notifications
- Profile update requests visible in admin dashboard
- Real-time activity tracking

### 💰 Fees & Salary Management
- Track student fees (paid/remaining)
- Manage teacher salaries
- Admin can update fees and salary information

## Tech Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite3
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Python**: 3.8+

## Installation

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
source venv/bin/activate      # On macOS/Linux
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

When prompted:
- Username: admin
- Email: admin@toppers.com
- Password: (choose a secure password)
- Role: Enter '1' for admin

### 5. Run Dev Server

```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

## Default Login Credentials

After running migrations, you can access:

### Admin Panel
- URL: `http://127.0.0.1:8000/admin/`
- Use the superuser credentials you created

### Application Login
- URL: `http://127.0.0.1:8000/login/`
- Test with sample accounts after creation

## Usage

### Registration Flow

1. **Students & Teachers** can register themselves on the registration page
2. **Admin** reviews pending registrations on the dashboard
3. **Admin** approves or rejects registrations
4. **Approved users** complete their profile (required form)
5. **Admin** reviews profile updates
6. **After approval**, users can access their dashboards

### Admin Workflow

1. Go to Admin Dashboard
2. View "Pending Approvals" to accept new registrations
3. Manage Students/Teachers using the provided options
4. Review and update fees/salary
5. Check notifications for all activities

### Student Workflow

1. Register and wait for approval
2. Complete profile when approved
3. View dashboard with attendance and fees
4. Check upcoming lectures
5. Update profile (requires approval)

### Teacher Workflow

1. Register and wait for approval
2. Complete profile when approved
3. View assigned lectures
4. Mark attendance for students
5. Update profile (requires approval)

## Database Models

### Core Models
- **CustomUser**: Base user model with role-based access
- **StudentProfile**: Student academic information and fees
- **TeacherProfile**: Teacher professional info and salary
- **Lecture**: Class schedule and details
- **AttendanceRecord**: Student attendance tracking
- **Notification**: Activity notifications for admin

## Project Structure

```
toppers/
├── manage.py
├── requirements.txt
├── toppers_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── __init__.py
├── core/
│   ├── models.py
│   ├── forms.py
│   ├── admin.py
│   ├── views.py
│   └── apps.py
├── authentication/
│   ├── views.py
│   ├── urls.py
│   └── apps.py
├── admin_dashboard/
│   ├── views.py
│   ├── urls.py
│   └── apps.py
├── student/
│   ├── views.py
│   ├── urls.py
│   └── apps.py
├── teacher/
│   ├── views.py
│   ├── urls.py
│   └── apps.py
├── attendance/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── apps.py
├── templates/
│   ├── base.html
│   ├── authentication/
│   ├── admin_dashboard/
│   ├── student/
│   └── teacher/
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Important Notes

1. **Roles**:
   - Admin: Full system access
   - Student: Can register, view attendance and fees
   - Teacher: Can register, mark attendance

2. **Approval Workflow**:
   - All new registrations require admin approval
   - Profile updates need admin review
   - Dashboard notifications keep admin informed

3. **Attendance**:
   - Teachers mark attendance per lecture
   - Students can view attendance percentage
   - Admin can view attendance records

4. **Fees & Salary**:
   - Admin manages student fees
   - Admin manages teacher salary
   - Students can track fees status
   - Teachers can view their salary

## Security Features

- Password hashing with Django's built-in system
- CSRF protection enabled
- User role-based access control
- Admin approval workflow for accounts
- Session-based authentication

## Future Enhancements

- Email notifications
- SMS alerts for fees/attendance
- Payment gateway integration
- Performance analytics dashboard
- Batch scheduling
- Document upload (certificates, assignments)

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Ensure virtual environment is activated and all requirements are installed
```bash
pip install -r requirements.txt
```

### Issue: Database errors  
**Solution**: Reset migrations
```bash
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
```

### Issue: Static files not loading
**Solution**: Collect static files (for production)
```bash
python manage.py collectstatic
```

## Support

For issues or questions, please contact the development team.

## License

This project is for educational purposes.

## Author

Created for College Semester 2 Project - TOPPERS Coaching Class Management System
