from django import forms
from .models import Appointment
from students.models import StudentProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class AppointmentBookingForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = User.objects.filter(role='doctor')
        self.fields['doctor'].label_from_instance = lambda obj: f"Dr. {obj.first_name} {obj.last_name}"
