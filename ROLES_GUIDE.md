# TOPPERS - Roles & Permissions Guide

## 👨‍💼 Admin Role

### Access
- **URL**: `/admin-panel/` or login as Admin role

### Responsibilities
- Approve/reject student and teacher registrations
- Manage student records (add, edit, delete)
- Manage teacher records (add, edit, delete)
- Update student fees and balances
- Update teacher salaries
- View attendance records
- Approve/reject profile updates
- Monitor all system activities
- View notifications for all activities

### Permissions
✅ Full system access
✅ Can modify any user data
✅ Can view all records
✅ Can delete users
✅ Can approve/reject applications
✅ Can update financial information

### Dashboard Features
- Statistics overview (students, teachers, pending)
- Pending registrations list
- Student management with search
- Teacher management with search
- Attendance records viewer
- Profile update approval queue
- Notifications with read/unread status
- Quick action buttons

### Key Actions
1. **Approve Registration**: Accept pending student/teacher
2. **Reject Registration**: Decline pending application
3. **Add Student**: Manually create student account
4. **Add Teacher**: Manually create teacher account
5. **Edit Student**: Update student info and fees
6. **Edit Teacher**: Update teacher info and salary
7. **Delete Records**: Remove student/teacher (irreversible)
8. **Approve Profile**: Accept profile update request
9. **View Attendance**: Check attendance by date/student

---

## 🎓 Student Role

### Access
- **URL**: `/student/` (after login with Student role)
- **Registration**: `/auth/register/` → Select "Student"

### Requirements
- Must register
- Must wait for admin approval
- Must complete profile after approval
- Must login again after profile completion

### Permissions
✅ View own profile
✅ View attendance records
✅ View upcoming lectures
✅ View fees information
✅ Update own details (requires approval)

❌ Cannot modify other student data
❌ Cannot view other students' records
❌ Cannot access teacher/admin features

### Dashboard Features
- Statistics (classes, attended, percentage, fees due)
- Quick links to all features
- Upcoming lectures list
- Personal information card

### Available Sections

#### 1. Dashboard (`/student/dashboard/`)
- Overview of academic status
- Attendance statistics
- Upcoming lectures
- Fees summary

#### 2. Profile (`/student/profile/`)
- View personal information
- View academic details
- View guardian information
- Edit profile button

#### 3. Attendance (`/student/attendance/`)
- Attendance percentage
- Present/absent breakdown
- Total classes
- Detailed records table
- Progress bar visualization

#### 4. Fees (`/student/fees/`)
- Total fees amount
- Amount paid
- Amount remaining
- Payment progress bar
- Status indicators

#### 5. Lectures (`/student/lectures/`)
- All scheduled classes
- Class date and time
- Subject and batch
- Teacher name
- Class topic

#### 6. Update Profile (`/student/update-profile/`)
- Edit personal details
- Edit academic information
- Edit guardian details
- Submit for admin approval
- Wait for approval notification

### Registration Process
```
1. Go to /auth/register/
2. Select "Student" role
3. Fill registration form
4. Click Register
5. See "Waiting for approval" message
6. Admin approves (admin checks pending)
7. Get "Approved" notification
8. Login again
9. Complete profile details
10. Profile saved, full access granted
```

### Update Profile Process
```
1. Go to Update Profile
2. Edit desired fields
3. Click "Submit for Approval"
4. Wait for admin approval
5. Get notification when approved
6. Changes appear in profile
```

---

## 👨‍🏫 Teacher Role

### Access
- **URL**: `/teacher/` (after login with Teacher role)
- **Registration**: `/auth/register/` → Select "Teacher"

### Requirements
- Must register
- Must wait for admin approval
- Must complete profile after approval
- Must login again after profile completion

### Permissions
✅ View own profile
✅ View assigned lectures
✅ Mark student attendance
✅ View salary information
✅ Update own details (requires approval)

❌ Cannot modify other teacher data
❌ Cannot view other teachers' records (except attendance context)
❌ Cannot access student/admin features

### Dashboard Features
- Statistics (total lectures, salary, experience)
- Quick links to all features
- Upcoming lectures with attendance button
- Professional information display

### Available Sections

#### 1. Dashboard (`/teacher/dashboard/`)
- Overview of teaching status
- Lecture statistics
- Upcoming lectures
- Salary information
- Quick attendance marking button

#### 2. Profile (`/teacher/profile/`)
- View personal information
- View professional qualifications
- View experience and subjects
- View salary
- Edit profile button

#### 3. Lectures (`/teacher/lectures/`)
- All assigned lectures
- Lecture date and time
- Subject and batch
- Topic information
- Mark attendance button for each lecture

