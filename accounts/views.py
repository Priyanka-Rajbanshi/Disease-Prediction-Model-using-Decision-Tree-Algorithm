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

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save the form data without committing to the database yet
            user.password = make_password(form.cleaned_data['password'])  # Explicitly hash the password
            user.save()  # Now save the user with the hashed password
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

# def pred(request):
#     return render(request, 'pred.html')

def pred(request):
    selected_symptoms_json = request.GET.get('selectedSymptoms')
    selected_symptoms = json.loads(selected_symptoms_json) if selected_symptoms_json else []
    context = {
        'selectedSymptoms': selected_symptoms,
    }
    print("inside pred function: ", selected_symptoms)
    return render(request, 'pred.html', context)

