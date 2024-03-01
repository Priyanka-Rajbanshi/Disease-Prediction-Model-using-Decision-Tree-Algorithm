from django.core.checks import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, response
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate
from .models import Prescription, Medicine, Diagnosis,MedicalDevice,LaboratoryTest,MedicineDirection,MedicineDirPrescriptionMap
from healthcare.models import Patient, PatientRecord
from accounts.middleware import  doctor_middleware , both_middleware,doctordata_middleware, doctordata1_middleware
from django.db import transaction

from django.http import FileResponse
import io
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter

def medicineFile(request, prescriptionId):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize= letter, bottomup= 0)
    textob= c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 16)
    p=("Patient Name-")
    textob.textLine(p)
    prescription = Prescription.objects.get(pk=prescriptionId)
    patient = Patient.objects.get(pk=prescription.patientId.id)
    diagnosis = Diagnosis.objects.get(pk=prescription.diagnosisId.id)
    medicinDirMap = MedicineDirPrescriptionMap.objects.filter(prescriptionId=prescription)
    textob.textLine(patient.name)
    q=("Diagnosis Name-")
    textob.textLine(q)
    textob.textLine(diagnosis.diagnosisName)
    r=("----------------------------------------------------------")
    textob.textLine(r)
    t=("[MEDICINES]")
    textob.textLine(t)
    if len(medicinDirMap) != 0:
            print('in if')
            medsDirList = []
            for entry in medicinDirMap:
                medsDir = MedicineDirection.objects.filter(pk=entry.medicineDirectionId.id).first()
                medsName = Medicine.objects.filter(pk=medsDir.medicineId.id).first()
                medsDirList.append({
                    'medsDir':medsDir,
                    'medsName':medsName
                })
            lines = []
            for meds in medsDirList:
                lines.append("Name-")
                lines.append(meds['medsName'].name)
                lines.append("Dose Unit-")
                lines.append(meds['medsDir'].doseUnit)
                lines.append("Duration-")
                lines.append(meds['medsDir'].duration)
                lines.append("Number Of Times-")
                lines.append(meds['medsDir'].doseTiming)
                lines.append("Instruction-")
                lines.append(meds['medsDir'].additionalInstruction)
                lines.append("Reason-")
                lines.append(meds['medsDir'].reason)
                lines.append("----------------------------------------------------------")
            
            for line in lines:
                textob.textLine(line)
    c.drawText(textob) 
    c.showPage() 
    c.save()  
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='medicine.pdf')

@both_middleware
def searchPatient(request):
    try:
        print(request.session['role'])
        if request.session['role']!= "Doctor" and request.session['role']!="Nurse":
            return render(request, 'index.html', {'messages': "You Are Not Authenticated"})
        if request.method == 'POST':
            searched = request.POST['searched']
            data = Patient.objects.filter(name__contains=searched)
            return render(request, "patientlist.html", {'data':data})   
    
    except Exception as e:
        messages.add_message(request, messages.ERROR, "Please Add Valid Details !")
        return render(request, "viewPatientRecord.html")

@both_middleware
def doctorHome(request):
    try:
        if request.session['role']!= "Doctor" and request.session['role']!="Nurse":
            messages.add_message(request, messages.ERROR, "Please Add Valid Details !")
            return render(request, 'index.html')
        return render(request, "doctor.html", {}) 
    except Exception as e:
        messages.add_message(request, messages.ERROR, "Please Add Valid Details !")
        return render(request, "index.html")

# Patient List
@both_middleware
def patientList(request):
    try:
        if request.session['role']!= "Doctor" and request.session['role']!="Nurse":
            messages.add_message(request, messages.ERROR, "Please Add Valid Details !")

            return render(request, 'index.html')
        data_pagin = Patient.objects.all().order_by('-createdDate')
        paginator = Paginator(data_pagin, 10)
        page_number = request.GET.get('page')
        data = paginator.get_page(page_number)
        return render(request, "patientlist.html", {'data':data})     
    except Exception as e:
        print(e)
        messages.add_message(request, messages.ERROR, "Please Add Valid Details !")
        return render(request, "viewPatientRecord.html")

