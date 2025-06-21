from django.db import models
# Create your models here.

class patientRegister(models.Model):
    Gender_Choices=[
        ('male','male'),
        ('female','female'),
        ('other','other'),
        ('prefer-not-to-say','prefer not to say'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=20, choices=Gender_Choices)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class appointment(models.Model):
    Department_choices=[
        ('Cardiology', 'Cardiology'),
        ('General-Medicine','General Medicine'),
        ('Orthopedics','Orthopedics'),
        ('Neurology','Neurology'),
        ('Dermatology','Dermatology'),
        ('Pediatrics','Pediatrics'),
    ]

    patient=models.ForeignKey(patientRegister, on_delete=models.CASCADE)
    department=models.CharField(max_length=28,choices=Department_choices)
    doctor=models.ForeignKey('doctor.doctorRegister', on_delete=models.CASCADE)
    appointment_date=models.DateField()
    appointment_time=models.TimeField()
    reason=models.TextField()
    is_paid=models.BooleanField(default=False)
    is_prescribed=models.BooleanField(default=False)
    payment_date=models.DateField(null=True,blank=True)

    def __str__(self):
        if self.patient_id:  # this checks if patient FK is set
            return f"{self.patient} - {self.appointment_date}"
        return f"Missing Patient - {self.appointment_date}"


class medicaldata(models.Model):

    patient=models.ForeignKey(patientRegister, on_delete=models.CASCADE, null=True)
    medical_date=models.DateField()
    doctor=models.ForeignKey('doctor.doctorRegister', on_delete=models.CASCADE)
    diagnosis=models.CharField(max_length=100)
    medications=models.TextField(null=False, blank=False)
    allergies=models.CharField(max_length=100)
    treatment=models.TextField(null=False,blank=False)

    def __str__(self):
        return f"{self.patient} - {self.medical_date}"