from django import forms
from .models import Patient, PatientRecord, Symptom

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'mobile', 'email', 'bloodGroup', 'gender', 'dateOfBirth']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Name'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Enter Email'}),
            'bloodGroup': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Blood Group'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'dateOfBirth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        # Add validation logic for mobile number if needed
        return mobile

    def clean_email(self):
        email = self.cleaned_data['email']
        # Add validation logic for email if needed
        return email

    def clean_dateOfBirth(self):
        date_of_birth = self.cleaned_data['dateOfBirth']
        # Add validation logic for date of birth if needed
        return date_of_birth
    
class PatientRecordForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = [ 'height', 'weight', 'bloodPressure', 'pulseRate', 'bodyTemprature', 'alcohol', 'smoke', 'diabetic', 'allergies', 'insurancePlanName', 'insurancePlanNumber', 'status']
        widgets = {
            'height': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Height in cm *'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Weight in kg *'}),
            'bloodPressure': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Blood Pressure in mm'}),
            'pulseRate': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Pulse Rate in BPM'}),
            'bodyTemprature': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Body Temprature(°F)'}),
            'alcohol': forms.Select(attrs={'class': 'form-control'}),
            'smoke': forms.Select(attrs={'class': 'form-control'}),
            'diabetic': forms.Select(attrs={'class': 'form-control'}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,'placeholder': 'Allergies *'}),
            'insurancePlanName': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Insurance Plan Name*'}),
            'insurancePlanNumber': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Insurance Number*'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        patient = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)
        if patient:
            self.fields['patientId'].widget = forms.HiddenInput()
            self.initial['patientId'] = patient.pk  # Set the initial value for patientId

class SymptomForm(forms.ModelForm):
    class Meta:
        model = Symptom
        fields = ['name']

class RegistrationNumberForm(forms.Form):
    registration_number = forms.CharField(max_length=50, label='Registration Number')