# Patient Detail
def patientRecord(request, patientId):
    try:
        patientDetails = Patient.objects.get(pk=patientId)
        his = PatientRecord.objects.filter(patientId=patientDetails)
        if(len(his)!=0):
            history=his.first()
            allPrescription = Prescription.objects.filter(patientId=patientDetails)
            prescriptionListData = []
            for prep in allPrescription:
                diagnosis = Diagnosis.objects.get(pk=prep.diagnosisId.id)
                prescriptionListData.append({
                    'diagnosisCreatedDate': diagnosis.createdDate,
                    'diagnosisName': diagnosis.diagnosisName,
                    'prescriptionId':prep.id
                })
            return render(request, "viewPatientRecord.html", {'history':history, 'details':patientDetails,'prescriptionList':prescriptionListData}) 
        else:
            return render(request, "viewPatientRecord.html", {'noRecord':True, 'details':patientDetails})
    except Exception as e:
        print(e)
        messages.add_message(request, messages.ERROR, "Please Add Valid Details !")
        return redirect('/')

# See Prescription
def viewMedicine(request,medicineId,prescriptionId):
    try:
        medicineDetails = Medicine.objects.get(pk=medicineId)
        return render(request,'viewMedicine.html',{'medicineDetails': medicineDetails,'prescriptionId':prescriptionId})
    except Exception as e:
        print(e)
        return redirect('viewPrescription',prescriptionId)

def viewPrescription(request, prescriptionId):
    try:
        prescription = Prescription.objects.get(pk=prescriptionId)
        patient = Patient.objects.get(pk=prescription.patientId.id)
        diagnosis = Diagnosis.objects.get(pk=prescription.diagnosisId.id)
        medicalDevice = MedicalDevice.objects.get(pk=prescription.medicalDevice.id)
        laboratoryTest = LabTestPrescriptionMap.objects.filter(prescriptionId=prescription)
        tests=[]
        if(len(laboratoryTest)>0):
            for lab in laboratoryTest:
                test = LaboratoryTest.objects.get(pk=lab.laboratoryTestId.id)
                tests.append(test)
        medicinDirMap = MedicineDirPrescriptionMap.objects.filter(prescriptionId=prescription)
        medsDirList = []
        if len(medicinDirMap) != 0:
            for entry in medicinDirMap:
                medsDir = MedicineDirection.objects.filter(pk=entry.medicineDirectionId.id).first()
                medsName = Medicine.objects.filter(pk=medsDir.medicineId.id).first()
                medsDirList.append({
                    'medsDir':medsDir,
                    'medsName':medsName
                })
                print(medsDirList)
        data = {
            'prescriptionId':prescriptionId,
            'patient':patient,
            'diagnosis':diagnosis,
            'medicalDevice':medicalDevice,
            'laboratoryTest':tests,
            'medsDirList':medsDirList
        }
        return render(request, "diagnosisDescription.html",{'data':data})
       
    except Exception as e:
        print(e)
        messages.add_message(request, messages.ERROR, "Something went wrong!")

        return render('/')   

@doctordata1_middleware
def laboratoryTest(request,prescriptionId):
    try:
        if request.method == 'POST':
            testName = request.POST.get('testName',None)
            testBodySite = request.POST.get('testBodySite',None)
            testUse = request.POST.get('testUse',None)
            testDescription =  request.POST.get('testDescription',None)
            testSpecimen =  request.POST.get('testSpecimen',None)
            with transaction.atomic():
                laboratoryTestData = LaboratoryTest.objects.create(testName=testName,testBodySite=testBodySite,testUse=testUse,testDescription=testDescription, testSpecimen=testSpecimen)
                prescription = Prescription.objects.get(pk=prescriptionId)
                labTestData = LabTestPrescriptionMap.objects.create(laboratoryTestId=laboratoryTestData, prescriptionId=prescription)
            # message='Test Added Successfully!'
            return render(request, 'labTest.html',{'prescriptionId':prescriptionId, 'success':"Test Added Successfully!"})
        else:
            return render(request, 'labTest.html',{'prescriptionId':prescriptionId})
        
    except:
        return render(request, 'labTest.html',{'prescriptionId':prescriptionId,'message':"Something Went Wrong!"})
