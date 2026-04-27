from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('cha-admin/approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('cha-admin/reject/<int:user_id>/', views.reject_user, name='reject_user'),
]
