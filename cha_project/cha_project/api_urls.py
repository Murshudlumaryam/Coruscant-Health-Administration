from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.api_views import api_register, api_login, api_me, api_pending_users, api_approve_user, UserListAPI
from patients.api_views import HealthRecordListCreate, HealthRecordDetail, api_patient_summary
from doctors.api_views import MedicalReportListCreate, MedicalOrderListCreate, MedicalOrderDetail

urlpatterns = [
    path('auth/register/', api_register, name='api_register'),
    path('auth/login/', api_login, name='api_login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('auth/me/', api_me, name='api_me'),
    path('admin/users/', UserListAPI.as_view(), name='api_users'),
    path('admin/pending/', api_pending_users, name='api_pending'),
    path('admin/approve/<int:user_id>/', api_approve_user, name='api_approve'),
    path('health-records/', HealthRecordListCreate.as_view(), name='api_health_records'),
    path('health-records/<int:pk>/', HealthRecordDetail.as_view(), name='api_health_record_detail'),
    path('health-records/summary/', api_patient_summary, name='api_patient_summary'),
    path('reports/', MedicalReportListCreate.as_view(), name='api_reports'),
    path('orders/', MedicalOrderListCreate.as_view(), name='api_orders'),
    path('orders/<int:pk>/', MedicalOrderDetail.as_view(), name='api_order_detail'),
]
