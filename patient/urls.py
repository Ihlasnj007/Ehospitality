from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.register_file, name="patient-register"),
    path('login/', views.login_file, name="patient-login"),
    path('dashboard/', views.dashboard_file, name="patient-dashboard"),
    path('appointmentlist/', views.appointmentlist_file, name="patient-appointmentlist"),
    path('appointmentdata/', views.appointmentdata_file, name="patient-appointmentdata"),
    path('medicallist/', views.medicalhistory_file, name="patient-medicallist"),
    path('medicaldata/', views.medicaldata_file, name="patient-medicaldata"),
    path('payments/', views.payment_file, name="patient-payments"),
    path('health/', views.health_file, name="patient-health"),
    path('myprescriptions/',views.myprescription, name="my-prescription"),
    path('mark-paid/<int:id>/', views.mark_paid, name='mark-paid'),
    path('cancel-appointment/<int:id>/',views.cancel_appointment, name="appointment-cancel"),
    path('create-checkout-session/<int:id>/', views.create_checkout_session, name='create-checkout-session'),
    path('logout/', views.patient_logout, name='patient-logout'),
]
