# from django.core.checks import messages
# from django.shortcuts import redirect, render
# from django.http import HttpResponse, response
# from django.contrib.auth.models import User
# import uuid
# from django.contrib import messages
# from .models import *
# from django.contrib.auth import authenticate
# from django.contrib import messages 

# from .middleware import auth_middleware, check_middleware


# @auth_middleware
# def choiseview(request):
#     try:

#         if request.session['role']== "Admin":
#             return render(request, 'choise.html' )
#         else:
#             messages.add_message(request, messages.ERROR, "You Are Not Authenticated")
#             return render(request, 'index.html')
#     except:
#         messages.add_message(request, messages.ERROR, "Something went wrong!!")
#         return render(request, 'index.html')


# @check_middleware
# def doctor_register(request, roledata):
#     try:
#         if request.method =='POST':
#             uname=request.POST.get('uname',None)
#             email=request.POST.get('eml',None)
#             pwd=request.POST.get('pwd',None)

#             if User.objects.filter(username=email).exists():
#                 messages.add_message(request, messages.ERROR, "User Already Exists")
#                 return redirect('')
#             else:
#                 user_obj=User.objects.create(username=email,password=pwd,email=email)
#                 user_obj.set_password(pwd)
#                 user_obj.save()
#                 if roledata == 'Doctor':
#                     role_name = Role.objects.filter(role='Doctor').first()
#                     print(role_name.id)
#                     userRole= UserroleMap.objects.create(user_id=user_obj, role_id=role_name)
#                     userRole.save()
#                     messages.add_message(request, messages.SUCCESS, "Doctor is created")
#                     return redirect('')
#                 else:
#                     role_name = Role.objects.filter(role='Nurse').first()
            
#                     userRole= UserroleMap.objects.create(user_id=user_obj, role_id=role_name)
#                     userRole.save()
#                     messages.add_message(request, messages.SUCCESS, "Nurse is created")

#                     return redirect('')
#         messages.add_message(request, messages.ERROR, "Please Add Valid Details !")
#         return render(request, 'ragister.html')    
#     except Exception as e:
#         print(e)
#         messages.add_message(request, messages.ERROR, "Something Went Wrong!")
#         return render(request, 'index.html')

# @auth_middleware
# def addNurse(request):
#     try:
#         if request.session['role']!= "Admin":
#             messages.add_message(request, messages.ERROR, "You Are Not Authenticated")
#             return render(request, 'index.html')
#         data={'roledata': 'Nurse' , 'message': "Register Nurse"}
#         return  render(request, 'ragister.html', context= data )
#     except:
#         messages.add_message(request, messages.ERROR, "Something Went Wrong!")  
#         return render(request, 'index.html')

# @auth_middleware
# def addDoctor(request):
#     try:
#         if request.session['role']!= "Admin":
#             messages.add_message(request, messages.ERROR, "You Are Not Authenticated")            
#             return render(request, 'index.html')
#         data={'roledata': 'Doctor' , 'message': "Register Doctor"}
#         return  render(request, 'ragister.html', context= data )
#     except:
#         print("nurse2")
#         messages.add_message(request, messages.ERROR, "something went wrong!!")
#         return render(request, 'index.html')


# def docter_login(request):
#     try:
#         if request.method =='POST':
#             email=request.POST.get('eml',None)
#             pwd=request.POST.get('pwd',None)
#             ubj= authenticate(request, username=email, password=pwd) 
#             if ubj == None:
#                 messages.add_message(request, messages.ERROR, "Invalid credentials!")
#                 return redirect('/accounts/loginpage')

#             q = User.objects.filter(username=email).filter(is_staff=True)
#             table1_data= UserroleMap.objects.filter(user_id=ubj.id).first()
#             userRole= Role.objects.filter(id=table1_data.role_id.id).first()
#             request.session["role"]=userRole.role
#             if q and ubj:
#                 messages.add_message(request, messages.SUCCESS, "Welcome Back")
#                 return redirect("")
#             else:
#                 messages.add_message(request, messages.SUCCESS, "Welcome Back")
#                 return redirect("")
#         else:
#             return render(request, 'index.html')
#     except Exception as e:
#         print(e)
#         messages.add_message(request, messages.ERROR, "Something Went Wrong!")
#         return render(request, 'index.html')

# def doctor_logout(request):
#     try:
#         del request.session['role']
#         return redirect('')
#     except:
#         return HttpResponse('<h3 style="text-align:center"> Somthing went wrong !!!!!</h3>')

# In your Django app's views.py

import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('eml')
        password = request.POST.get('pwd')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'doctor':
                return redirect('doctor')  # Redirect to event list if user is an organizer
            elif user.user_type == 'admin':
                return redirect('home')  # Redirect to dashboard if preferences exist
    return render(request, 'login.html')

CustomUser = get_user_model()

@user_passes_test(lambda u: u.user_type == 'admin')  # Ensure only users with user_type 'admin' can access this view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.user_type = 'doctor'  # Set user type to 'doctor'
            user.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'ragister.html', {'form': form})

