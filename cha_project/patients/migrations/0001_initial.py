
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recorded_at', models.DateTimeField(auto_now_add=True)),
                ('heart_rate', models.FloatField(blank=True, help_text='bpm', null=True)),
                ('temperature', models.FloatField(blank=True, help_text='°C', null=True)),
                ('blood_pressure_systolic', models.IntegerField(blank=True, null=True)),
                ('blood_pressure_diastolic', models.IntegerField(blank=True, null=True)),
                ('oxygen_saturation', models.FloatField(blank=True, help_text='%', null=True)),
                ('glucose_level', models.FloatField(blank=True, help_text='mg/dL', null=True)),
                ('weight', models.FloatField(blank=True, help_text='kg', null=True)),
                ('notes', models.TextField(blank=True)),
                ('source', models.CharField(choices=[('manual', 'Manual Entry'), ('device', 'Device Upload'), ('emergency', 'Emergency')], default='manual', max_length=50)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_records', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-recorded_at'],
            },
        ),
        migrations.CreateModel(
            name='PatientProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_type', models.CharField(blank=True, max_length=5)),
                ('allergies', models.TextField(blank=True)),
                ('emergency_contact', models.CharField(blank=True, max_length=100)),
                ('emergency_phone', models.CharField(blank=True, max_length=20)),
                ('insurance_number', models.CharField(blank=True, max_length=50)),
                ('assigned_doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patients', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
