from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('otp-verify/', views.otp_verify_view, name='otp_verify'),
    path('whitedevil-dashboard/', views.whitedevil_dashboard_view, name='whitedevil_dashboard'),
    path('whitedevil-dashboard/approve/<int:attempt_id>/', views.admin_approve_login, name='admin_approve_login'),
    path('whitedevil-dashboard/reset-device/<int:user_id>/', views.admin_reset_device, name='admin_reset_device'),
    path('whitedevil-dashboard/terminate/<int:user_id>/', views.admin_terminate_session, name='admin_terminate_session'),
]
