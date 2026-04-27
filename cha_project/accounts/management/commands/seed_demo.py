from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User
from patients.models import PatientProfile, HealthRecord
from doctors.models import DoctorProfile, MedicalReport, MedicalOrder
from departments.models import Department
import random, datetime

class Command(BaseCommand):
    help = 'Seed database with demo data for CHA'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding CHA demo data...')

        admin, _ = User.objects.get_or_create(username='admin', defaults={
            'first_name':'System','last_name':'Admin','email':'admin@cha.gov',
            'role':'administrator','is_approved':True,'is_active':True,'is_superuser':True,'is_staff':True
        })
        admin.set_password('admin123'); admin.save()

        depts = []
        for name, code in [('Radiology','RAD'),('Cardiology','CARD'),('Neurology','NEURO'),('Pathology','PATH')]:
            d, _ = Department.objects.get_or_create(code=code, defaults={'name':name,'is_active':True})
            depts.append(d)

        doctors = []
        for fn, ln, spec in [('Aayla','Secura','Cardiology'),('Qui-Gon','Jinn','Neurology'),('Luminara','Unduli','Radiology')]:
            u, created = User.objects.get_or_create(username=f'dr_{fn.lower()}', defaults={
                'first_name':fn,'last_name':ln,'email':f'{fn.lower()}@cha.gov',
                'role':'doctor','is_approved':True,'is_active':True
            })
            if created: u.set_password('demo123'); u.save()
            DoctorProfile.objects.get_or_create(user=u, defaults={'specialty':spec})
            doctors.append(u)

        patients = []
        for fn, ln, bt in [('Anakin','Skywalker','A+'),('Padme','Amidala','O-'),('Obi-Wan','Kenobi','B+')]:
            u, created = User.objects.get_or_create(username=f'{fn.lower()}_{ln.lower()}', defaults={
                'first_name':fn,'last_name':ln,'email':f'{fn.lower()}@coruscant.gov',
                'role':'patient','is_approved':True,'is_active':True
            })
            if created: u.set_password('demo123'); u.save()
            PatientProfile.objects.get_or_create(user=u, defaults={'blood_type':bt,'assigned_doctor':doctors[0]})
            patients.append(u)

        for p in patients:
            for i in range(10):
                dt = timezone.now() - datetime.timedelta(days=i*2)
                HealthRecord.objects.get_or_create(patient=p, recorded_at=dt, defaults={
                    'heart_rate': random.uniform(62,98), 'temperature': random.uniform(36.2,37.4),
                    'blood_pressure_systolic': random.randint(110,145), 'blood_pressure_diastolic': random.randint(70,95),
                    'oxygen_saturation': random.uniform(95,99.5), 'glucose_level': random.uniform(80,120),
                    'weight': random.uniform(65,90), 'source': 'device',
                })

        for p in patients[:2]:
            MedicalReport.objects.get_or_create(doctor=doctors[0], patient=p, title=f'Review — {p.first_name}', defaults={
                'diagnosis':'Stable vitals. Continue current regimen.','prescription':'Lisinopril 10mg daily.','is_visible_to_patient':True
            })
            MedicalOrder.objects.get_or_create(doctor=doctors[0], patient=p, order_type='ct_scan', defaults={
                'description':'Chest CT scan — routine','priority':'normal','status':'pending','department':depts[0]
            })

        for uname, fn, ln, role in [('emergency_1','Emergency','Services','emergency'),('dept_radiology','Radiology','Dept','department')]:
            u, created = User.objects.get_or_create(username=uname, defaults={
                'first_name':fn,'last_name':ln,'role':role,'is_approved':True,'is_active':True
            })
            if created: u.set_password('demo123'); u.save()

        u, created = User.objects.get_or_create(username='pending_patient', defaults={
            'first_name':'Rex','last_name':'Captain','role':'patient','is_approved':False,'is_active':True
        })
        if created: u.set_password('demo123'); u.save()

        self.stdout.write(self.style.SUCCESS(f'''
✅ Demo data seeded!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 admin / admin123          (Administrator)
👨‍⚕️ dr_aayla / demo123        (Doctor)
🏥 anakin_skywalker / demo123 (Patient)
🚨 emergency_1 / demo123     (Emergency)
🏢 dept_radiology / demo123  (Department)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        '''))
