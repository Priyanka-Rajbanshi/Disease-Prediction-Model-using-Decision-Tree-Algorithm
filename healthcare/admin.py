from django.contrib import admin
from .models import Patient, PatientRecord, Symptom

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'email', 'gender', 'dateOfBirth')
    list_filter = ('gender', 'bloodGroup')
    search_fields = ('name', 'mobile', 'email')

@admin.register(PatientRecord)
class PatientRecordAdmin(admin.ModelAdmin):
    list_display = ('patientId', 'height', 'weight', 'bloodPressure', 'status')
    list_filter = ('status', 'alcohol', 'smoke', 'diabetic')
    search_fields = ('patientId__name', 'patientId__mobile', 'patientId__email')

@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ('name', 'patient')
    list_filter = ('patient',)
    search_fields = ('name', 'patient__name', 'patient__mobile', 'patient__email')
