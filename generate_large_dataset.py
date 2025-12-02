"""
Generate 20,000 student health records for Haramaya University Health Center
Clean and organized data generator for testing the health management system
"""
import csv
import random
import os
from datetime import datetime, timedelta


# ============================================================================
# CONFIGURATION
# ============================================================================
NUM_RECORDS = 20000
OUTPUT_FILE = 'data/complete_health_records.csv'
START_DATE = datetime(2024, 1, 1)
DATE_RANGE_DAYS = 365


# ============================================================================
# DATA POOLS - Ethiopian Names and University Data
# ============================================================================
class DataPool:
    """Centralized data pool for generating realistic records"""
    
    FIRST_NAMES_MALE = [
        'Mohammed', 'Abdi', 'Dawit', 'Yonas', 'Biniam', 'Tesfaye', 'Kebede', 
        'Mulugeta', 'Bekele', 'Tadesse', 'Ahmed', 'Ali', 'Hassan', 'Ibrahim', 
        'Mustafa', 'Omar', 'Solomon', 'Daniel', 'Samuel', 'Michael', 'Elias', 
        'Abraham', 'Isaac', 'Jacob'
    ]
    
    FIRST_NAMES_FEMALE = [
        'Hana', 'Fatuma', 'Sara', 'Meron', 'Rahel', 'Tigist', 'Hawi', 'Bekelech',
        'Chaltu', 'Lensa', 'Aisha', 'Amina', 'Zainab', 'Mariam', 'Khadija',
        'Ruth', 'Esther', 'Rebecca', 'Leah', 'Bethlehem', 'Selam', 'Senait'
    ]
    
    LAST_NAMES = [
        'Ahmed', 'Ali', 'Hassan', 'Kebede', 'Tesfaye', 'Mulugeta', 'Tadesse', 
        'Bekele', 'Haile', 'Solomon', 'Abera', 'Negash', 'Fikadu', 'Daba', 
        'Gurmessa', 'Gemechu', 'Lemma', 'Desta', 'Girma', 'Wolde', 'Gebre', 
        'Mengistu', 'Assefa', 'Alemu'
    ]
    
    COLLEGES = ['CNCS', 'CVM', 'CAES', 'CHE', 'CBE', 'CALS']
    
    DEPARTMENTS = {
        'CNCS': ['ICT', 'Computer Science', 'Software Engineering', 'Information Systems', 'Data Science'],
        'CVM': ['Vet Science', 'Animal Science', 'Veterinary Medicine', 'Animal Health'],
        'CAES': ['Agronomy', 'Horticulture', 'Plant Science', 'Soil Science', 'Agricultural Economics'],
        'CHE': ['Public Health', 'Nursing', 'Environmental Health', 'Health Education'],
        'CBE': ['Economics', 'Accounting', 'Management', 'Marketing', 'Finance'],
        'CALS': ['Law', 'Legal Studies', 'Criminology']
    }
    
    DOCTORS = ['Dr. Lensa', 'Dr. Roba', 'Dr. Gemechu', 'Dr. Abera', 'Dr. Tadesse', 'Dr. Bekele']
    
    TECHNICIANS = ['Merga', 'Chaltu', 'Tigist', 'Hawi', 'Bekelech', 'Ahmed']
    
    APPOINTMENT_REASONS = [
        'Headache', 'Abdominal pain', 'Fever', 'Cough', 'Eye infection', 'Skin rash',
        'Dental pain', 'Back pain', 'Allergies', 'Flu symptoms', 'Chest pain',
        'Dizziness', 'Nausea', 'Fatigue', 'Joint pain', 'Sore throat'
    ]
    
    SYMPTOMS = [
        'Fever and cough', 'Stomach cramps and nausea', 'Red and itchy eyes',
        'Lower back pain', 'High fever and body aches', 'Skin rash and itching',
        'Severe headache', 'Chest pain and shortness of breath', 'Persistent cough',
        'Abdominal pain and diarrhea', 'Joint pain and swelling', 'Sore throat and fever'
    ]
    
    DIAGNOSES = [
        'Flu', 'Gastritis', 'Conjunctivitis', 'Muscle strain', 'Malaria', 
        'Allergic dermatitis', 'Migraine', 'Bronchitis', 'Food poisoning', 
        'Arthritis', 'Tonsillitis', 'Common cold', 'Hypertension', 'Diabetes', 
        'Anemia', 'Typhoid', 'UTI'
    ]
    
    TEST_TYPES = ['Malaria', 'Urine Test', 'Blood Test', 'TB Test', 'CBC', 'Stool Test', 'HIV Test']
    
    TEST_RESULTS = ['Negative', 'Positive', 'Normal', 'Abnormal', 'Low hemoglobin', 'High WBC']
    
    SERVICES = [
        'CBC Test', 'Urine Analysis', 'Malaria Test', 'Blood Test', 'Eye Examination',
        'Consultation Fee', 'TB Test', 'X-Ray', 'Ultrasound', 'ECG', 'Stool Test'
    ]
    
    SERVICE_AMOUNTS = [5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 75, 100]
    
    STATUSES = ['Pending', 'Approved', 'Completed', 'Cancelled']
    
    BILL_STATUSES = ['Paid', 'Pending']


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
class Generator:
    """Helper functions for generating realistic data"""
    
    @staticmethod
    def phone_number():
        """Generate Ethiopian phone number (09XXXXXXXX)"""
        return f"09{random.randint(10000000, 99999999)}"
    
    @staticmethod
    def student_id(index, year):
        """Generate student ID (HU-UGR-YEAR-#####)"""
        return f"HU-UGR-{year}-{10000 + index:05d}"
    
    @staticmethod
    def date(base_date, days_range):
        """Generate random date within range"""
        random_days = random.randint(0, days_range)
        return (base_date + timedelta(days=random_days)).strftime('%Y-%m-%d')
    
    @staticmethod
    def time():
        """Generate appointment time (8:00 AM - 4:30 PM)"""
        hour = random.randint(8, 16)
        minute = random.choice([0, 30])
        return f"{hour:02d}:{minute:02d}"
    
    @staticmethod
    def full_name(gender):
        """Generate full name based on gender"""
        if gender == 'M':
            first_name = random.choice(DataPool.FIRST_NAMES_MALE)
        else:
            first_name = random.choice(DataPool.FIRST_NAMES_FEMALE)
        last_name = random.choice(DataPool.LAST_NAMES)
        return f"{first_name} {last_name}"


