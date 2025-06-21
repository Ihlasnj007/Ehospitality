from django.urls import path
from .import views

urlpatterns = [
    path('register/',views.register_file, name='doctor_register'),
    path('login/',views.login_file, name='doctor_login'),
    path('dashboard/', views.dashboard_file, name='doctor_dashboard'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patient/<int:patient_id>/', views.patient_details, name='patient_details'),
    path('appointments/', views.appointment_schedule, name='appointment_schedule'),
    path('prescribe/', views.prescription_list, name='prescription_list'),
    path('prescribe/<int:appointment_id>/', views.prescription_form, name='prescription_form'),
    path('logout/', views.doctor_logout, name='doctor_logout'),
]