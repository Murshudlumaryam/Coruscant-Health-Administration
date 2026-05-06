from django.test import TestCase

from accounts.models import User
from patients.forms import HealthRecordForm


class HealthRecordFormTest(TestCase):
    def test_requires_reading_or_note(self):
        form = HealthRecordForm(data={"source": "manual"})
        self.assertFalse(form.is_valid())

    def test_accepts_single_reading(self):
        form = HealthRecordForm(data={"heart_rate": 72, "source": "device"})
        self.assertTrue(form.is_valid())
