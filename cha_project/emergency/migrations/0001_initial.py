
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
            name='EmergencyPatient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='O', max_length=10)),
                ('chief_complaint', models.TextField()),
                ('severity', models.CharField(choices=[('critical', 'Critical'), ('severe', 'Severe'), ('moderate', 'Moderate'), ('minor', 'Minor')], default='moderate', max_length=10)),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('initial_vitals', models.JSONField(blank=True, default=dict)),
                ('notes', models.TextField(blank=True)),
                ('is_resolved', models.BooleanField(default=False)),
                ('linked_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='emergency_records', to=settings.AUTH_USER_MODEL)),
                ('registered_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-registered_at'],
            },
        ),
    ]
