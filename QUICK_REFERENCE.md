# TOPPERS - Quick Reference Card

## 🚀 Quick Start (60 seconds)

```bash
# 1. Navigate to project
cd c:\sanika\python_project_sem2\toppers

# 2. Run setup
setup.bat                    # Windows
# bash setup.sh             # Mac/Linux

# 3. Create admin
python manage.py createsuperuser

# 4. Start server
python manage.py runserver

# 5. Visit and login
# http://127.0.0.1:8000/
```

---

## 📌 Essential URLs

| URL | Purpose | Access |
|-----|---------|--------|
| `/` | Home redirect | Public |
| `/auth/login/` | Login page | Public |
| `/auth/register/` | Register (student/teacher) | Public |
| `/admin/` | Django admin | Admin only |
| `/admin-dashboard/` | Admin panel | Admin only |
| `/student/dashboard/` | Student home | Student only |
| `/teacher/dashboard/` | Teacher home | Teacher only |

---

## 👤 Test Accounts (After Sample Data)

```
Admin:
  - Username: admin
  - Password: admin (set during setup)

Test Student:
  - Username: student1
  - Password: student123

Test Teacher:
  - Username: teacher1
  - Password: teacher123
```

---

## 🔑 Default Roles

| Role | Can Do |
|------|--------|
| **Admin** | Approve/manage users, view all data, manage fees/salary |
| **Student** | View own dashboard, fees, attendance, lectures |
| **Teacher** | View own dashboard, mark attendance, view lectures |

---

## 📋 Key Features by Role

### Student Can:
- ✅ Register with guardian info
- ✅ View dashboard with stats
- ✅ Track attendance & percentage
- ✅ View fees due
- ✅ See upcoming lectures
- ✅ Update own profile (pending approval)

### Teacher Can:
- ✅ Complete profile after approval
- ✅ View assigned lectures
- ✅ Mark student attendance
- ✅ View salary info
- ✅ Update own profile (pending approval)

### Admin Can:
- ✅ Approve/reject registrations
- ✅ Add/edit/delete students & teachers
- ✅ Update fees & salary
- ✅ View all attendance
- ✅ Approve profile updates
- ✅ Manage notifications
- ✅ Search all records

---

## 🗄️ Database Models (6)

```
CustomUser
  ├─ StudentProfile (if role='student')
  ├─ TeacherProfile (if role='teacher')
  ├─ Lecture (if teacher)
  ├─ AttendanceRecord (if student)
  └─ Notification (activity log)
```

---

## 🎯 Workflows

### Student Registration Flow
```
1. Register at /auth/register/ (role=student)
2. Wait for admin approval
3. Admin approves at /admin-dashboard/pending-registrations/
4. Student logs in
5. Complete profile at /auth/complete-profile/student/
6. Access /student/dashboard/
```

### Mark Attendance
```
1. Teacher: /teacher/dashboard/
2. Click "Mark Attendance" on lecture
3. Select present/absent for students
4. Submit
5. Students see in /student/attendance/
```

### Update Fees
```
1. Admin: /admin-dashboard/all-students/
2. Click Edit on student
3. Update "Fees Paid"
4. Save
5. Student sees updated at /student/fees/
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `manage.py` | Django management |
| `requirements.txt` | Python packages |
| `toppers_project/settings.py` | Django config |
| `core/models.py` | Database models |
| `core/forms.py` | User forms |
| `templates/base.html` | Main layout |
| `static/css/style.css` | Custom styling |

---

## 🔧 Common Commands

```bash
# Run server
python manage.py runserver

# Create admin user
python manage.py createsuperuser

# Load sample data
python manage.py create_sample_data

# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Django shell
python manage.py shell

# Check config
python manage.py check
```

---

## 🆘 Quick Fixes

| Problem | Fix |
|---------|-----|
| No module django | `pip install -r requirements.txt` |
| No tables | `python manage.py migrate` |
| Port 8000 in use | `python manage.py runserver 8001` |
| Login fails | Check status='approved' |
| No static files | `python manage.py collectstatic --noinput` |

---

## 📚 Documentation Map

| File | Purpose |
|------|---------|
| README.md | Start here |
| SETUP_GUIDE.md | Installation help |
| FEATURES.md | What you can do |
| DATABASE_SCHEMA.md | How data is stored |
| API_REFERENCE.md | All URLs & forms |
| TROUBLESHOOTING.md | Problem solutions |
| PROJECT_SUMMARY.md | Complete overview |
| FILE_LISTING.md | All project files |
| **This file** | Quick reference |

---

## 💾 Backup Database

```bash
# Make backup
copy db.sqlite3 db.sqlite3.backup

# Restore from backup
copy db.sqlite3.backup db.sqlite3
```

---

## 🔐 User Status Workflow

```
Pending → (Admin approves) → Approved → Can login & use system
   ↓
(Admin rejects) → Rejected → Cannot login
```

---

## 📊 Dashboard Stats Shown

### Admin Dashboard
- Total Students
- Total Teachers
- Pending Approvals
- Recent Notifications

### Student Dashboard
- Total Classes
- Classes Attended
- Attendance %
- Fees Info

### Teacher Dashboard
- Total Lectures
- Monthly Salary
- Years Experience

---

## 🎨 Key Features

✨ **Beautiful Design**
- Bootstrap 5 responsive layout
- Professional color scheme
- Font Awesome icons
- Mobile-friendly

🔒 **Secure**
- Django authentication
- CSRF protection
- Role-based access control
- Password hashing

📊 **Complete**
- 6 database models
- 40+ views
- 35+ templates
- All business logic

📱 **Responsive**
- Works on mobile
- Works on tablet
- Works on desktop
- Optimized experience

---

## ⏰ Time Reference

- Setup: ~5 minutes
- First login: ~2 minutes
- Approve user: ~1 minute
- Mark attendance: ~2 minutes
- View dashboard: Instant

---

## 🎯 Next Steps

1. **Setup** → Run `setup.bat` in project folder
2. **Admin** → Create superuser account
3. **Data** → Load sample data (optional)
4. **Test** → Register as student, login, approve, track
5. **Customize** → Edit templates with your colors/logo

---

## 📞 Support

All documentation is included in the project. Start with:
1. README.md (overview)
2. SETUP_GUIDE.md (how to get running)
3. FEATURES.md (what to do)
4. TROUBLESHOOTING.md (if something breaks)

---

## 🏪 What's Included

- ✅ Complete Django backend
- ✅ Beautiful responsive frontend
- ✅ Database with all models
- ✅ Admin control panel
- ✅ Student portal
- ✅ Teacher portal
- ✅ Attendance system
- ✅ Fees tracking
- ✅ Salary tracking
- ✅ Notifications
- ✅ Complete docs
- ✅ Setup scripts
- ✅ Sample data

---

**Version:** 1.0  
**Status:** ✅ Production Ready  
**Created:** 2024  

**Ready to launch! Start with setup.bat and enjoy your coaching management system.** 🚀

---

## 🌟 Pro Tips

1. **Change Dashboard Title**: Edit `templates/base.html` - replace "TOPPERS"
2. **Customize Colors**: Edit `static/css/style.css` - change CSS variables
3. **Add Logo**: Place image in `static/` and reference in `base.html`
4. **More Students**: Use admin panel to add them quickly
5. **Backup Often**: Copy `db.sqlite3` file regularly
6. **Test Thoroughly**: Use sample data before going live

---

**Everything you need is here. Enjoy!** 😊
