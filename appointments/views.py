from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentBookingForm
from students.models import StudentProfile

@login_required
def book_appointment(request):
    """Student books an appointment"""
    if not request.user.is_student():
        messages.error(request, 'Only students can book appointments.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.student = request.user.student_profile
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('my_appointments')
    else:
        form = AppointmentBookingForm()
    
    return render(request, 'appointments/book.html', {'form': form})

@login_required
def my_appointments(request):
    """View student's appointments"""
    if not request.user.is_student():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    appointments = Appointment.objects.filter(
        student=request.user.student_profile
    ).order_by('-date', '-time')
    
    return render(request, 'appointments/my_appointments.html', {
        'appointments': appointments
    })

@login_required
def manage_appointments(request):
    """Doctor/Receptionist manages appointments"""
    if not request.user.is_staff_member():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.user.role == 'doctor':
        appointments = Appointment.objects.filter(doctor=request.user)
    else:
        appointments = Appointment.objects.all()
    
    appointments = appointments.order_by('-date', '-time')
    
    return render(request, 'appointments/manage.html', {
        'appointments': appointments
    })

@login_required
def update_appointment_status(request, appointment_id):
    """Update appointment status"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['Approved', 'Completed', 'Cancelled']:
            appointment.status = status
            appointment.save()
            messages.success(request, f'Appointment {status.lower()} successfully!')
    
    return redirect('manage_appointments')
