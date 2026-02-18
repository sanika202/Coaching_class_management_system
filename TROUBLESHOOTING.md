# TOPPERS - Troubleshooting Guide

## 🔧 Common Issues & Solutions

### Setup & Installation

#### Issue: "ModuleNotFoundError: No module named 'django'"
**Cause:** Django not installed or wrong Python environment
**Solution:**
```bash
# Make sure you're in the project directory
cd c:\sanika\python_project_sem2\toppers

# Install requirements
pip install -r requirements.txt

# Verify installation
python -m django --version
```

---

#### Issue: "No such file or directory: 'manage.py'"
**Cause:** Not in the correct project directory
**Solution:**
```bash
# Navigate to project root (where manage.py is located)
cd c:\sanika\python_project_sem2\toppers

# List files to confirm
dir  # Windows
ls   # Mac/Linux

# Should show: manage.py and toppers_project folder
```

---

#### Issue: "python: command not found" or "python is not recognized"
**Cause:** Python not in system PATH
**Solution:**
```bash
# Try using python3
python3 --version

# If that works, use:
python3 manage.py runserver

# Add Python to PATH (Windows):
# Control Panel → System → Advanced → Environment Variables
# Add C:\Users\YourUsername\AppData\Local\Programs\Python\Python310 to PATH
```

---

#### Issue: "error: Microsoft Visual C++ 14.0 or greater is required" (Windows)
**Cause:** Pillow needs Visual C++ for image processing
**Solution:**
```bash
# Option 1: Install pre-built Pillow wheel
pip install --upgrade pillow

# Option 2: Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

---

### Database Issues

#### Issue: "OperationalError: no such table: core_customuser"
**Cause:** Database migrations not run
**Solution:**
```bash
# Run migrations
python manage.py migrate

# If still issues, reset database:
python manage.py migrate core zero  # Rollback core app
python manage.py migrate             # Re-run migrations
```

---

#### Issue: "UNIQUE constraint failed: core_customuser.username"
**Cause:** Username already exists in database
**Solution:**
```bash
# Option 1: Use different username
# Register again with different username

# Option 2: Reset database (clear all data)
# Delete file: toppers_project/db.sqlite3
# Then run: python manage.py migrate
```

---

#### Issue: "IntegrityError: UNIQUE constraint failed: core_studentprofile.enrollment_number"
**Cause:** Enrollment number already exists
**Solution:**
```bash
# During registration/admin add, use unique enrollment number
# Check existing students: /admin-dashboard/all-students/
# Use different enrollment number (e.g., 2024002, 2024003)
```

---

### Login & Authentication

#### Issue: "Login fails silently, page redirects back to login"
**Cause:** Multiple possible reasons - check each:

1. **User not approved yet**
   - Solution: Admin must approve at `/admin-dashboard/pending-registrations/`
   - Status must be 'approved' (not 'pending' or 'rejected')

2. **Wrong role selected**
   - Solution: Select same role as registration
   - Student must login as 'student', teacher as 'teacher'

3. **Password incorrect**
   - Solution: Verify password carefully
   - Passwords are case-sensitive

4. **Wrong username**
   - Solution: Check username, not email
   - Use username field, not email field

**Debug Steps:**
```bash
# Check user in database
python manage.py shell
>>> from core.models import CustomUser
>>> CustomUser.objects.filter(username='testuser').values()
# Check: status, role, is_active
```

---

#### Issue: "Page says 'Pending Approval'"
**Cause:** Admin hasn't approved registration
**Solution:**
1. Admin must login
2. Go to `/admin-dashboard/pending-registrations/`
3. Click "Approve" button
4. User can login after approval

---

#### Issue: "After login, always redirected to 'Complete Profile'"
**Cause:** Profile not completed yet
**Solution:**
1. Complete the profile form
2. Fill all required fields
3. Submit form
4. Now should access dashboard

---

### Views & Pages

#### Issue: "404 Not Found" when accessing dashboard
**Cause:** Missing app configuration or URL routing issue
**Solution:**
```bash
# Verify all apps in settings.py
python manage.py check

# Clear browser cache and try again
# Hard refresh: Ctrl+Shift+Delete (Chrome) or Cmd+Shift+Delete (Mac)

