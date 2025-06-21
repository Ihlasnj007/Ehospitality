from django.shortcuts import render,redirect,get_object_or_404
from .models import patientRegister,appointment,medicaldata
from django.contrib import messages
from datetime import date as current_date
from django.contrib.auth.hashers import make_password,check_password
from django.utils.timezone import now
import stripe
from django.conf import settings
from django.http import JsonResponse
from doctor.models import doctorRegister,prescriptionDetails


# Create your views here.

def register_file(request):
    if request.method == 'POST' :
        first = request.POST.get('firstName')
        last = request.POST.get('lastName')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        passwordHashed = make_password(request.POST.get('password'))

        if confirm_password!=password:
            messages.error(request, "Password do not Match")
            return redirect('patient-register')
        
        if patientRegister.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('patient-register')
        
        patient = patientRegister(
            first_name=first,
            last_name=last,
            dob=dob,
            gender=gender,
            email=email,
            phone=phone,
            address=address,
            password=passwordHashed
        )
        patient.save()

        return redirect('patient-login')  

    return render(request, 'patient/register.html')

def login_file(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            patient=patientRegister.objects.get(email=email)
        except patientRegister.DoesNotExist:
            messages.error(request, "Email doesnot Exist, Try signUp!")
            return redirect('patient-login')

        if check_password(password,patient.password):
            #login success
            request.session['patient_id'] = patient.id
            return redirect('patient-dashboard')
        else:
            messages.error(request, "Password Incorrect!")
            return redirect('patient-login')
        
    return render(request, 'patient/login.html')

def dashboard_file(request):
    patient_id=request.session.get('patient_id')
    if patient_id:
        try:
            patient=patientRegister.objects.get(id=patient_id)
            return render(request, 'patient/dashboard.html',{'patient':patient})
        except patientRegister.DoesNotExist:
            return redirect('patient-login')
    else:
        return redirect('patient-login')

def appointmentlist_file(request):
    # FOR GETTING DIFFERENT DATA FOR DIFFERENT PATIENTS
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient-login')

    today= current_date.today()
    patient=get_object_or_404(patientRegister, id=patient_id)
    all_appointment = appointment.objects.filter(patient=patient).order_by('-appointment_date','-appointment_time')
    return render(request, 'patient/appointment_list.html', {
        'appointments':all_appointment ,
        'today':today
    } )

# VIEW FOR CANCELLING APPOINTMENT
def cancel_appointment(request, id):
    patient_id = request.session.get('patient_id')
    appt=get_object_or_404(appointment, id=id, patient_id=patient_id)
    appt.delete()
    messages.success(request, "Cancelled Successfully")
    return redirect('patient-appointmentlist')


# APPOINTMENT DATA COLLECTION
def appointmentdata_file(request):
    # FOR DIFF USER DIFF DATA / FOR A PARTICULAR USER
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient-login')
    
    doctors = doctorRegister.objects.all()

    if request.method == 'POST':
        department = request.POST.get('department')
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')
        reason = request.POST.get('reason')

        patient=get_object_or_404(patientRegister,id=patient_id)

        from datetime import datetime
        try:
            appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format.')
            return redirect('patient-appointmentdata')

        # Check if the date is today or in the future
        if appointment_date < current_date.today():
            messages.error(request, 'Cannot book appointment for past dates.')
            return redirect('patient-appointmentdata')
        
        try:
            doctor = doctorRegister.objects.get(id=doctor_id)
        except doctorRegister.DoesNotExist:
            messages.error(request, 'Selected doctor does not exist.')
            return redirect('patient-appointmentdata')

        new_appointment = appointment(
            patient=patient,
            department=department,
            doctor=doctor,
            appointment_date=date,
            appointment_time=time,
            reason=reason
        )
        new_appointment.save()

        messages.success(request,'Appointment Booked successfully!')
        return redirect('patient-appointmentlist')

    return render(request, 'patient/appointment.html', {'doctors': doctors})

def medicalhistory_file(request):
    # DISPLAY DATA OF THAT PARTICULAR USER
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient-login')

    patient = get_object_or_404(patientRegister, id=patient_id)
    all_medicalhistory=medicaldata.objects.filter(patient=patient)
    return render(request, 'patient/medical_history.html', {"medicals":all_medicalhistory})

def medicaldata_file(request):
    # FOR A USER:
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient-login')
    
    doctors = doctorRegister.objects.all()

    if request.method == 'POST':
        date=request.POST.get('date')
        doctor_id=request.POST.get('doctor')
        diagnosis=request.POST.get('diagnosis')
        medications=request.POST.get('medications')
        allergies=request.POST.get('allergies')
        treatment=request.POST.get('treatment')

        patient=get_object_or_404(patientRegister, id=patient_id)

        from datetime import datetime, date as dt_date
        try:
            medical_date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format.')
            return redirect('patient-medicaldata')

        # Prevent pastdated medical entries
        if medical_date > dt_date.today():
            messages.error(request, 'Cannot add future medical records.')
            return redirect('patient-medicaldata')
        
        try:
            doctor = doctorRegister.objects.get(id=doctor_id)
        except doctorRegister.DoesNotExist:
            messages.error(request, 'Selected doctor does not exist.')
            return redirect('patient-appointmentdata')    

        new_medicaldata=medicaldata(
            patient=patient,
            medical_date=date,
            doctor=doctor,
            diagnosis=diagnosis,
            medications=medications,
            allergies=allergies,
            treatment=treatment
        )
        new_medicaldata.save()

    return render(request, 'patient/medical_list.html', {'doctors': doctors})


def payment_file(request):
    # PAYMENT OF THAT USER ONLY
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient-login')
    
    patient = get_object_or_404(patientRegister, id=patient_id)

    payments=appointment.objects.filter(patient=patient).order_by('-appointment_date','-appointment_time')

    unpaid_payments=payments.filter(is_paid=False)
    paid_payments=payments.filter(is_paid=True)

    return render(request, 'patient/bills.html', {
        'unpaid_payments':unpaid_payments,
        'paid_payments':paid_payments,
    } )

def create_checkout_session(request, id):
    patient_id = request.session.get('patient_id')
    appointment_instance = get_object_or_404(appointment, id=id, patient_id=patient_id)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'unit_amount': 50000,  # ₹500.00 (in paise)
                    'product_data': {
                        'name': f'Appointment with Dr. {appointment_instance.doctor}',
                        'description': f'{appointment_instance.department} - {appointment_instance.reason}',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(f'/patient/mark-paid/{appointment_instance.id}/'),
            cancel_url=request.build_absolute_uri('/patient/payments/'),
        )
        return redirect(checkout_session.url)
    except Exception as e:
        return JsonResponse({'error': str(e)})
    
def mark_paid(request, id):
        patient_id = request.session.get('patient_id')
        appt = get_object_or_404(appointment, id=id, patient_id=patient_id)
        appt.is_paid = True
        appt.payment_date = now().date()
        appt.save()
        return redirect('patient-payments') 


def health_file(request):
    return render(request, 'patient/health.html')

def myprescription(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient-login')
    
    prescriptions = prescriptionDetails.objects.filter(appointment__patient_id=patient_id)

    return render(request, 'patient/my_prescriptions.html', {'prescriptions': prescriptions})

def patient_logout(request):
    if 'patient_id' in request.session:
        del request.session['patient_id']
    return redirect('patient-login')
