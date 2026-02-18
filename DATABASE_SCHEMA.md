# TOPPERS - Database Schema

## 📊 Core Models

### 1. CustomUser
Extended Django User model with role-based access.

```
Field              Type            Constraints
─────────────────────────────────────────────────
id                 AutoField       Primary Key
username           CharField       Unique, Max 150
email              EmailField      Unique
first_name         CharField       Max 30
last_name          CharField       Max 30
password           CharField       Hashed
phone              CharField       Max 20 (Blank/Null)
date_of_birth      DateField       Blank/Null
profile_image      ImageField      Blank/Null
address            TextField       Blank
role               CharField       Choices: admin, student, teacher
status             CharField       Choices: pending, approved, rejected
created_at         DateTimeField   Auto now_add
updated_at         DateTimeField   Auto now
is_active          BooleanField    Default True
is_staff           BooleanField    Default False
is_superuser       BooleanField    Default False
```

### 2. StudentProfile
Detailed student information and fees tracking.

```
Field                    Type              Constraints
──────────────────────────────────────────────────────
id                       AutoField         Primary Key
user                     OneToOneField     → CustomUser (CASCADE)
enrollment_number        CharField         Unique, Max 50
guardian_name            CharField         Max 100
guardian_phone           CharField         Max 20
batch                    CharField         Max 100
subjects                 CharField         Max 500
total_fees               DecimalField      Max 10, 2 decimals
fees_paid                DecimalField      Max 10, 2 decimals
profile_update_status    CharField         Choices: pending, approved, rejected
created_at               DateTimeField     Auto now_add
updated_at               DateTimeField     Auto now

Methods:
  - fees_remaining: Calculated property
```

### 3. TeacherProfile
Detailed teacher information and salary tracking.

```
Field                    Type              Constraints
──────────────────────────────────────────────────────
id                       AutoField         Primary Key
user                     OneToOneField     → CustomUser (CASCADE)
employee_id              CharField         Unique, Max 50
qualifications           TextField         
subjects_taught          CharField         Max 500
experience               IntegerField      Years of experience
salary                   DecimalField      Max 10, 2 decimals
profile_update_status    CharField         Choices: pending, approved, rejected
created_at               DateTimeField     Auto now_add
updated_at               DateTimeField     Auto now
```

### 4. Lecture
Class schedule and lecture information.

```
Field              Type              Constraints
────────────────────────────────────────────────
id                 AutoField         Primary Key
teacher            ForeignKey        → CustomUser (CASCADE, limit to teacher role)
subject            CharField         Max 100
batch              CharField         Max 100
class_date         DateField         
start_time         TimeField         
end_time           TimeField         
topic              CharField         Max 200
created_at         DateTimeField     Auto now_add
```

### 5. AttendanceRecord
Student attendance tracking for lectures.

```
Field              Type              Constraints
────────────────────────────────────────────────
id                 AutoField         Primary Key
lecture            ForeignKey        → Lecture (CASCADE)
student            ForeignKey        → CustomUser (CASCADE, limit to student role)
date               DateField         Auto now_add
status             CharField         Choices: present, absent
created_at         DateTimeField     Auto now_add

Constraints:
  - Unique together: (lecture, student)
```

### 6. Notification
Activity notifications for admin dashboard.

```
Field              Type              Constraints
────────────────────────────────────────────────
id                 AutoField         Primary Key
user               ForeignKey        → CustomUser (CASCADE)
notification_type  CharField         Choices: registration, profile_update,
                                      login, fees, salary, attendance
title              CharField         Max 200
message            TextField         
related_user       ForeignKey        → CustomUser (SET_NULL, Blank/Null)
is_read            BooleanField      Default False
created_at         DateTimeField     Auto now_add
```

---

## 🔗 Relationships

### User Role Relationships

```
┌─────────────┐
│ CustomUser  │
│   role      │ ← admin, student, teacher
│   status    │ ← pending, approved, rejected
└─────────────┘
      ↓
   ├─ StudentProfile (OneToOne, if role='student')
   ├─ TeacherProfile (OneToOne, if role='teacher')
   ├─ Lecture (as teacher, if role='teacher')
   ├─ AttendanceRecord (as student, if role='student')
   └─ Notification (to receive notifications)
```

### Lecture & Attendance Relationship

