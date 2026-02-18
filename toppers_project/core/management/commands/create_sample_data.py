"""
Create sample data for TOPPERS
Usage: python manage.py create_sample_data
"""
from django.core.management.base import BaseCommand
from core.models import CustomUser, StudentProfile, TeacherProfile, Lecture, Notification
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Create sample data for TOPPERS'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        # Create admin if not exists
        if not CustomUser.objects.filter(role='admin').exists():
            admin = CustomUser.objects.create_user(
                username='admin',
                email='admin@toppers.com',
                first_name='Admin',
                last_name='User',
                password='admin123',
                role='admin',
                status='approved'
            )
            self.stdout.write(f'✓ Admin created: {admin.username}')
        
        # Create sample students
        batches = ['XI-Science', 'XII-Science', 'XI-Commerce', 'XII-Commerce']
        subjects_map = {
            'XI-Science': 'Physics, Chemistry, Biology, Mathematics',
            'XII-Science': 'Physics, Chemistry, Biology, Mathematics',
            'XI-Commerce': 'Economics, Accounts, Business Studies',
            'XII-Commerce': 'Economics, Accounts, Business Studies',
        }
        
        for i in range(6):
            username = f'student{i+1}'
            batch = batches[i % len(batches)]
            
            if not CustomUser.objects.filter(username=username).exists():
                student_user = CustomUser.objects.create_user(
                    username=username,
                    email=f'student{i+1}@toppers.com',
                    first_name=f'Student{i+1}',
                    last_name='User',
                    password='student123',
                    phone=f'9000{i:05d}',
                    role='student',
                    status='approved'
                )
                
                StudentProfile.objects.create(
                    user=student_user,
                    enrollment_number=f'ENR{i+1:03d}',
                    guardian_name=f'Guardian {i+1}',
                    guardian_phone=f'9100{i:05d}',
                    batch=batch,
                    subjects=subjects_map[batch],
                    total_fees=50000,
                    fees_paid=random.randint(10000, 40000),
                    profile_update_status='approved'
                )
                self.stdout.write(f'✓ Student created: {username}')
        
        # Create sample teachers
        teacher_subjects = [
            'Physics',
            'Chemistry',
            'Biology',
            'Mathematics',
            'Economics',
            'Accounts'
        ]
        
        for i, subject in enumerate(teacher_subjects):
            username = f'teacher{i+1}'
            
            if not CustomUser.objects.filter(username=username).exists():
                teacher_user = CustomUser.objects.create_user(
                    username=username,
                    email=f'teacher{i+1}@toppers.com',
                    first_name=f'Teacher{i+1}',
                    last_name='User',
                    password='teacher123',
                    phone=f'9200{i:05d}',
                    role='teacher',
                    status='approved'
                )
                
                TeacherProfile.objects.create(
                    user=teacher_user,
                    employee_id=f'EMP{i+1:03d}',
                    qualifications='B.Sc, M.Sc, B.Ed',
                    subjects_taught=subject,
                    experience=random.randint(2, 15),
                    salary=50000 + (i * 5000),
                    profile_update_status='approved'
                )
                self.stdout.write(f'✓ Teacher created: {username}')
        
        # Create sample lectures
        admin_user = CustomUser.objects.filter(role='admin').first()
        teachers = CustomUser.objects.filter(role='teacher', status='approved')
        
        if teachers.exists():
            today = datetime.now().date()
            
            for i in range(12):
                date = today + timedelta(days=i)
                teacher = teachers[i % teachers.count()]
                batch = ['XI-Science', 'XII-Science', 'XI-Commerce', 'XII-Commerce'][i % 4]
                subject = [
                    'Physics', 'Chemistry', 'Biology', 'Mathematics',
                    'Economics', 'Accounts', 'Business Studies'
                ][i % 7]
                
                Lecture.objects.create(
                    teacher=teacher,
                    subject=subject,
                    batch=batch,
                    class_date=date,
                    start_time='09:00:00',
                    end_time='10:00:00',
                    topic=f'{subject} Lecture - Part {(i % 3) + 1}'
                )
            
            self.stdout.write(f'✓ {12} lectures created')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Sample data created successfully!'))
        self.stdout.write('\nTest Accounts:')
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  Student: student1 / student123')
        self.stdout.write('  Teacher: teacher1 / teacher123')
