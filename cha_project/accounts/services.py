from documents.models import EncryptedDocument
from doctors.models import MedicalOrder, MedicalReport
from emergency.models import EmergencyPatient
from patients.models import HealthRecord

from accounts.models import User


def build_dashboard(user):
    if user.role == "patient" or (user.is_superuser and user.role == "patient"):
        records = HealthRecord.objects.filter(patient=user)
        reports = MedicalReport.objects.filter(
            patient=user,
            is_visible_to_patient=True,
        )
        orders = MedicalOrder.objects.filter(patient=user)
        documents = EncryptedDocument.objects.filter(owner=user)
        return "dashboard/patient.html", {
            "health_records": records[:10],
            "reports": reports[:5],
            "orders": orders[:5],
            "documents": documents[:5],
            "patient_snapshot": {
                "records": records.count(),
                "reports": reports.count(),
                "orders": orders.count(),
                "documents": documents.count(),
            },
        }

    if user.role == "doctor":
        my_patients = User.objects.filter(
            patient_profile__assigned_doctor=user,
            role="patient",
        )
        recent_reports = MedicalReport.objects.filter(doctor=user)
        pending_orders = MedicalOrder.objects.filter(doctor=user, status="pending")
        return "dashboard/doctor.html", {
            "my_patients": my_patients,
            "recent_reports": recent_reports[:5],
            "pending_orders": pending_orders[:5],
            "doctor_snapshot": {
                "patients": my_patients.count(),
                "reports": recent_reports.count(),
                "pending_orders": pending_orders.count(),
            },
        }

    if user.role == "administrator" or user.is_superuser:
        pending_users = User.objects.filter(
            is_approved=False,
            role__in=["patient", "doctor"],
        )
        return "dashboard/admin.html", {
            "pending_users": pending_users,
            "pending_count": pending_users.count(),
            "total_patients": User.objects.filter(role="patient").count(),
            "total_doctors": User.objects.filter(role="doctor").count(),
            "total_records": HealthRecord.objects.count(),
            "recent_users": User.objects.order_by("-date_joined")[:10],
        }

    if user.role == "emergency":
        recent_emergency = EmergencyPatient.objects.filter(registered_by=user)
        return "dashboard/emergency.html", {
            "recent_emergency": recent_emergency[:10],
            "emergency_snapshot": {
                "active_cases": EmergencyPatient.objects.filter(
                    is_resolved=False
                ).count(),
                "registered_today": recent_emergency.count(),
            },
        }

    if user.role == "department":
        pending_orders = MedicalOrder.objects.filter(status="pending")
        in_progress_orders = MedicalOrder.objects.filter(status="in_progress")
        return "dashboard/department.html", {
            "pending_orders": pending_orders[:10],
            "in_progress_orders": in_progress_orders[:10],
            "department_snapshot": {
                "pending": pending_orders.count(),
                "active": in_progress_orders.count(),
            },
        }

    return "dashboard/base_dashboard.html", {}


def set_approval_state(user, approved):
    user.is_approved = approved
    user.is_active = approved
    user.save(update_fields=["is_approved", "is_active"])
