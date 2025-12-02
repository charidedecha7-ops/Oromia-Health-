from django import forms
from django.contrib.auth import get_user_model
from .models import StudentProfile

User = get_user_model()

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    # Student Profile Fields
    student_id = forms.CharField(max_length=20)
    college = forms.CharField(max_length=100)
    department = forms.CharField(max_length=100)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    year = forms.IntegerField()
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.role = 'student'
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                student_id=self.cleaned_data['student_id'],
                college=self.cleaned_data['college'],
                department=self.cleaned_data['department'],
                gender=self.cleaned_data['gender'],
                year=self.cleaned_data['year'],
                date_of_birth=self.cleaned_data['date_of_birth']
            )
        return user
