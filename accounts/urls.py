from django.urls import path
from . import views

from . import views

urlpatterns = [
    # path('/createnurse/', views.addNurse),
    # path('/createdoctor/', views.addDoctor),
    # path('/checkusercheck/<roledata>' ,views.doctor_register),
    # path('/loginpage' , views.docter_login),
    # path('/logout' , views.doctor_logout),
    # path('/choise/', views.choiseview)
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('doctor/', views.doctor, name='doctor'),
    path('patientlist/', views.patientlist, name='patientlist'),
    path('newpatient/', views.newpatient, name='newpatient'),
    path('patientRecord/', views.patientRecord, name='patientRecord'),
    path('viewPatientRecord/', views.viewPatientRecord, name='viewPatientRecord'),
    path('OldviewPatientRecord/', views.OldviewPatientRecord, name='OldviewPatientRecord'),
    path('updatePatientRecord/', views.updatePatientRecord, name='updatePatientRecord'),
    path('choise/', views.choise, name='choise'),
    path('diagnosisPage/', views.diagnosisPage, name='diagnosisPage'),
    path('diagnosisDescription/', views.diagnosisDescription, name='diagnosisDescription'),
    path('labTest/', views.labTest, name='labTest'),
    path('medicationPage/', views.medicationPage, name='medicationPage'),
    path('viewMedicine/', views.viewMedicine, name='viewMedicine'),
    path('pred/', views.pred, name='pred'),


]