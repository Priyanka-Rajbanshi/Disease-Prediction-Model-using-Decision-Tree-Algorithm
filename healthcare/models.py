import datetime
import random
from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
# Create your models here.
class Patient(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    name = models.CharField(max_length=150, null=False)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=False,blank=False,unique=True)
    registrationNumber = models.CharField(max_length=50, unique=True)
    bloodGroup = models.CharField(max_length=10, null=False)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dateOfBirth = models.DateField(null=False)

    def __str__(self):
        return str(self.name)

    
    def save(self, *args, **kwargs):
        if not self.registrationNumber:  # Generate registration number if not provided
            self.registrationNumber = self.generate_registration_number()
        super().save(*args, **kwargs)

    def generate_registration_number(self):
        # Logic to generate a unique registration number
        # Here, I'm generating a random number as an example
        return ''.join(random.choices('0123456789', k=10))

class PatientRecord(models.Model):
    ALCOHOL_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )

    DIBETIC_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )

    SMOKE_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )

    STATUS_CHOICES = (
        ('recovered', 'Pending'),
        ('undertreament', 'Under Treatment'),
    )
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    bloodPressure = models.CharField(max_length=50)
    pulseRate = models.CharField(max_length=50)
    bodyTemprature = models.CharField(max_length=50)
    alcohol = models.CharField(max_length=5, choices=ALCOHOL_CHOICES)
    smoke = models.CharField(max_length=5, choices=SMOKE_CHOICES)
    diabetic = models.CharField(max_length=5, choices=DIBETIC_CHOICES)
    allergies = models.TextField(null=True)
    insurancePlanName = models.CharField( max_length=100,null=True)
    insurancePlanNumber = models.CharField( max_length=50, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    

    def __str__(self):
        return str(self.height)


class Symptom(models.Model):
    name = models.CharField(max_length=100)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='symptoms')

    def __str__(self):
        return self.name
