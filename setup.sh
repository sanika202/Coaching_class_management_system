#!/bin/bash
# TOPPERS - Coaching Class Management System Setup Script

echo ""
echo "========================================"
echo "  TOPPERS - Coaching Class Management"
echo "========================================"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Setting up database..."
python manage.py makemigrations
python manage.py migrate

echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Create admin user: python manage.py createsuperuser"
echo "2. Run server: python manage.py runserver"
echo "3. Visit: http://127.0.0.1:8000/"
echo ""
echo "Happy coding!"
echo ""
