from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('profile/', views.teacher_profile, name='teacher_profile'),
    path('lectures/', views.teacher_lectures, name='teacher_lectures'),
    path('mark-attendance/<int:lecture_id>/', views.mark_attendance, name='mark_attendance'),
    path('update-profile/', views.update_teacher_profile, name='update_teacher_profile'),
    path('salary/', views.teacher_salary, name='teacher_salary'),
]
