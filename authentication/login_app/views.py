from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Employee

import random
from django.core.mail import send_mail
from django.conf import settings


def indexView(request):
    return render(request, 'index.html')


def loginView(request):
    return render(request, 'authentication/login.html')


def verifyView(request):

    username = request.POST['username']
    password = request.POST['password']

    print(username, password)

    emp = Employee.objects.filter(email_id=username, password=password)

    if emp:

        # generate random nubmer of 6 digits
        #otp = random.randint(100000, 999999)
        otp = settings.OTP

        # send email with otp
        subject = 'Welcome to Jumanji'
        message = 'Here is your otp to login to\
            Employee Management System. OTP : {}'.format(otp)

        recepient = emp[0].email_id

        # send_mail(subject, message, settings.EMAIL_HOST_USER,
        #          [recepient], fail_silently=False)

        context = {}
        context['otp'] = otp
        return render(request, 'authentication/verify_user.html', context)
    else:
        return redirect('login/')


def dashboardView(request):

    user_otp = request.POST['otp']

    if int(user_otp) == settings.OTP:
        return render(request, 'dashboard.html')
    else:
        return redirect('/login')


def registerView(request):

    return render(request, 'authentication/register.html')


def userregistrationView(request):

    print('bbc')

    if request.method == 'POST':
        email_id = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        mobile = int(request.POST['mobile'])

        e = Employee()

        e.email_id = email_id
        e.name = name
        e.password = password
        e.mobile_number = mobile
        e.save()

        return redirect('/login')

    else:
        return redirect('')
