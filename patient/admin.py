from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import patientRegister,appointment,medicaldata
# Register your models here.

class patientAdminsite(AdminSite):
    site_header="Patient Admin Site"
    site_title="patient Admin panel"
    index_title="Patient Management"

patient_admin = patientAdminsite(name='patient_admin')

patient_admin.register(patientRegister)
patient_admin.register(appointment)
patient_admin.register(medicaldata)