from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('complete-profile-student/', views.complete_profile_student, name='complete_profile_student'),
    path('complete-profile-teacher/', views.complete_profile_teacher, name='complete_profile_teacher'),
]
