from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('profile/', views.student_profile, name='student_profile'),
    path('attendance/', views.student_attendance, name='student_attendance'),
    path('fees/', views.student_fees, name='student_fees'),
    path('lectures/', views.student_lectures, name='student_lectures'),
    path('update-profile/', views.update_student_profile, name='update_student_profile'),
]
