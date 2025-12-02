"""
Django management command to import CSV data into the database
Usage: python manage.py import_csv
"""
import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from students.models import StudentProfile
from appointments.models import Appointment
from medical.models import Consultation
from lab.models import LabTest
from billing.models import Bill
from datetime import datetime

User = get_user_model()


class Command(BaseCommand):
    help = 'Import health records from CSV file'

    def handle(self, *args, **kwargs):
        csv_file = 'data/complete_health_records.csv'
        
        self.stdout.write("Starting CSV import...")
        
        # Track created objects
        students_created = 0
        appointments_created = 0
        consultations_created = 0
        lab_tests_created = 0
        bills_created = 0
        
        # Cache for users and students
        user_cache = {}
        student_cache = {}
        doctor_cache = {}
        tech_cache = {}
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for i, row in enumerate(reader, 1):
                try:
                    # Get or create student user
                    student_id = row['student_id']
                    
                    if student_id not in student_cache:
                        # Create user for student
                        username = student_id.lower().replace('-', '_')
                        full_name = row['full_name']
                        name_parts = full_name.split(' ', 1)
                        first_name = name_parts[0]
                        last_name = name_parts[1] if len(name_parts) > 1 else ''
                        
                        user, created = User.objects.get_or_create(
                            username=username,
                            defaults={
                                'first_name': first_name,
                                'last_name': last_name,
                                'role': 'student'
                            }
                        )
                        
                        # Create student profile
                        student, created = StudentProfile.objects.get_or_create(
                            student_id=student_id,
                            defaults={
                                'user': user,
                                'college': row['college'],
                                'department': row['department'],
                                'gender': row['gender'],
                                'year': int(row['year'])
                            }
                        )
                        
                        student_cache[student_id] = student
                        if created:
                            students_created += 1
                    else:
                        student = student_cache[student_id]
                    
                    # Get or create doctor
                    doctor_name = row['appointment_doctor']
                    if doctor_name not in doctor_cache:
                        doctor_username = doctor_name.lower().replace(' ', '_').replace('.', '')
                        doctor, _ = User.objects.get_or_create(
                            username=doctor_username,
                            defaults={
                                'first_name': doctor_name,
                                'role': 'doctor'
                            }
                        )
                        doctor_cache[doctor_name] = doctor
                    else:
                        doctor = doctor_cache[doctor_name]
                    
                    # Create appointment
                    appointment = Appointment.objects.create(
                        student=student,
                        doctor=doctor,
                        date=datetime.strptime(row['appointment_date'], '%Y-%m-%d').date(),
                        time=datetime.strptime(row['appointment_time'], '%H:%M').time(),
                        reason=row['appointment_reason'],
                        status=row['appointment_status']
                    )
                    appointments_created += 1
                    
                    # Create consultation if exists
                    if row['consultation_id']:
                        consultation_doctor_name = row['consultation_doctor']
                        if consultation_doctor_name not in doctor_cache:
                            cons_doc_username = consultation_doctor_name.lower().replace(' ', '_').replace('.', '')
                            cons_doctor, _ = User.objects.get_or_create(
                                username=cons_doc_username,
                                defaults={
                                    'first_name': consultation_doctor_name,
                                    'role': 'doctor'
                                }
                            )
                            doctor_cache[consultation_doctor_name] = cons_doctor
                        else:
                            cons_doctor = doctor_cache[consultation_doctor_name]
                        
                        Consultation.objects.create(
                            appointment=appointment,
                            student=student,
                            doctor=cons_doctor,
                            symptoms=row['symptoms'],
                            diagnosis=row['diagnosis']
                        )
                        consultations_created += 1
                    
                    # Get or create lab technician
                    tech_name = row['lab_technician']
                    if tech_name not in tech_cache:
                        tech_username = tech_name.lower().replace(' ', '_')
                        tech, _ = User.objects.get_or_create(
                            username=tech_username,
                            defaults={
                                'first_name': tech_name,
                                'role': 'lab_tech'
                            }
                        )
                        tech_cache[tech_name] = tech
                    else:
                        tech = tech_cache[tech_name]
                    
                    # Create lab test
                    test_type_map = {
                        'Malaria': 'Malaria',
                        'Urine Test': 'Urine',
                        'Blood Test': 'Blood',
                        'TB Test': 'TB',
                        'CBC': 'CBC'
                    }
                    test_type = test_type_map.get(row['test_type'], 'Other')
                    
                    LabTest.objects.create(
                        student=student,
                        test_type=test_type,
                        result=row['test_result'],
                        technician=tech,
                        is_completed=True
                    )
                    lab_tests_created += 1
                    
                    # Create bill
                    Bill.objects.create(
                        student=student,
                        service=row['service'],
                        amount=float(row['amount']),
                        status=row['bill_status']
                    )
                    bills_created += 1
                    
                    # Progress
                    if i % 1000 == 0:
                        self.stdout.write(f"Processed {i:,} records...")
                
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error at row {i}: {str(e)}"))
                    continue
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ Import completed!"))
        self.stdout.write(f"Students created: {students_created:,}")
        self.stdout.write(f"Appointments created: {appointments_created:,}")
        self.stdout.write(f"Consultations created: {consultations_created:,}")
        self.stdout.write(f"Lab tests created: {lab_tests_created:,}")
        self.stdout.write(f"Bills created: {bills_created:,}")