#### 4. Mark Attendance (`/teacher/mark-attendance/<lecture_id>/`)
- List of all students in batch
- Radio buttons for present/absent
- Student enrollment numbers
- Save attendance button
- Confirmation message on save

#### 5. Salary (`/teacher/salary/`)
- Monthly salary amount
- Employee ID
- Name and details
- Experience
- Contact admin for updates

#### 6. Update Profile (`/teacher/update-profile/`)
- Edit personal details
- Edit professional information
- Edit qualifications
- Edit experience
- Submit for admin approval
- Wait for approval notification

### Registration Process
```
1. Go to /auth/register/
2. Select "Teacher" role
3. Fill registration form
4. Click Register
5. See "Waiting for approval" message
6. Admin approves (admin checks pending)
7. Get "Approved" notification
8. Login again
9. Complete profile details
10. Profile saved, full access granted
```

### Mark Attendance Process
```
1. Go to Dashboard or Lectures
2. Find lecture in upcoming list
3. Click "Mark Attendance"
4. Select present/absent for each student
5. Click "Save Attendance"
6. Get confirmation
7. Attendance recorded in system
```

### Update Profile Process
```
1. Go to Update Profile
2. Edit desired fields
3. Click "Submit for Approval"
4. Wait for admin approval
5. Get notification when approved
6. Changes appear in profile
```

---

## 🔐 Authentication Rules

### Registration
- **Students**: Can register anytime
- **Teachers**: Can register anytime
- **Status**: Start as "Pending"

### Login
- **Must provide**:
  - Username
  - Password
  - Role (Admin/Student/Teacher)
- **Requirements**:
  - Account must exist
  - Account must be approved
  - Correct role must be selected
- **Not allowed if**:
  - Status is "Pending" → Shows waiting message
  - Status is "Rejected" → Shows rejection message
  - Role doesn't match → Shows error

### Account Lifecycle
```
Registration (Status: Pending)
    ↓
Admin Review
    ↓
Approved (Can login, must complete profile)
    ↓
Profile Completion
    ↓
Full Access Granted
    ↓
Can request profile updates (require re-approval)
```

---

## 📊 Data Access Rules

### Students Can See
✅ Only their own records
✅ Their attendance only
✅ Their fees only
✅ Lectures scheduled for their batch

### Teachers Can See
✅ Only their own records
✅ Lectures they teach
✅ Students in their batch (when marking attendance)
✅ Their own salary

### Admins Can See
✅ All students
✅ All teachers
✅ All attendance records
✅ All fees and salary information
✅ All registrations
✅ All notifications

---

## 🎯 Common Tasks by Role

### For Students
1. **Check attendance** → Go to Attendance
2. **View fees status** → Go to Fees
3. **See upcoming classes** → Go to Lectures
4. **Update contact info** → Go to Update Profile
5. **Track progress** → View Dashboard

### For Teachers
1. **Mark attendance** → Go to Dashboard → Click Mark Attendance
2. **Check schedule** → Go to Lectures
3. **View salary** → Go to Salary
4. **Update qualifications** → Go to Update Profile
5. **See statistics** → View Dashboard

### For Admins
1. **Approve registrations** → Dashboard → Pending Approvals
2. **Manage students** → All Students → Edit/Add/Delete
3. **Manage teachers** → All Teachers → Edit/Add/Delete
4. **Update fees** → Edit Student → Update Fees Field
5. **Update salary** → Edit Teacher → Update Salary Field
6. **Review notifications** → Dashboard → Check Recent Notifications

---

## ⚠️ Important Notes

1. **Profile Completion**
   - Required after account approval
   - Cannot access system fully until completed
   - Information helps teachers identify students

2. **Attendance**
   - Only teachers can mark attendance
   - Only for their assigned lectures
   - Teachers can see their student lists

3. **Fees & Salary**
   - Only admin can update
   - Students can only view their fees
   - Teachers can only view their salary

4. **Profile Updates**
   - Any update from student/teacher needs admin approval
   - Admin will see notification
   - Changes take effect only after approval

5. **Status Indicators**
   - Pending: Waiting for admin approval
   - Approved: Can access system (but may need profile completion)
   - Rejected: Account cannot be used

---

## 🔑 Test Accounts (Sample Data)

| Role | Username | Password | Status |
|------|----------|----------|---------|
| Admin | admin | admin123 | Approved |
| Student | student1-6 | student123 | Approved |
| Teacher | teacher1-6 | teacher123 | Approved |

---

For detailed features, see FEATURES.md
For setup instructions, see SETUP_GUIDE.md
For project information, see README.md
