from django import forms
from .models import Consultation, Prescription

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['symptoms', 'diagnosis', 'notes']
        widgets = {
            'symptoms': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'diagnosis': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['drug_name', 'dosage', 'instructions']
        widgets = {
            'drug_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
