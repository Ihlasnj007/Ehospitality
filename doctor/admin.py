from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import doctorRegister, prescriptionDetails
# Register your models here.

class doctorAdminsite(AdminSite):
    site_header = 'Doctor Admin Site'
    site_title = 'Doctor Admin Panel'
    index_title = 'Doctor Index'

doctor_admin = doctorAdminsite(name='doctor-admin')

doctor_admin.register(doctorRegister)
doctor_admin.register(prescriptionDetails)