def logout_view(request):
    logout(request)
    # Redirect to a specific URL after logout
    return redirect('login')


@login_required
def home(request):
    return render(request, 'home.html')

def doctor(request):
    return render(request, 'doctor.html')

def patientlist(request):
    return render(request, 'patientlist.html')

def newpatient(request):
    return render(request, 'newpatient.html')

def patientRecord(request):
    return render(request, 'patientRecord.html')

def viewPatientRecord(request):
    return render(request, 'viewPatientRecord.html')
def OldviewPatientRecord(request):
    return render(request, 'OldviewPatientRecord.html')
def updatePatientRecord(request):
    return render(request, 'updatePatientRecord.html')

def choise(request):
    return render(request, 'choise.html')

def diagnosisPage(request):
    return render(request, 'diagnosisPage.html')

def diagnosisDescription(request):
    return render(request, 'diagnosisDescription.html')
    
def viewMedicine(request):
    return render(request, 'viewMedicine.html')

def labTest(request):
    return render(request, 'labTest.html')

def medicationPage(request):
    return render(request, 'medicationPage.html')

# def pred(request):
#     return render(request, 'pred.html')

# def pred(request):
#     selected_symptoms_str = request.GET.get('selectedSymptoms')
#     selected_symptoms = []
#     if selected_symptoms_str:
#         selected_symptoms = json.loads(selected_symptoms_str)
    

#     # Render the 'pred.html' template and pass the selectedSymptoms as context
#     return render(request, 'pred.html', {'selectedSymptoms': selected_symptoms})


import os
import pickle
import numpy as np

def pred(request):
    # Create an array with 132 items
    headsym = ['itching', 'skin_rash', 'nodal_skin_eruptions',
        'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
        'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting',
        'vomiting', 'burning_micturition', 'spotting_ urination',
        'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets',
        'mood_swings', 'weight_loss', 'restlessness', 'lethargy',
        'patches_in_throat', 'irregular_sugar_level', 'cough',
        'high_fever', 'sunken_eyes', 'breathlessness', 'sweating',
        'dehydration', 'indigestion', 'headache', 'yellowish_skin',
        'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes',
        'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea',
        'mild_fever', 'yellow_urine', 'yellowing_of_eyes',
        'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
        'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision',
        'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure',
        'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
        'fast_heart_rate', 'pain_during_bowel_movements',
        'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus',
        'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity',
        'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes',
        'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties',
        'excessive_hunger', 'extra_marital_contacts',
        'drying_and_tingling_lips', 'slurred_speech', 'knee_pain',
        'hip_joint_pain', 'muscle_weakness', 'stiff_neck',
        'swelling_joints', 'movement_stiffness', 'spinning_movements',
        'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side',
        'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
        'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching',
        'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain',
        'altered_sensorium', 'red_spots_over_body', 'belly_pain',
        'abnormal_menstruation', 'dischromic _patches',
        'watering_from_eyes', 'increased_appetite', 'polyuria',
        'family_history', 'mucoid_sputum', 'rusty_sputum',
        'lack_of_concentration', 'visual_disturbances',
        'receiving_blood_transfusion', 'receiving_unsterile_injections',
        'coma', 'stomach_bleeding', 'distention_of_abdomen',
        'history_of_alcohol_consumption', 'fluid_overload.1',
        'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations',
        'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring',
        'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails',
        'inflammatory_nails', 'blister', 'red_sore_around_nose',
        'yellow_crust_ooze']

    # Get the selected symptoms from the request
    selected_symptoms_str = request.GET.get('selectedSymptoms')
    selected_symptoms = []
    if selected_symptoms_str:
        selected_symptoms = json.loads(selected_symptoms_str)

    # Compare headsym with selected_symptoms array to create new_array_for_model
    new_array_for_model = [1 if symptom in selected_symptoms else 0 for symptom in headsym]

    # Load the saved model
    model_path = os.path.join('/Users/priyankarajbanshi/Documents/new_directory_name/HackathonBackend-main', 'model.pkl')
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        print("Model loaded successfully.")
    except FileNotFoundError:
        model = None
        print("Model not loaded.")

    # Ensure there are 132 values in new_array_for_model
    if len(new_array_for_model) != 132:
        print("Error: new_array_for_model should have 132 values.")
        return HttpResponse("Error: new_array_for_model should have 132 values. ", status=500)

    else:
    # Convert the new_array_for_model into a numpy array
        new_array_for_model = np.array(new_array_for_model).reshape(1, -1)

    # Make a prediction using the loaded model
        prediction = model.predict(new_array_for_model)[0]

    # Render the 'pred.html' template and pass the selected symptoms, predicted disease, and headsym array as context
        return render(request, 'pred.html', {'selectedSymptoms': selected_symptoms, 'predictedDisease': prediction, 'headsym': headsym})

