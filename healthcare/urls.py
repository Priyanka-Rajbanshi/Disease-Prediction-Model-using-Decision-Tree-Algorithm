from django.contrib import admin
from django.urls import path
from healthcare import views

urlpatterns = [
    path('create/', views.create_patient, name='create_patient'),
    path('patients/', views.patient_list, name='patient_list'),
    
    path('add_record/<int:patient_id>/', views.add_patient_record, name='add_patient_record'),
    path('view_records/<int:patient_id>/', views.view_patient_records, name='view_patient_records'),
    path('update_patient_record/<int:record_id>/', views.update_patient_record, name='update_patient_record'),

     path('patient-detail/', views.patient_detail_view, name='patient_detail'),

    path('/newPatient', views.newPatient, name='newPatient'),
    path('/patientRecord/<patientId>', views.patientRecord, name='patientRecord'),
    path('/updatePatientRecord/<patientId>', views.updatePatientRecord, name='updatePatientRecord'),
]
