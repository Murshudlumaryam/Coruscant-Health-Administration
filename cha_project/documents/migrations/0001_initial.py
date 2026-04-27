
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
            name='EncryptedDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_type', models.CharField(choices=[('lab_result', 'Lab Result'), ('prescription', 'Prescription'), ('imaging', 'Imaging'), ('insurance', 'Insurance'), ('id_document', 'ID Document'), ('consent_form', 'Consent Form'), ('other', 'Other')], default='other', max_length=30)),
                ('title', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='encrypted_docs/')),
                ('original_filename', models.CharField(max_length=255)),
                ('file_size', models.IntegerField(default=0)),
                ('is_encrypted', models.BooleanField(default=True)),
                ('checksum', models.CharField(blank=True, max_length=64)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to=settings.AUTH_USER_MODEL)),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents_uploaded', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
