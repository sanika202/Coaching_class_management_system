from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from core.models import CustomUser, StudentProfile, TeacherProfile, Lecture, Subject, Batch
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=20, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'phone', 'date_of_birth', 'password1', 'password2')
        widgets = {
            'role': forms.RadioSelect(choices=[('student', 'Student'), ('teacher', 'Teacher')]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Password must be at least 8 characters'
        self.fields['password2'].help_text = 'Enter same password'
      # --- Date of Birth Validation ---
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        role = self.cleaned_data.get('role')  # Get selected role
        if dob and role:
            today = date.today()
            if dob > today:
                raise ValidationError("Date of birth cannot be in the future.")

            # Calculate age
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            # Role-based validation
            if role == 'teacher' and age < 21:
                raise ValidationError("Teacher must be at least 21 years old.")
            elif role == 'student' and age < 15:
                raise forms.ValidationError("Student must be at least 15 years old.")

        return dob


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'date_of_birth', 'address', 'profile_image')


class LoginForm(AuthenticationForm):
    role = forms.ChoiceField(choices=[('admin', 'Admin'), ('student', 'Student'), ('teacher', 'Teacher')])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['role'].widget.attrs.update({'class': 'form-control'})


class StudentProfileForm(forms.ModelForm):
    batch = forms.ModelChoiceField(queryset=Batch.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),required=True)
    class Meta:
        model = StudentProfile
        fields = ['enrollment_number', 'guardian_name', 'guardian_phone', 'batch', 'subjects']
   
class TeacherProfileForm(forms.ModelForm):
    subjects_taught = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True
    )
    class Meta:
        model = TeacherProfile
        fields = ['employee_id', 'qualifications', 'subjects_taught', 'experience']
        widgets = {
            'qualifications': forms.Textarea(attrs={'rows': 3}),
        }
    class TeacherForm(forms.ModelForm):
        def clean_date_of_birth(self):
           dob = self.cleaned_data.get("date_of_birth")
           today = date.today()
           age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
           if age < 23:
              raise forms.ValidationError("Teacher must be at least 23 years old.")
           return dob

#for timetable app,

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['teacher', 'subject', 'batch', 'day', 'start_time', 'end_time', 'class_date']
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'batch': forms.Select(attrs={'class': 'form-control'}),
            'day': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'class_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

#for adding subjects and batches in the timetable app,
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject name'})
        }
    def clean_name(self):
        name = self.cleaned_data['name'].strip()

        if Subject.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("This subject already exists.")

        return name


class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter batch name'})
        }
    def clean_name(self):
        name = self.cleaned_data['name'].strip()

        if Batch.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("This batch already exists.")

        return name