```
┌─────────────────────┐
│  Lecture (class)    │
│  teacher_id → ──────┼── CustomUser (teacher)
│  subject, batch     │
│  class_date, time   │
└─────────────────────┘
          ↓
   ┌──────────────────────────┐
   │ AttendanceRecord (many)  │
   │ lecture_id → ──────────┐ │
   │ student_id → ──────────┼─┼── CustomUser (student)
   │ status (present/absent)│ │
   └──────────────────────────┘
```

---

## 📈 Database Relationships Diagram

```
CustomUser
├── StudentProfile (OneToOne)
│   ├── enrollment_number (unique)
│   ├── fees_tracking
│   └── guardian_info
│
├── TeacherProfile (OneToOne)
│   ├── employee_id (unique)
│   ├── qualifications
│   └── salary_info
│
├── Lecture (if teacher) (ForeignKey)
│   ├── subject
│   ├── batch
│   ├── class_date
│   └── time_info
│       └── AttendanceRecord (ForeignKey)
│           └── student (ForeignKey back to CustomUser)
│
└── Notification (ForeignKey)
    ├── notification_type
    ├── title
    └── message
```

---

## 🗃️ Data Flows

### Registration & Approval Flow

```
User Registration
    ↓
CustomUser (status='pending')
    ↓
Admin Reviews
    ↓
├─ APPROVE → status='approved'
│   ↓
│ User completes profile
│   ↓
│ StudentProfile/TeacherProfile created
│   ↓
│ User can login
│
└─ REJECT → status='rejected'
    ↓
    User cannot login
```

### Attendance Flow

```
StudentProfile.batch + subjects
    ↓
Lecture (teacher assigns)
    ↓
AttendanceRecord (teacher marks)
    ↓
Student views in dashboard
    ↓
Admin views in attendance report
```

### Fees & Salary Flow

```
Admin sets: StudentProfile.total_fees
Admin updates: StudentProfile.fees_paid
    ↓
Student views: remaining = total - paid
    ↓
Notification → Admin when paid

Admin sets: TeacherProfile.salary
Admin updates when needed
    ↓
Teacher views salary
```

---

## 📋 Sample Data Quantities

With `create_sample_data` command:

```
CustomUsers:      7 total
├── Admin:        1
├── Students:     6
└── Teachers:     6

StudentProfiles:  6
TeacherProfiles:  6
Lectures:         12
AttendanceRecords: 0 (empty, needs teacher to mark)
Notifications:    Variable (auto-generated)
```

---

## 🔍 Key Constraints & Validations

### Status Workflow
- `pending` → `approved` ✅ or `rejected` ✅
- Cannot revert status back

### Role Assignments
- Admin cannot change user role
- Student/Teacher chosen at registration
- Remains fixed throughout

### Attendance Data
- Unique per lecture per student
- Cannot mark twice for same lecture-student
- Status must be 'present' or 'absent'

### Fees/Salary
- Must be non-negative decimal
- Admin-only updates
- Calculated fields for remaining fees

### Profile Completeness
- Students need StudentProfile for full access
- Teachers need TeacherProfile for full access
- Enforced by views/decorators

---

## 📊 Database Optimization

### Indexes
- username (unique)
- email (unique)
- enrollment_number (unique)
- employee_id (unique)
- role (for filtering)
- status (for admin queries)
- class_date (for lecture queries)

### Query Optimization
- Use `select_related()` for ForeignKey
- Use `prefetch_related()` for reverse ForeignKey
- Filter by role in queries when needed
- Use database-level constraints

### Pagination Ready
- Models support pagination
- OrderedQuerySets implemented
- Can be easily filtered and sorted

---

## 🔐 Data Privacy & Security

### User Data
- Password hashed using Django's PBKDF2
- Sensitive data not exposed in templates
- CSRF tokens on all forms
- Session-based authentication

### Role-Based Access
- Views check user role
- Decorators prevent unauthorized access
- Admin approval required for deletion

### Data Validation
- Model-level validation
- Form-level validation
- Database constraints
- Type checking

---

## 📝 Database Migration Notes

### Initial Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### After Model Changes
```bash
python manage.py makemigrations <app_name>
python manage.py migrate
```

### Rollback (if needed)
```bash
python manage.py migrate <app_name> <migration_number>
```

---

## 📚 Related Files

- Models: `core/models.py`
- Admin Config: `core/admin.py`
- Forms: `core/forms.py`
- Signals: `core/signals.py`

For complete implementation details, refer to the source files.