# Restart development server
python manage.py runserver
```

---

#### Issue: "Permission denied" or "403 Forbidden"
**Cause:** User role doesn't match URL
**Solution:**
1. Student accessing `/teacher/` - Login as teacher instead
2. Teacher accessing `/student/dashboard/` - Student account required
3. Non-admin accessing `/admin-dashboard/` - Login as admin

**Correct URLs by role:**
```
Admin:   /admin-dashboard/*
Student: /student/*
Teacher: /teacher/*
```

---

#### Issue: "Static files (CSS/images) not loading"
**Cause:** Static files not collected or server not configured correctly
**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# For development, should auto-serve:
# If not, restart server: python manage.py runserver

# Check browser console for 404 errors (F12 → Network tab)
# Look for failed CSS/image requests
```

---

#### Issue: "Images not showing (broken images)"
**Cause:** Image file missing or path incorrect
**Solution:**
```bash
# Check media files folder:
# Should be at: toppers/media/

# Verify settings.py has:
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# For development, add to urls.py:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Clear browser cache and refresh
```

---

### Features Not Working

#### Issue: "Can't mark attendance - no students showing"
**Cause:** Students not in matching batch
**Solution:**
1. Verify lecture has correct batch assigned
2. Verify students have same batch in profile
3. Students must be approved status
4. Reload page: Ctrl+F5

**Debug:**
```bash
python manage.py shell
>>> from core.models import Lecture, CustomUser
>>> lecture = Lecture.objects.first()
>>> lecture.batch
'2024A'  # Check batch
>>> CustomUser.objects.filter(
...     role='student', 
...     student_profile__batch='2024A',
...     status='approved'
... ).count()
# Should show number of matching students
```

---

#### Issue: "Profile update stuck on 'pending' approval"
**Cause:** Admin hasn't approved the update
**Solution:**
1. Admin login
2. `/admin-dashboard/profile-updates/`
3. Find pending update
4. Click "Approve" or "Reject"
5. Student gets notification

---

#### Issue: "Attendance percentage showing wrong"
**Cause:** Calculation logic or missing records
**Solution:**
```bash
# Verify records exist
python manage.py shell
>>> from core.models import AttendanceRecord
>>> AttendanceRecord.objects.filter(student_id=5).count()
# Should show attendance record count

# Verify lecture records
>>> from core.models import Lecture
>>> Lecture.objects.filter(batch='2024A').count()
# Should show lectures for batch
```

---

#### Issue: "Can't see fees or salary information"
**Cause:** Profile not complete or admin hasn't set values
**Solution:**
1. **For students:** Verify StudentProfile.total_fees is set
   - Admin: `/admin-dashboard/edit-student/<id>/`
   - Set "Total Fees" field
   - Save changes

2. **For teachers:** Verify TeacherProfile.salary is set
   - Admin: `/admin-dashboard/edit-teacher/<id>/`
   - Set "Salary" field
   - Save changes

3. **Search by:**
   - Student: `/student/fees/`
   - Teacher: `/teacher/salary/`

---

### Notifications

#### Issue: "Not seeing notifications"
**Cause:** New notifications might not be visible if dismissed
**Solution:**
1. Notifications appear in top navbar
2. Click bell icon to expand
3. Marked as read when clicked
4. Admin can mark as read/unread

**Debug:**
```bash
python manage.py shell
>>> from core.models import Notification
>>> Notification.objects.filter(user_id=1).order_by('-created_at')[:5]
# Shows recent 5 notifications for user 1
```

---

#### Issue: "No notifications received for events"
**Cause:** Signals not loading or notification creation failed
**Solution:**
```bash
# Check core/apps.py has ready() method:
# File should have: from .signals import *

# Restart server to reload signals:
python manage.py runserver

# Verify signal execution:
python manage.py shell
>>> from django.core.signals import pre_delete
>>> from core.signals import *
# Should not raise errors
```

---

### Performance Issues

#### Issue: "Page loading very slowly"
**Cause:** Database queries or missing indexing
**Solution:**
```bash
# Check for N+1 query problem:
# Django debug toolbar (install separately):
pip install django-debug-toolbar

# Or reduce pagination limit in views.py:
# Change: paginate_by = 50
# To: paginate_by = 10

# Restart server after changes
python manage.py runserver
```

---

#### Issue: "Database file getting too large"
**Cause:** Too many notifications or test data
**Solution:**
```bash
# Clean old notifications:
python manage.py shell
>>> from core.models import Notification
>>> from django.utils import timezone
>>> from datetime import timedelta
>>> old_date = timezone.now() - timedelta(days=30)
>>> Notification.objects.filter(created_at__lt=old_date).delete()
# Deletes notifications older than 30 days

# Or reset entire database (removes all data):
# Delete: toppers/db.sqlite3
# Then: python manage.py migrate
```

---

### Admin Panel Issues

#### Issue: "Can't access Django admin panel"
**Cause:** Superuser not created or not logged in
**Solution:**
```bash
# Create superuser
python manage.py createsuperuser
# Follow prompts

# Then visit: http://127.0.0.1:8000/admin/
# Login with superuser credentials
```

---

#### Issue: "Admin panel shows models but can't edit"
**Cause:** Admin configuration missing
**Solution:**
- Check `core/admin.py` has model registrations
- Should have: `admin.site.register(CustomUser, CustomUserAdmin)`
- If missing, add model to admin.py
- Restart server

---

### Server Issues

#### Issue: "Port 8000 already in use"
**Cause:** Another process using port or server not shut down
**Solution:**
```bash
# Option 1: Use different port
python manage.py runserver 8001

# Option 2: Kill existing process (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Option 3: Kill existing process (Mac/Linux)
lsof -ti:8000 | xargs kill -9
```

---

#### Issue: "DisallowedHost at /"
**Cause:** Host not in ALLOWED_HOSTS in settings
**Solution:**
```python
# Edit: toppers_project/settings.py
# Find: ALLOWED_HOSTS = []
# Change to: ALLOWED_HOSTS = ['*']  # Development only!

# Or specific hosts:
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'yourdomain.com']

# Restart server
```

---

#### Issue: "CSRF token missing or incorrect"
**Cause:** Form submitted without CSRF token
**Solution:**
1. Ensure all forms include: `{% csrf_token %}`
2. Check template for missing token tag
3. Clear browser cookies (Ctrl+Shift+Delete)
4. Refresh page and try again

**In template:**
```html
<form method="POST">
    {% csrf_token %}  <!-- Must include this -->
    <!-- form fields -->
    <button type="submit">Submit</button>
</form>
```

---

## 🆘 Getting Help

### Debug Information to Collect
When reporting issues, gather:
```
1. Error message (exact text)
2. URL where error occurs
3. Browser console errors (F12 → Console)
4. Server console output (terminal where runserver runs)
5. Steps to reproduce
6. Your username/role type
7. Django version: python manage.py --version
8. Database: check toppers/db.sqlite3 exists
```

### Reset Everything (Nuclear Option)
```bash
# Use only if nothing works - removes all data!
# Delete database
rm toppers/db.sqlite3  # Mac/Linux
del toppers\db.sqlite3  # Windows

# Delete migrations (keep __init__.py)
# In each app folder, delete .py files except __init__.py

# Recreate everything:
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py create_sample_data
python manage.py runserver
```

---

## 📞 Support Resources

### Check These Files First
1. [README.md](README.md) - Project overview
2. [SETUP_GUIDE.md](SETUP_GUIDE.md) - Installation steps
3. [FEATURES.md](FEATURES.md) - Feature list
4. [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) - Model documentation
5. [API_REFERENCE.md](API_REFERENCE.md) - URL and form specifications

### Django Documentation
- Main: https://docs.djangoproject.com/
- Models: https://docs.djangoproject.com/en/4.2/topics/db/models/
- Views: https://docs.djangoproject.com/en/4.2/topics/http/views/
- Forms: https://docs.djangoproject.com/en/4.2/topics/forms/

### Common Commands Reference
```bash
# Start server
python manage.py runserver

# Database operations
python manage.py migrate
python manage.py makemigrations

# User operations
python manage.py createsuperuser
python manage.py changepassword <username>

# Shell access
python manage.py shell

# Test data
python manage.py create_sample_data

# Collect static files
python manage.py collectstatic --noinput

# Check configuration
python manage.py check
```

---

**Last Updated:** 2024
**Version:** 1.0
