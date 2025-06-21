from datetime import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from .models import doctorRegister, prescriptionDetails
from patient.models import appointment, medicaldata, patientRegister

# Create your views here.


def register_file(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstName')
        lastname = request.POST.get('lastName')
        emailaddress = request.POST.get('email')
        password = request.POST.get('password')
        phonenumber = request.POST.get('phone')
        medicallicense = request.POST.get('licenseNumber')
        specialization = request.POST.get('specialization')
        qualification = request.POST.get('qualification')
        hospitalname = request.POST.get('clinicName')
        address = request.POST.get('address')
        passwordhash = make_password(request.POST.get('password'))

        if doctorRegister.objects.filter(email_address=emailaddress).exists():
            messages.error(request, 'Email Already in Use!')
            return redirect('doctor_register')
        
        doctor = doctorRegister(
            first_name = firstname,
            last_name = lastname,
            email_address = emailaddress,
            password = passwordhash,
            phone_number = phonenumber,
            medical_license = medicallicense,
            specialization = specialization,
            qualification = qualification,
            hospital_name = hospitalname,
            address = address,
        )
        doctor.save()

        return redirect('doctor_login')   

    return render(request, 'doctor/doc_register.html')

def login_file(request):
    if request.method == 'POST':
        emailaddress = request.POST.get('email')
        password = request.POST.get('password')

        try:
            doctor = doctorRegister.objects.get(email_address=emailaddress)
        except doctorRegister.DoesNotExist:
            messages.error(request, 'Email does not Exists..! Please Register..')
            return redirect('doctor_login')

        if check_password(password,doctor.password):
            # LOGIN SUCCESS
            request.session['doctor_id'] = doctor.id   # Creates a session id for that particular doctor
            return redirect('doctor_dashboard')
        else:
            messages.error(request, "Password Incorrect!")
            return redirect('doctor_login')

    return render(request, 'doctor/doc_login.html')

def dashboard_file(request):

    doctor_id = request.session.get('doctor_id')
    if doctor_id:
        try:
            doctor = doctorRegister.objects.get(id=doctor_id)
            return render(request, 'doctor/doc_dashboard.html', {'doctor': doctor})
        except doctorRegister.DoesNotExist:
            return redirect('doctor_login')
    else:
        return redirect('doctor_login')

def patient_list(request):

    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')
    
    try:
        doctor = doctorRegister.objects.get(id=doctor_id)
    except doctorRegister.DoesNotExist:
        return redirect('doctor_login')
    
    appointments = appointment.objects.filter(doctor=doctor)

    medicaldatas = medicaldata.objects.filter(doctor=doctor)

    medicals = []
    for meds in medicaldatas:
        if meds.patient not in medicals:
            medicals.append(meds.patient)

    patients = []
    for appt in appointments:
        if appt.patient not in patients:
            patients.append(appt.patient)

    display_list = []
    for patient in patients:
        status = "followUp" if patient in medicals else "New Patient"
        display_list.append({'patient': patient, 'status': status})

    return render(request, 'doctor/patient_list.html', {
        'display_list': display_list,
        'doctor': doctor,
        })

def patient_details(request, patient_id):

    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')
    
    doctor = get_object_or_404(doctorRegister, id=doctor_id)
    patient = get_object_or_404(patientRegister, id=patient_id)

    return render(request, 'doctor/patient_details.html', {
        'doctor': doctor,
        'patient': patient,
        })

def appointment_schedule(request):

    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')
    
    try:
        doctor = doctorRegister.objects.get(id=doctor_id)
    except doctorRegister.DoesNotExist:
        return redirect('doctor_login')
    
    appointments = appointment.objects.filter(doctor=doctor)

    appointment_list = []
    now = timezone.now()

    for appt in appointments:
        appt_datetime = datetime.combine(appt.appointment_date, appt.appointment_time)
        appt_datetime = timezone.make_aware(appt_datetime, timezone.get_current_timezone())
        status = "Completed" if appt_datetime < now else "Upcoming"
        appointment_list.append({
            'appointment': appt,
            'status': status
        })

    return render(request, 'doctor/myappointments.html', {
        'appointments': appointment_list,
        'doctor': doctor,
    })


def prescription_list(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')
    
    try:
        doctor = doctorRegister.objects.get(id=doctor_id)
    except doctorRegister.DoesNotExist:
        return redirect('doctor_login')
    
    appointments_with_prescription = appointment.objects.filter(doctor=doctor, is_prescribed=True)
    appointments_needing_prescription = appointment.objects.filter(doctor=doctor, is_prescribed=False)

    return render(request, 'doctor/prescription_list.html', {
        'doctor': doctor,
        'appointments_with_prescription': appointments_with_prescription,
        'appointments_needing_prescription': appointments_needing_prescription,
    })


def prescription_form(request, appointment_id):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')

    doctor = get_object_or_404(doctorRegister, id=doctor_id)
    appointment_obj = get_object_or_404(appointment, id=appointment_id)

    if appointment_obj.is_prescribed:
        messages.error(request, "This appointment has already been prescribed.")
        return redirect('prescription_list')


    if request.method == 'POST':
        diagnosis = request.POST.get('diagnosis')
        prescription = request.POST.get('prescription')

        if diagnosis and prescription:
            prescriptionDetails.objects.create(
                appointment=appointment_obj,
                diagnosis=diagnosis,
                prescription=prescription,
            )

            appointment_obj.is_prescribed = True
            appointment_obj.save()

            messages.success(request, 'prescription saved successfully')
            return redirect('prescription_list')
        else:
            messages.error(request, 'All fields are Required')

    return render(request, 'doctor/prescription_details.html', {
        'appointments': appointment_obj,
        'doctor': doctor
        })


def doctor_logout(request):
    # Clear the doctor session
    if 'doctor_id' in request.session:
        del request.session['doctor_id']
    return redirect('doctor_login')