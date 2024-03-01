from django import forms
from .models import MedicineDirection, LaboratoryTest, Diagnosis, MedicalDevice

class MedicineDirectionForm(forms.ModelForm):
    class Meta:
        model = MedicineDirection
        fields = ['medicineId', 'doseUnit', 'duration', 'doseTiming', 'additionalInstruction', 'reason']
        widgets = {
            'medicineId': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Name of medicine *'}),
            'doseUnit': forms.TextInput(attrs={'class': 'form-control','placeholder': 'DoseUnit *'}),
            'duration': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Duration *'}),
            'doseTiming': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Number Of Times  *'}),
            'additionalInstruction': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Instruction *'}),
            'reason': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Reason *'}),
        }

    def __init__(self, *args, **kwargs):
        patient = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)
        if patient:
            self.fields['patientId'].widget = forms.HiddenInput()
            self.initial['patientId'] = patient.pk   # Set the initial value for patientId

class LaboratoryTestForm(forms.ModelForm):
    class Meta:
        model = LaboratoryTest
        fields = ['testName', 'testSpecimen', 'testBodySite', 'testUse', 'testDescription', 'testReport']
        widgets = {
            'testName': forms.TextInput(attrs={'class': 'form-control'}),
            'testSpecimen': forms.TextInput(attrs={'class': 'form-control'}),
            'testBodySite': forms.TextInput(attrs={'class': 'form-control'}),
            'testUse': forms.TextInput(attrs={'class': 'form-control'}),
            'testDescription': forms.TextInput(attrs={'class': 'form-control'}),
            'testReport': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        patient = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)
        if patient:
            self.fields['patientId'].widget = forms.HiddenInput()
            self.initial['patientId'] = patient.pk  # Set the initial value for patientId


class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['diagnosisName', 'diagnosisBodySite', 'dateOfOnset', 'severity', 'dateOfAbatement', 'diagnosisCertainity', 'diagnosisDescription']
        widgets = {
            'diagnosisName': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Digonosis Name *'}),
            'diagnosisBodySite': forms.TextInput(attrs={'class': 'form-control','placeholder': 'BodySite *'}),
            'dateOfOnset': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder': 'Date of onset *'}),
            'severity': forms.TextInput(attrs={'class': 'form-control','placeholder': 'severity'}),
            'dateOfAbatement': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder': 'Date Of Abatement *'}),
            'diagnosisCertainity': forms.TextInput(attrs={'class': 'form-control','placeholder': 'diagnosisCertainity'}),
            'diagnosisDescription': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Diagnosis Description *'}),
            
        }

    def __init__(self, *args, **kwargs):
        patient = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)
        if patient:
            self.fields['patientId'].widget = forms.HiddenInput()
            self.initial['patientId'] = patient.pk 

class MedicalDeviceForm(forms.ModelForm):
    class Meta:
        model = MedicalDevice
        fields = ['deviceName', 'deviceBodySite', 'deviceUse', 'deviceDescription']
        widgets = {
            'deviceName': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Device Name'}),
            'deviceBodySite': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Body Site'}),
            'deviceUse': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Device Use'}),
            'deviceDescription': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Device Description'}),
        }

    def __init__(self, *args, **kwargs):
        patient = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)
        if patient:
            self.fields['patientId'].widget = forms.HiddenInput()
            self.initial['patientId'] = patient.pk 