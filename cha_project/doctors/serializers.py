from rest_framework import serializers
from .models import MedicalReport, MedicalOrder, DoctorProfile

class MedicalReportSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    class Meta:
        model = MedicalReport
        fields = '__all__'
        read_only_fields = ['id','created_at','updated_at','doctor']

class MedicalOrderSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    order_type_display = serializers.CharField(source='get_order_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = MedicalOrder
        fields = '__all__'
        read_only_fields = ['id','created_at','updated_at','doctor']

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'
