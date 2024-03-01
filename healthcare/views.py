from datetime import datetime
import json
from urllib import response
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
import random
from healthcare.models import Patient, PatientRecord, Symptom
from django.core.mail import send_mail
import uuid
from django.conf import settings
from .forms import PatientForm, PatientRecordForm, RegistrationNumberForm, SymptomForm
# Create your views here.
from django.http import HttpResponseBadRequest, QueryDict
from django.urls import reverse
from accounts.middleware import nurse_middleware,nursedata_middleware

def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')  # Redirect to a success page
    else:
        form = PatientForm()
    return render(request, 'newpatient.html', {'form': form})


def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patientlist.html', {'patients': patients})

def add_patient_record(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    
    if request.method == 'POST':
        record_form = PatientRecordForm(request.POST)
        if record_form.is_valid():
            record = record_form.save(commit=False)
            record.patientId = patient 
            record.save()
            
            # Process symptoms
            selected_symptoms = request.POST.getlist('selected_symptoms')  # Use getlist to retrieve multiple values
            for symptom in selected_symptoms:
                Symptom.objects.create(name=symptom.strip(), patient=record.patientId)  # Strip to remove extra spaces

            return redirect('patient_list')  # Move this line outside of the loop
    else:
        record_form = PatientRecordForm(initial={'patientId': patient})

    return render(request, 'patientRecord.html', {'record_form': record_form, 'patient': patient})

def update_patient_record(request, record_id):
    record = get_object_or_404(PatientRecord, pk=record_id)
    
    if request.method == 'POST':
        record_form = PatientRecordForm(request.POST, instance=record)
        if record_form.is_valid():
            record = record_form.save(commit=False)
            record.save()
        
            selected_symptoms = request.POST.getlist('selected_symptoms')  # Use getlist to retrieve multiple values
            
            # Clear existing symptoms for the record
            Symptom.objects.filter(patient=record.patientId).delete()
            
            # Add new symptoms to the record
            for symptom in selected_symptoms:
                Symptom.objects.create(name=symptom.strip(), patient=record.patientId)  # Corrected line
            
            return redirect(reverse('view_patient_records', kwargs={'patient_id': record.patientId.pk}))# Redirect to appropriate URL after successful update
    else:
        record_form = PatientRecordForm(instance=record)

    return render(request, 'updatePatientRecord.html', {'record_form': record_form, 'record': record})



def patient_detail_view(request):
    form = RegistrationNumberForm()  # Initialize the form outside the if block
    
    if request.method == 'POST':
        form = RegistrationNumberForm(request.POST)
        if form.is_valid():
            registration_number = form.cleaned_data['registration_number']
            patient = get_object_or_404(Patient, registrationNumber=registration_number)
            records = PatientRecord.objects.filter(patientId=patient)
            symptoms = patient.symptoms.all()
            return render(request, 'viewPatientRecord.html', {'patient': patient, 'records': records, 'symptoms': symptoms})
    
    return render(request, 'registrationNo.html', {'form': form})
# --------------------------------------
def view_patient_records(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    records = PatientRecord.objects.filter(patientId=patient)
    symptoms = patient.symptoms.all()
    return render(request, 'viewPatientRecord.html', {'patient': patient, 'records': records, 'symptoms': symptoms})

@nurse_middleware
def newPatient(request):
    try:
        if request.method == 'POST':
            try:
                name = request.POST['name']
                mobile = request.POST['mobile']
                email = request.POST['email']
                patient = Patient.objects.filter(email=email)
                if len(patient) != 0:
                    return render(request, 'newPatient.html',{'message':'Patient already exists'})
                gender = request.POST['gender']
                dateOfBirth = request.POST['dateOfBirth']
                bloodGroup = request.POST['bloodGroup']
                uuidNo = str(uuid.uuid4()).replace("-","")[0:10]
                registrationNumber = name.replace(' ','')+uuidNo+str(random.randint(2345678909800, 9923456789000))[0:5]
                patientData = Patient.objects.create(name=name,mobile=mobile,email=email,gender=gender,dateOfBirth=dateOfBirth,bloodGroup=bloodGroup,registrationNumber=registrationNumber)
                patientData.save()
            except:
                return render(request, 'newPatient.html',{'message':'Something went Wrong'})
            try:
                send_mail(
                    subject='Registered to Innovative Healthcare',
                    message='',
                    html_message=f'''Hi {name}, <br><br>
                Thank you for being part of Innovative healthcare.<br> Use the following registration id to view you prescription history<br>
                <b>{registrationNumber}</b><br><br>Regards<br>
                Innovative Healthcare''',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email]
                )
            except Exception as e:
                print(e)
                return render(request, 'newPatient.html',{'message':'Failed To Send Email'})
            finally:
                return render(request, 'newPatient.html',{'success':True, 'patientId':patientData.id})
        else:
            return render(request, 'newPatient.html')
    except Exception as e:
        print(e)
        return render(request, 'newPatient.html',{'message':'Something went wrong'})

# Create new patient record

@nursedata_middleware
def patientRecord(request, patientId):
    try:
        patient = Patient.objects.filter(id=patientId).first()
        if request.method == 'POST':
                patientRecord = PatientRecord.objects.filter(patientId=patientId)
                if len(patientRecord) != 0:
                    return render(request, 'patientRecord.html',{'message':'Patient record already exists'})
                height = request.POST['height']
                weight = request.POST['weight']
                allergies = request.POST['allergies']
                pregnancyStatus = request.POST.get('pregnancyStatus', None)
                if request.POST.get('estimatedDelivery', None) == None:
                    estimatedDelivery = None
                else:
                    estimatedDelivery = request.POST.get('estimatedDelivery', None)
                bloodPressure = request.POST['bloodPressure']
                pulseRate = request.POST['pulseRate']
                bodyTemprature = request.POST['bodyTemprature']
                isAlcolohic = request.POST.get('isAlcolohic',None)
                isSmoker = request.POST.get('isSmoker',None)
                isDiabetic = request.POST.get('isDiabetic',None)
                insurancePlanName = request.POST['insurancePlanName']
                insurancePlanNumber = request.POST['insurancePlanNumber']
                previousSurgery = request.POST['previousSurgery']
                status = request.POST['status']
                patientRecord = PatientRecord()
                patientRecord.patientId = patient
                patientRecord.bloodPressure =bloodPressure
                patientRecord.pulseRate = pulseRate
                patientRecord.bodyTemprature = bodyTemprature
                patientRecord.isAlcolohic = isAlcolohic
                patientRecord.isSmoker = isSmoker
                patientRecord.height = height
                patientRecord.weight = weight
                patientRecord.allergies = allergies
                patientRecord.pregnancyStatus = pregnancyStatus
                patientRecord.estimatedDelivery = estimatedDelivery
                patientRecord.insurancePlanName = insurancePlanName
                patientRecord.insurancePlanNumber = insurancePlanNumber
                patientRecord.isDiabetic = isDiabetic
                patientRecord.previousSurgery = previousSurgery
                patientRecord.status = status
                patientRecord.save()
                return redirect('/doctor/patient-list')
        else:
            return render(request, 'patientRecord.html', {'patient':patient,'patientId':patientId})
    except Exception as e:
        print(e)
        return HttpResponse("<h1>something went wrong!!!</h1>")
        
# update patient record
@nursedata_middleware
def updatePatientRecord(request, patientId):
    try:
        if request.session['role']!="Nurse":
            return render(request, 'index.html', {'messages': "You Are Not Authenticated"})

        patientP = Patient.objects.filter(id=patientId).first()
        patient = PatientRecord.objects.filter(patientId=patientId)
        if len(patient) == 0:
            return render(request, 'patientRecord.html',{'message':'Patient desnot exist!'})
        patientRecord = patient.first()
        if request.method == 'POST':
                height = request.POST['height']
                weight = request.POST['weight']
                allergies = request.POST['allergies']
                pregnancyStatus = request.POST.get('pregnancyStatus', None)
                if request.POST.get('estimatedDelivery', None) == None:
                    estimatedDelivery = None
                else:
                    estimatedDelivery = request.POST.get('estimatedDelivery', None)
                bloodPressure = request.POST['bloodPressure']
                pulseRate = request.POST['pulseRate']
                bodyTemprature = request.POST['bodyTemprature']
                isAlcolohic = request.POST.get('isAlcolohic',None)
                isSmoker = request.POST.get('isSmoker',None)
                isDiabetic = request.POST.get('isDiabetic',None)
                insurancePlanName = request.POST['insurancePlanName']
                insurancePlanNumber = request.POST['insurancePlanNumber']
                previousSurgery = request.POST['previousSurgery']
                status = request.POST['status']
                patientRecord.patientId = patientP
                patientRecord.bloodPressure =bloodPressure
                patientRecord.pulseRate = pulseRate
                patientRecord.bodyTemprature = bodyTemprature
                patientRecord.isAlcolohic = isAlcolohic
                patientRecord.isSmoker = isSmoker
                patientRecord.height = height
                patientRecord.weight = weight
                patientRecord.allergies = allergies
                patientRecord.pregnancyStatus = pregnancyStatus
                patientRecord.estimatedDelivery = estimatedDelivery
                patientRecord.insurancePlanName = insurancePlanName
                patientRecord.insurancePlanNumber = insurancePlanNumber
                patientRecord.isDiabetic = isDiabetic
                patientRecord.previousSurgery = previousSurgery
                patientRecord.status = status
                patientRecord.save()

                return render(request, 'updatePatientRecord.html',{'patient':patientRecord,'success':True,'profile':patientP})
                
        else:
            return render(request, 'updatePatientRecord.html', {'patient':patientRecord,'profile':patientP})
    except Exception as e:
        print(e)
        return HttpResponse("<h1>something went wrong!!!</h1>")