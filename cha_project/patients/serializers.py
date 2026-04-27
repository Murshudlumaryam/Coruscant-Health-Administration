from rest_framework import serializers
from .models import HealthRecord, PatientProfile

class HealthRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    class Meta:
        model = HealthRecord
        fields = '__all__'
        read_only_fields = ['id','recorded_at','patient']

class PatientProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    class Meta:
        model = PatientProfile
        fields = '__all__'
