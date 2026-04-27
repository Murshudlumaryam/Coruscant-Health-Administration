from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import HealthRecord, PatientProfile
from .serializers import HealthRecordSerializer, PatientProfileSerializer

class HealthRecordListCreate(generics.ListCreateAPIView):
    serializer_class = HealthRecordSerializer

    def get_queryset(self):
        u = self.request.user
        if u.role in ('doctor','administrator') or u.is_superuser:
            patient_id = self.request.query_params.get('patient_id')
            if patient_id:
                return HealthRecord.objects.filter(patient_id=patient_id)
            return HealthRecord.objects.all()
        return HealthRecord.objects.filter(patient=u)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

class HealthRecordDetail(generics.RetrieveAPIView):
    serializer_class = HealthRecordSerializer

    def get_queryset(self):
        u = self.request.user
        if u.role in ('doctor','administrator') or u.is_superuser:
            return HealthRecord.objects.all()
        return HealthRecord.objects.filter(patient=u)

@api_view(['GET'])
def api_patient_summary(request):
    u = request.user
    records = HealthRecord.objects.filter(patient=u)
    latest = records.first()
    return Response({
        'total_records': records.count(),
        'latest': HealthRecordSerializer(latest).data if latest else None,
    })
