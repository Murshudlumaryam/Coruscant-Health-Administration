from django.test import TestCase, Client
from django.urls import reverse
from .models import User
from patients.models import PatientProfile, HealthRecord
from doctors.models import DoctorProfile, MedicalReport, MedicalOrder

class UserModelTest(TestCase):
    def test_create_patient(self):
        u = User.objects.create_user('patient1', password='testpass123', role='patient')
        self.assertEqual(u.role, 'patient')
        self.assertFalse(u.is_approved)
        self.assertFalse(u.is_admin)

    def test_create_doctor(self):
        u = User.objects.create_user('doc1', password='testpass123', role='doctor')
        self.assertEqual(u.role, 'doctor')
        self.assertFalse(u.is_approved)

    def test_create_admin(self):
        u = User.objects.create_user('admin1', password='testpass123', role='administrator')
        self.assertTrue(u.is_admin)

    def test_needs_approval(self):
        patient = User.objects.create_user('p2', password='x', role='patient', is_approved=False)
        self.assertTrue(patient.needs_approval)
        patient.is_approved = True
        patient.save()
        self.assertFalse(patient.needs_approval)

class AuthViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user('admin', password='adminpass', role='administrator', is_approved=True, is_active=True, is_superuser=True, is_staff=True)

    def test_login_page_loads(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)

    def test_register_page_loads(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)

    def test_login_valid(self):
        resp = self.client.post(reverse('login'), {'username': 'admin', 'password': 'adminpass'})
        self.assertRedirects(resp, reverse('dashboard'))

    def test_login_invalid(self):
        resp = self.client.post(reverse('login'), {'username': 'admin', 'password': 'wrongpass'})
        self.assertEqual(resp.status_code, 200)

    def test_register_creates_patient(self):
        resp = self.client.post(reverse('register'), {
            'username': 'newpatient', 'email': 'p@test.com', 'password': 'securepass123',
            'first_name': 'Test', 'last_name': 'Patient', 'role': 'patient'
        })
        self.assertRedirects(resp, reverse('login'))
        u = User.objects.get(username='newpatient')
        self.assertEqual(u.role, 'patient')
        self.assertFalse(u.is_approved)

    def test_approve_user(self):
        patient = User.objects.create_user('p3', password='x', role='patient', is_approved=False)
        self.client.force_login(self.admin)
        self.client.get(reverse("approve_user", args=[patient.id]), follow=True)
        patient.refresh_from_db()
        self.assertTrue(patient.is_approved)

    def test_dashboard_redirects_unauthenticated(self):
        resp = self.client.get(reverse('dashboard'))
        self.assertRedirects(resp, '/accounts/login/?next=/dashboard/')

    def test_health_check(self):
        resp = self.client.get(reverse('health_check'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, b'ok')

class HealthRecordTest(TestCase):
    def setUp(self):
        self.patient = User.objects.create_user('pt', password='x', role='patient', is_approved=True)
        PatientProfile.objects.create(user=self.patient)

    def test_create_health_record(self):
        r = HealthRecord.objects.create(patient=self.patient, heart_rate=72, temperature=36.6)
        self.assertEqual(r.patient, self.patient)
        self.assertEqual(r.heart_rate, 72)

    def test_upload_health_data(self):
        self.client.force_login(self.patient)
        resp = self.client.post(reverse('upload_health'), {
            'heart_rate': '80', 'temperature': '37.0', 'source': 'manual'
        })
        self.assertRedirects(resp, reverse('patient_records'))
        self.assertEqual(HealthRecord.objects.filter(patient=self.patient).count(), 1)

class MedicalReportTest(TestCase):
    def setUp(self):
        self.doctor = User.objects.create_user('dr1', password='x', role='doctor', is_approved=True)
        self.patient = User.objects.create_user('pt1', password='x', role='patient', is_approved=True)
        DoctorProfile.objects.create(user=self.doctor)
        PatientProfile.objects.create(user=self.patient)

    def test_create_report(self):
        r = MedicalReport.objects.create(
            doctor=self.doctor, patient=self.patient,
            title='Test Report', diagnosis='All good'
        )
        self.assertEqual(r.doctor, self.doctor)
        self.assertEqual(r.patient, self.patient)
        self.assertTrue(r.is_visible_to_patient)

    def test_write_report_view(self):
        self.client.force_login(self.doctor)
        resp = self.client.post(reverse('write_report'), {
            'patient': self.patient.id, 'title': 'Checkup', 'diagnosis': 'Healthy', 'visible': 'on'
        })
        self.assertRedirects(resp, reverse('doctor_reports'))
        self.assertEqual(MedicalReport.objects.count(), 1)

class MedicalOrderTest(TestCase):
    def setUp(self):
        self.doctor = User.objects.create_user('dr2', password='x', role='doctor', is_approved=True)
        self.patient = User.objects.create_user('pt2', password='x', role='patient', is_approved=True)
        DoctorProfile.objects.create(user=self.doctor)
        PatientProfile.objects.create(user=self.patient)

    def test_create_order(self):
        o = MedicalOrder.objects.create(
            doctor=self.doctor, patient=self.patient,
            order_type='ct_scan', description='Chest CT needed', priority='normal'
        )
        self.assertEqual(o.status, 'pending')
        self.assertEqual(o.order_type, 'ct_scan')
