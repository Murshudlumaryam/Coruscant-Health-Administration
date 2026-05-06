from django.test import TestCase

from emergency.forms import EmergencyRegistrationForm


class EmergencyRegistrationFormTest(TestCase):
    def test_build_initial_vitals(self):
        form = EmergencyRegistrationForm(
            data={
                "first_name": "Leia",
                "last_name": "Organa",
                "gender": "F",
                "chief_complaint": "Respiratory distress",
                "severity": "critical",
                "heart_rate": "110",
                "blood_pressure": "90/60",
                "temperature": "38.2",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.build_initial_vitals()["heart_rate"], "110")
