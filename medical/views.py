from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Consultation, Prescription
from .forms import ConsultationForm, PrescriptionForm
from appointments.models import Appointment

@login_required
def create_consultation(request, appointment_id):
    """Doctor creates consultation for an appointment"""
    if not request.user.role == 'doctor':
        messages.error(request, 'Only doctors can create consultations.')
        return redirect('dashboard')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)
    
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.appointment = appointment
            consultation.student = appointment.student
            consultation.doctor = request.user
            consultation.save()
            
            appointment.status = 'Completed'
            appointment.save()
            
            messages.success(request, 'Consultation recorded successfully!')
            return redirect('manage_appointments')
    else:
        form = ConsultationForm()
    
    return render(request, 'medical/create_consultation.html', {
        'form': form,
        'appointment': appointment
    })

@login_required
def my_medical_records(request):
    """Student views their medical records"""
    if not request.user.is_student():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    consultations = Consultation.objects.filter(
        student=request.user.student_profile
    ).order_by('-date')
    
    return render(request, 'medical/my_records.html', {
        'consultations': consultations
    })

@login_required
def consultation_detail(request, consultation_id):
    """View consultation details"""
    consultation = get_object_or_404(Consultation, id=consultation_id)
    
    # Check permissions
    if request.user.is_student():
        if consultation.student.user != request.user:
            messages.error(request, 'Access denied.')
            return redirect('dashboard')
    elif not request.user.is_staff_member():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    return render(request, 'medical/consultation_detail.html', {
        'consultation': consultation
    })
