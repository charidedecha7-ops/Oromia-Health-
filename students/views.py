from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentRegistrationForm

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student registration successful! You can now login.')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'students/register.html', {'form': form})
