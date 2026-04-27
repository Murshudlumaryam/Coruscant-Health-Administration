from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import MedicalReport, MedicalOrder
from .serializers import MedicalReportSerializer, MedicalOrderSerializer

class IsDoctorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role in ('doctor','administrator') or request.user.is_superuser)

class MedicalReportListCreate(generics.ListCreateAPIView):
    serializer_class = MedicalReportSerializer

    def get_queryset(self):
        u = self.request.user
        if u.role == 'patient':
            return MedicalReport.objects.filter(patient=u, is_visible_to_patient=True)
        if u.role == 'doctor':
            return MedicalReport.objects.filter(doctor=u)
        return MedicalReport.objects.all()

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)

class MedicalOrderListCreate(generics.ListCreateAPIView):
    serializer_class = MedicalOrderSerializer
    permission_classes = [IsDoctorOrAdmin]

    def get_queryset(self):
        u = self.request.user
        if u.role == 'doctor':
            return MedicalOrder.objects.filter(doctor=u)
        return MedicalOrder.objects.all()

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)

class MedicalOrderDetail(generics.RetrieveUpdateAPIView):
    queryset = MedicalOrder.objects.all()
    serializer_class = MedicalOrderSerializer