# ============================================================================
# RECORD GENERATOR
# ============================================================================
class HealthRecordGenerator:
    """Main class for generating health records"""
    
    def __init__(self, num_records, output_file, start_date):
        self.num_records = num_records
        self.output_file = output_file
        self.start_date = start_date
        self.fieldnames = [
            'student_id', 'full_name', 'college', 'department', 'phone', 'gender', 'year',
            'appointment_id', 'appointment_doctor', 'appointment_date', 'appointment_time',
            'appointment_reason', 'appointment_status',
            'consultation_id', 'symptoms', 'diagnosis', 'consultation_doctor', 'consultation_date',
            'lab_test_id', 'test_type', 'test_result', 'lab_technician', 'lab_date',
            'bill_id', 'service', 'amount', 'bill_status', 'bill_date'
        ]
    
    def generate_student_info(self, index):
        """Generate student information"""
        gender = random.choice(['M', 'F'])
        college = random.choice(DataPool.COLLEGES)
        department = random.choice(DataPool.DEPARTMENTS.get(college, ['General']))
        year = random.randint(1, 5)
        student_year = random.randint(2021, 2024)
        
        return {
            'student_id': Generator.student_id(index, student_year),
            'full_name': Generator.full_name(gender),
            'college': college,
            'department': department,
            'phone': Generator.phone_number(),
            'gender': gender,
            'year': year
        }
    
    def generate_appointment_info(self, index):
        """Generate appointment information"""
        apt_date = Generator.date(self.start_date, DATE_RANGE_DAYS)
        
        return {
            'appointment_id': f"APT-{10000 + index:05d}",
            'appointment_doctor': random.choice(DataPool.DOCTORS),
            'appointment_date': apt_date,
            'appointment_time': Generator.time(),
            'appointment_reason': random.choice(DataPool.APPOINTMENT_REASONS),
            'appointment_status': random.choice(DataPool.STATUSES),
            'date': apt_date
        }
    
    def generate_consultation_info(self, index, has_consultation):
        """Generate consultation information"""
        if not has_consultation:
            return {
                'consultation_id': '',
                'symptoms': '',
                'diagnosis': '',
                'consultation_doctor': '',
                'consultation_date': ''
            }
        
        return {
            'consultation_id': f"CONS-{10000 + index:05d}",
            'symptoms': random.choice(DataPool.SYMPTOMS),
            'diagnosis': random.choice(DataPool.DIAGNOSES),
            'consultation_doctor': random.choice(DataPool.DOCTORS),
            'consultation_date': ''  # Will be set to appointment date
        }
    
    def generate_lab_info(self, index):
        """Generate lab test information"""
        return {
            'lab_test_id': f"LAB-{10000 + index:05d}",
            'test_type': random.choice(DataPool.TEST_TYPES),
            'test_result': random.choice(DataPool.TEST_RESULTS),
            'lab_technician': random.choice(DataPool.TECHNICIANS),
            'lab_date': ''  # Will be set to appointment date
        }
    
    def generate_billing_info(self, index):
        """Generate billing information"""
        return {
            'bill_id': f"BILL-{10000 + index:05d}",
            'service': random.choice(DataPool.SERVICES),
            'amount': random.choice(DataPool.SERVICE_AMOUNTS),
            'bill_status': random.choice(DataPool.BILL_STATUSES),
            'bill_date': ''  # Will be set to appointment date
        }
    
    def generate_record(self, index):
        """Generate a complete health record"""
        # Generate all components
        student = self.generate_student_info(index)
        appointment = self.generate_appointment_info(index)
        has_consultation = random.random() > 0.3  # 70% have consultations
        consultation = self.generate_consultation_info(index, has_consultation)
        lab = self.generate_lab_info(index)
        billing = self.generate_billing_info(index)
        
        # Set dates
        apt_date = appointment['date']
        if has_consultation:
            consultation['consultation_date'] = apt_date
        lab['lab_date'] = apt_date
        billing['bill_date'] = apt_date
        
        # Remove temporary date field
        del appointment['date']
        
        # Combine all data
        record = {**student, **appointment, **consultation, **lab, **billing}
        return record
    
    def ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"📁 Created directory: {output_dir}")
    
    def generate_all_records(self):
        """Generate all records and write to CSV file"""
        self.ensure_output_directory()
        
        print(f"🏥 Generating {self.num_records:,} student health records...")
        print(f"📝 Output file: {self.output_file}\n")
        
        with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            
            for i in range(self.num_records):
                record = self.generate_record(i)
                writer.writerow(record)
                
                # Progress indicator
                if (i + 1) % 1000 == 0:
                    print(f"✓ Generated {i + 1:,} records...")
        
        print(f"\n✅ Successfully generated {self.num_records:,} student health records!")
        print(f"📁 File saved: {self.output_file}")
        print(f"💾 File size: {os.path.getsize(self.output_file) / (1024*1024):.2f} MB")



# ============================================================================
# MAIN EXECUTION
# ============================================================================
def main():
    """Main function to run the generator"""
    generator = HealthRecordGenerator(
        num_records=NUM_RECORDS,
        output_file=OUTPUT_FILE,
        start_date=START_DATE
    )
    generator.generate_all_records()


if __name__ == "__main__":
    main()
