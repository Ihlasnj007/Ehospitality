from django.db import models
from patient.models import appointment
# Create your models here.

class doctorRegister(models.Model):

    Specialization_choices = [
        ('Cardiology','Cardiology'),
        ('Dermatology','Dermatology'),
        ('Pediatrics','Pediatrics'),
        ('Neurology','Neurology'),
        ('Orthopedics','Orthopedics')
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    medical_license = models.CharField(max_length=100)
    specialization = models.CharField(max_length=15,choices=Specialization_choices)
    qualification = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class prescriptionDetails(models.Model):

    appointment = models.ForeignKey(appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    prescription = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.appointment.patient.first_name} - ({self.appointment.reason})"