@doctordata_middleware      
def diagnosis(request, patientId):
    try:
        if request.session['role']!= "Doctor":
            return render(request, 'index.html', {'messages': "You Are Not Authenticated"})
        patient = Patient.objects.filter(id=patientId).first()
        if request.method == 'POST':
            diagnosisName = request.POST.get('diagnosisName',None)
            diagnosisBodySite = request.POST.get('diagnosisBodySite',None)
            if request.POST['dateOfOnset'] == '':
                dateOfOnset = None
            else:
                dateOfOnset = request.POST['dateOfOnset']
            severity = request.POST.get('severity',None)
            if request.POST['dateOfAbatement'] == '':
                dateOfAbatement = None
            else:
                dateOfAbatement = request.POST['dateOfAbatement']
            diagnosisCertainity = request.POST.get('diagnosisCertainity',None)
            diagnosisDescription = request.POST.get('diagnosisDescription',None)
            deviceName = request.POST.get('deviceName',None)
            deviceBodySite = request.POST.get('deviceBodySite',None)
            deviceUse = request.POST.get('deviceUse',None)
            deviceDescription = request.POST.get('deviceDescription',None)
            
            with transaction.atomic():
                diagnosisData = Diagnosis.objects.create(diagnosisName=diagnosisName,diagnosisBodySite=diagnosisBodySite,dateOfOnset=dateOfOnset,severity=severity,dateOfAbatement=dateOfAbatement,diagnosisCertainity=diagnosisCertainity,diagnosisDescription=diagnosisDescription)
                deviceData = MedicalDevice.objects.create(deviceName=deviceName,deviceBodySite=deviceBodySite,deviceUse=deviceUse,deviceDscription=deviceDescription)
                prescriptionData = Prescription.objects.create(patientId=patient,diagnosisId=diagnosisData,medicalDevice=deviceData)
                allMeds = Medicine.objects.all()
                prescriptionId=prescriptionData.id
            return redirect('viewPrescription',prescriptionId)
        else:
            return render(request, "diagnosisPage.html",{'patient':patient})
    except Exception as e:
        print(e)
        return render(request, "diagnosisPage.html",{'patient':patient, 'message':'Something Went Wrong!'})

@doctordata1_middleware
def medication(request, prescriptionId):
    try:
        if request.session['role']!= "Doctor":
            return render(request, 'index.html', {'messages': "You Are Not Authenticated"})
        allMeds = Medicine.objects.all()
        if request.method == 'POST':
            medicineId = request.POST['medicineId']
            medicine = Medicine.objects.filter(id=medicineId).first()
            doseUnit = request.POST['doseUnit']
            duration = request.POST['duration']
            doseTiming = request.POST['doseTiming']
            additionalInstruction = request.POST['additionalInstruction']
            reason = request.POST['reason']
            with transaction.atomic():
                medicationData = MedicineDirection.objects.create(medicineId=medicine,doseUnit=doseUnit,duration=duration,doseTiming=doseTiming,additionalInstruction=additionalInstruction,reason=reason)
                prescription = Prescription.objects.get(pk=prescriptionId)
                medicationDirData = MedicineDirPrescriptionMap.objects.create(prescriptionId=prescription,medicineDirectionId=medicationData)
            return render(request, "medicationPage.html",{'prescriptionId':prescriptionId, 'allMeds':allMeds, 'success':"Medicine Added Successfullty"})
        else:
            return render(request, "medicationPage.html",{'prescriptionId':prescriptionId,'allMeds':allMeds,})
    except Exception as e:
        print(e)
        allMeds = Medicine.objects.all()
        return render(request, "medicationPage.html",{'prescriptionId':prescriptionId,'allMeds':allMeds,'message':"Please Fill All The Required Details!"})

