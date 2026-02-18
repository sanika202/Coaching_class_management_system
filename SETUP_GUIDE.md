# TOPPERS Setup Guide

## ⚡ Quick Start

### Option 1: Automated Setup (Windows)

```batch
cd toppers
setup.bat
python manage.py createsuperuser
python manage.py create_sample_data
python manage.py runserver
```

### Option 2: Automated Setup (macOS/Linux)

```bash
cd toppers
chmod +x setup.sh
./setup.sh
python manage.py createsuperuser
python manage.py create_sample_data
python manage.py runserver
```

### Option 3: Manual Setup

#### 1. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 4. Create Admin User
```bash
python manage.py createsuperuser
```

Follow the prompts and enter:
- Username: `admin` (or any username)
- Email: `admin@toppers.com` (or any email)
- Password: (choose a secure password)
- Role: When prompted for role, enter the numeric choice for admin (usually 1 or pick "admin")

#### 5. (Optional) Load Sample Data
```bash
python manage.py create_sample_data
```

This creates:
- 1 Admin account: `admin` / `admin123`
- 6 Sample Students: `student1-6` / `student123`
- 6 Sample Teachers: `teacher1-6` / `teacher123`
- 12 Sample Lectures
- Sample attendance records

#### 6. Start Development Server
```bash
python manage.py runserver
```

Server will be available at: `http://127.0.0.1:8000/`

## 🎯 First Steps After Setup

### 1. Access the Application
- Home: `http://127.0.0.1:8000/`
- Login: `http://127.0.0.1:8000/login/`
- Register: `http://127.0.0.1:8000/auth/register/`

### 2. Login as Admin
- Go to Login
- Username: `admin`
- Password: (your chosen password)
- Role: **Admin**

### 3. Explore Admin Dashboard
- View pending registrations
- Manage students and teachers
- Add new students/teachers manually
- Approve/reject profile updates
- View attendance records
- Manage fees and salary

### 4. Test Student Role (if sample data loaded)
- Login with `student1` / `student123` as `Student`
- View attendance
- Check fees status
- See upcoming lectures

### 5. Test Teacher Role (if sample data loaded)
- Login with `teacher1` / `teacher123` as `Teacher`
- View assigned lectures
- Mark attendance
- View salary information

## 📁 Project Structure

```
toppers/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── README.md                          # Documentation
├── setup.bat / setup.sh              # Setup scripts
├── test_installation.py              # Installation test
├── .gitignore                        # Git configuration
│
├── toppers_project/                  # Main project folder
│   ├── __init__.py
│   ├── settings.py                   # Django settings
│   ├── urls.py                       # Main URL routing
│   ├── wsgi.py / asgi.py
│
├── core/                             # Core app (models, forms)
│   ├── models.py                     # All models
│   ├── forms.py                      # Forms
│   ├── admin.py                      # Admin configuration
│   ├── signals.py                    # Signal handlers
│   ├── views.py
│   └── management/
│       └── commands/
│           └── create_sample_data.py # Sample data loader
│
├── authentication/                   # Auth app (login, register)
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│
├── admin_dashboard/                  # Admin panel
│   ├── views.py
│   ├── urls.py
│
├── student/                          # Student portal
│   ├── views.py
│   ├── urls.py
│
├── teacher/                          # Teacher portal
│   ├── views.py
│   ├── urls.py
│
├── attendance/                       # Attendance module
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│
├── templates/                        # HTML templates
│   ├── base.html                     # Base template
│   ├── authentication/
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── complete_profile_*.html
│   ├── admin_dashboard/
│   │   ├── dashboard.html
│   │   ├── pending_registrations.html
│   │   ├── all_students.html
│   │   ├── all_teachers.html
│   │   ├── edit_student.html
│   │   ├── edit_teacher.html
│   │   └── ...
│   ├── student/
│   │   ├── dashboard.html
│   │   ├── profile.html
│   │   ├── attendance.html
│   │   ├── fees.html
│   │   ├── lectures.html
│   │   └── update_profile.html
│   ├── teacher/
│   │   ├── dashboard.html
│   │   ├── profile.html
│   │   ├── lectures.html
│   │   ├── salary.html
│   │   ├── mark_attendance.html
│   │   └── update_profile.html
│   └── attendance/
│       └── attendance_list.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## 🔑 Test Accounts (Sample Data)

After running `create_sample_data`:

### Admin Account
```
Username: admin
Password: admin123
Role: Admin
```

### Student Accounts
```
Username: student1 to student6
Password: student123
Role: Student
```

### Teacher Accounts
```
Username: teacher1 to teacher6
Password: teacher123
Role: Teacher
```

## 🛠️ Common Commands

### Create Migrations
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Create Sample Data
```bash
python manage.py create_sample_data
```

### Run Development Server
```bash
python manage.py runserver
```

### Run on Different Port
```bash
python manage.py runserver 8080
```

### Access Django Admin Panel
```
http://127.0.0.1:8000/admin/
```

### Collect Static Files (Production)
```bash
python manage.py collectstatic
```

### Reset Database (Warning: Deletes all data!)
```bash
# Remove existing database
rm db.sqlite3

# Re-run migrations
python manage.py migrate
```

## 🐛 Troubleshooting

### Issue: "No module named Django"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "ModuleNotFoundError: No module named 'core'"
**Solution:** Ensure you're in the correct directory:
```bash
cd toppers_project
```

### Issue: "ProgrammingError: relation does not exist"
**Solution:** Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Images/CSS not loading
**Solution 1** (Development): Already handled automatically
**Solution 2** (Production): Run collect static
```bash
python manage.py collectstatic --noinput
```

### Issue: "Port 8000 already in use"
**Solution:** Use different port:
```bash
python manage.py runserver 8080
```

### Issue: Static files showing 404 errors
**Solution:**
1. Ensure static folder exists: `toppers/static/`
2. Restart development server
3. Clear browser cache

## 📚 Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- Bootstrap 5: https://getbootstrap.com/
- Font Awesome Icons: https://fontawesome.com/

## ✅ Verification Checklist

After setup, verify the following work:

- [ ] Home page loads at `/`
- [ ] Registration page loads at `/auth/register/`
- [ ] Login page loads at `/login/`
- [ ] Admin panel loads at `/admin/`
- [ ] Can create new user and login
- [ ] Admin dashboard shows statistics
- [ ] Notifications appear in admin panel
- [ ] Student can view attendance
- [ ] Teacher can mark attendance
- [ ] CSS/styling loads correctly
- [ ] Bootstrap appears on all pages

## 🚀 Deployment (Basics)

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Set secure `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Use PostgreSQL instead of SQLite
5. Collect static files
6. Set up proper logging
7. Use environment variables for secrets
8. Deploy on server (Heroku, AWS, DigitalOcean, etc.)

## 📞 Support

For issues or questions:
1. Check the README.md
2. Review Django documentation
3. Check the troubleshooting section above

---

**Happy Learning! 🎓**

For more details, see README.md
