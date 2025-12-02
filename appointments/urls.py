from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('manage/', views.manage_appointments, name='manage_appointments'),
    path('update/<int:appointment_id>/', views.update_appointment_status, name='update_appointment_status'),
]