# ------------------------------------------------------------------------


from django.shortcuts import render, redirect
from .models import MedicineDirection, Patient
from .forms import DiagnosisForm, MedicalDeviceForm, MedicineDirectionForm

def add_medicine(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    if request.method == 'POST':
        form = MedicineDirectionForm(request.POST)
        if form.is_valid():
            medicine_direction = form.save(commit=False)
            medicine_direction.patientId = patient  # Note: patientId should be set as patient object, not patient_id
            medicine_direction.save()
            return redirect('patient_list')  # Redirect to a success URL
    else:
        form = MedicineDirectionForm()  # No need to pass patient here
    return render(request, 'medicationPage.html', {'form': form, 'patient': patient})

def update_medicine(request, patient_id, medicine_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    medicine_direction = get_object_or_404(MedicineDirection, pk=medicine_id)
    
    if request.method == 'POST':
        form = MedicineDirectionForm(request.POST, instance=medicine_direction)
        if form.is_valid():
            form.save()
            return redirect('patient_list')  # Redirect to a success URL
    else:
        form = MedicineDirectionForm(instance=medicine_direction)
    return render(request, 'update_medicine.html', {'form': form, 'patient': patient})

def patient_medicine(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    medicines = MedicineDirection.objects.filter(patientId=patient)
    return render(request, 'viewMedicine.html', {'patient': patient, 'medicines': medicines})


def add_diagnosis(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    if request.method == 'POST':
        diagnosis_form = DiagnosisForm(request.POST)
        device_form = MedicalDeviceForm(request.POST)
        if diagnosis_form.is_valid() and device_form.is_valid():
            diagnosis = diagnosis_form.save(commit=False)
            diagnosis.patientId = patient  # Assign patient to the diagnosis object
            diagnosis.save()
            device = device_form.save(commit=False)
            device.patientId = patient  # Assign patient to the device object
            device.save()
            return redirect('patient_list')  # Redirect to patient detail page
    else:
        diagnosis_form = DiagnosisForm()
        device_form = MedicalDeviceForm()  # Don't pass patient to the form
    return render(request, 'diagnosisPage.html', {'diagnosis_form': diagnosis_form, 'device_form': device_form, 'patient': patient})

def view_diagnosis(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    diagnoses = Diagnosis.objects.filter(patientId=patient)
    medical_devices = MedicalDevice.objects.filter(patientId=patient)
    return render(request, 'diagnosisDescription.html', {'patient': patient, 'diagnoses': diagnoses, 'medical_devices': medical_devices})

def update_diagnosis(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    diagnosis = Diagnosis.objects.filter(patientId=patient).first()
    device = MedicalDevice.objects.filter(patientId=patient).first()
    
    if request.method == 'POST':
        diagnosis_form = DiagnosisForm(request.POST, instance=diagnosis)
        device_form = MedicalDeviceForm(request.POST, instance=device)
        
        print("POST data:", request.POST)  # Debugging
        
        if diagnosis_form.is_valid() and device_form.is_valid():
            diagnosis = diagnosis_form.save(commit=False)
            diagnosis.patientId = patient
            diagnosis.save()
            
            device = device_form.save(commit=False)
            device.patientId = patient
            device.save()
            
            print("Diagnosis:", diagnosis)  # Debugging
            print("Device:", device)  # Debugging
            
            return redirect('view_diagnosis', patient_id=patient_id)
        else:
            print("Diagnosis form errors:", diagnosis_form.errors)  # Debugging
            print("Device form errors:", device_form.errors)  # Debugging
    else:
        diagnosis_form = DiagnosisForm(instance=diagnosis)
        device_form = MedicalDeviceForm(instance=device)
        
    return render(request, 'updatediagonis.html', {'diagnosis_form': diagnosis_form, 'device_form': device_form, 'patient': patient})