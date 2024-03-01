
from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctorHome),
    path('/patient-list/', views.patientList),
    path('/patient-list/patient/<int:patientId>', views.patientRecord,name='patientDiagnosis'),
    path('/viewPrescription/<int:prescriptionId>', views.viewPrescription, name="viewPrescription"),
    path('/diagnosis/<int:patientId>', views.diagnosis),
    path('/medication/<int:prescriptionId>', views.medication),
    path('/searchpage/', views.searchPatient, name='searchlist'),
    path('/medicineFile/<int:prescriptionId>', views.medicineFile, name='medicineFile'),
    path('/laboratoryTest/<int:prescriptionId>', views.laboratoryTest, name='laboratoryTest'),
    path('/viewMedicine/<int:medicineId>/<int:prescriptionId>',views.viewMedicine, name='viewMedicine'),

    path('add_medicine/<int:patient_id>/', views.add_medicine, name='add_medicine'),
    path('patient/<int:patient_id>/medicine/', views.patient_medicine, name='patient_medicine'),
     path('<int:patient_id>/update_medicine/<int:medicine_id>/', views.update_medicine, name='update_medicine'),

    path('add_diagnosis/<int:patient_id>/', views.add_diagnosis, name='add_diagnosis'),
    path('view_diagnosis/<int:patient_id>/', views.view_diagnosis, name='view_diagnosis'),
    path('patient/<int:patient_id>/update_diagnosis/', views.update_diagnosis, name='update_diagnosis'),
]
