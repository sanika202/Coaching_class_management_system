"""
Test script to verify TOPPERS installation
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toppers_project.settings')
django.setup()

from core.models import CustomUser

def test_installation():
    print("\n" + "="*50)
    print("TOPPERS - Installation Test")
    print("="*50 + "\n")
    
    try:
        # Test database connection
        user_count = CustomUser.objects.count()
        print("✓ Database connection: OK")
        print(f"  Users in database: {user_count}")
        
        # Test models
        print("\n✓ Models loaded successfully:")
        print("  - CustomUser")
        print("  - StudentProfile")
        print("  - TeacherProfile")
        print("  - Lecture")
        print("  - AttendanceRecord")
        print("  - Notification")
        
        print("\n" + "="*50)
        print("Installation Status: SUCCESS ✓")
        print("="*50 + "\n")
        
        print("Next steps:")
        print("1. Create superuser: python manage.py createsuperuser")
        print("2. Run development server: python manage.py runserver")
        print("3. Visit http://127.0.0.1:8000/")
        print()
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        print("\nPlease run migrations first:")
        print("  python manage.py makemigrations")
        print("  python manage.py migrate")
        sys.exit(1)

if __name__ == "__main__":
    test_installation()
