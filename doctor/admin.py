# admin.py
from django.contrib import admin
from .models import MedicineDirection, LaboratoryTest, Diagnosis, MedicalDevice

@admin.register(MedicineDirection)
class MedicineDirectionAdmin(admin.ModelAdmin):
    list_display = ['patientId', 'medicineId', 'doseUnit', 'duration', 'doseTiming']

@admin.register(LaboratoryTest)
class LaboratoryTestAdmin(admin.ModelAdmin):
    list_display = ['patientId', 'testName', 'testSpecimen', 'testBodySite', 'testUse', 'testDescription', 'testReport']

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ['patientId', 'diagnosisName', 'diagnosisBodySite', 'dateOfOnset', 'severity', 'dateOfAbatement', 'diagnosisCertainity', 'createdDate']

@admin.register(MedicalDevice)
class MedicalDeviceAdmin(admin.ModelAdmin):
    list_display = ['patientId', 'deviceName', 'deviceBodySite', 'deviceUse', 'deviceDescription']
