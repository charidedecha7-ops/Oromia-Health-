from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    user = request.user
    if user.role == 'student':
        return render(request, 'core/student_dashboard.html')
    elif user.role == 'doctor':
        return render(request, 'core/doctor_dashboard.html')
    elif user.role == 'lab_tech':
        return render(request, 'core/lab_dashboard.html')
    elif user.role == 'pharmacist':
        return render(request, 'core/pharmacy_dashboard.html')
    elif user.role == 'receptionist':
        return render(request, 'core/receptionist_dashboard.html')
    elif user.role == 'admin':
        return redirect('/admin/') # Or a custom admin dashboard
    else:
        return render(request, 'core/dashboard.html') # Fallback
