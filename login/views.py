from django.shortcuts import render, redirect
from django.http import HttpResponse
from web.settings import EMAIL_HOST_USER
import requests
from . import forms
from . import models
import json
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta

# Create your views here.

def home(request):
    url = "http://127.0.0.1:8000/api-token-auth/"
    querystring = {"username": "ashhuu27", "password": "112233"}
    headers = {
        'x-rapidapi-host': "gurubrahma-smsly-sms-to-india-v1.p.rapidapi.com",
        'x-rapidapi-key': "0f613269e2msh5fc467929a8d0edp11181ejsn5fb72d7062f1"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    return HttpResponse("Dashboard")

def register(request):
    if request.COOKIES.get('token'):
        return redirect('Dashboard')
    else:
        error = ""
        token = ""
        if request.method == 'POST':
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                ename = models.UserDetails.objects.filter(username=data['username']).exists()
                ephone = models.UserDetails.objects.filter(phone=data['phone']).exists()
                emaile = models.UserDetails.objects.filter(email=data['email']).exists()
                data['ref'] = "None"
                data['perms'] = 7
                data['role'] = "Master"
                data['team'] = "Head"
                # Basic Form Validations
                if data['password'] != data['password2']:
                    error = "Password did not match"
                elif ename == True:
                    error = "The username is already registered"
                elif ephone == True:
                    error = "Number already registered, please enter another number"
                elif emaile == True:
                    error = "The email is already registered"
                elif len(data['phone']) != 10:
                    error = "The phone number should be of 10 digits"
                else:
                    # url = "https://gurubrahma-smsly-sms-to-india-v1.p.rapidapi.com/otp/generate/" + data['phone']
                    # querystring = {"getOTP": "true", "duration": "1000", "digits": "4",
                    #                "message": "Your verification code is OTP_VALUE"}
                    # headers = {
                    #     'x-rapidapi-host': "gurubrahma-smsly-sms-to-india-v1.p.rapidapi.com",
                    #     'x-rapidapi-key': "0f613269e2msh5fc467929a8d0edp11181ejsn5fb72d7062f1"
                    # }
                    # data['password'] = make_password(data['password'])
                    # response = requests.request("GET", url, headers=headers, params=querystring)
                    # temp = response.text
                    # res = json.loads(temp)
                    # otp = res['OTP']
                    otp = 2234
                    data['password'] = make_password(data['password'])
                    html1 = redirect('verifyOTP')
                    html1.set_cookie('form', data)
                    html1.set_cookie('otp', otp)
                    return html1
        else:
            form = forms.RegisterForm()
    return render(request, 'login/index.html', {'form': form, 'error': error, 'token': token})


def verifyOTP(request):
    error = ""
    data = request.COOKIES.get('form')
    otp = request.COOKIES.get('otp')
    html = redirect('Dashboard')
    html.delete_cookie('form')
    html.delete_cookie('otp')
    print(data)
    if request.method == 'POST':
        form = forms.OTP(request.POST)
        if form.is_valid():
            userotp = form.data['otp']
            print(userotp)
            print(otp)
            if userotp == otp:
                data4 = eval(data)
                r = requests.post('http://127.0.0.1:8000/api/token/', data=data4)
                print(r)
                text = r.json()
                print(text)
                token = text['token']
                # Adding Token to UserDetails
                query = models.UserDetails.objects.get(username=data4['username'])
                query.token = token
                query.save()
                # Setting Redirect and adding token to cookies
                html.set_cookie('token', token)
                # sendWelcomeEmail(data4)
                return html
            else:
                error = "Incorrect OTP"
    else:
        form = forms.OTP()
    return render(request, 'login/verify.html', {'form': form, 'error': error})

def sendWelcomeEmail(data):
    subject = 'Welcome to our website, ' + data['name']
    receiver = data['email']
    print(EMAIL_HOST_USER + " " + data['email'] + " " + data['name'])
    message = 'Hope you have a nice stay!'
    send_mail(subject, message, EMAIL_HOST_USER, [receiver], fail_silently=False)

def sendForgotEmail(data, token):
    subject = 'Seems like you have forgot your password, ' + data['username']
    receiver = data['email']
    print(EMAIL_HOST_USER + " " + data['email'] + " " + data['username'])
    url = 'http://127.0.0.1:8000/activate/' + token + '/' + data['token']
    message = 'Your reset link is as follows: ' + url
    send_mail(subject, message, EMAIL_HOST_USER, [receiver], fail_silently=False)
    return True

def login(request):
    if request.COOKIES.get('token'):
        tokenConfirm = request.COOKIES.get('token')
        return redirect('Dashboard')
    else:
        error = ""
        if request.method == 'POST':
            form = forms.LoginForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                checkUser = models.UserDetails.objects.filter(username=data['name']).exists()
                if checkUser == True:
                    query = models.UserDetails.objects.filter(username=data['name']).values()
                    row = query[0]
                    check = check_password(data['password'], row['password'])
                    print(check)
                    if check == True:
                        r = requests.post('http://127.0.0.1:8000/api/gentoken/', data=data)
                        text = r.json()
                        token = text['token']
                        query = models.UserDetails.objects.get(username=data['name'])
                        query.token = token
                        query.save()
                        html = redirect('Dashboard')
                        html.set_cookie('token', token)
                        return html
                    else:
                        error = "Username and password does not match"
                else:
                    error = "The user does not exist"

        else:
            form = forms.LoginForm()
    return render(request, 'login/login.html', {'form': form, 'error': error})

def logout(request):
    if request.COOKIES.get('token'):
        token = request.COOKIES.get('token')
        html = redirect('Login')
        html.delete_cookie('token')
        r = requests.post('http://127.0.0.1:8000/api/verify/', data={'token': token})
        text = r.json()
        check = text['exists']
        if check == 'true':
            print("Successfully Deleted Cookies and Logged out")
        elif check == 'false':
            print("Could not find verified token")
        return html
    else:
        print("Could not find any token")
        return redirect('Login')


def activate(request, token, ptoken):
    checkuser = models.UserDetails.objects.filter(token=ptoken).exists()
    checktoken = models.ResetTokens.objects.filter(token=token).exists()
    status = models.ResetTokens.objects.get(token=token)
    if status.status == 0:
        return HttpResponse("Link Expired")
    validity = tokenValidity(token)
    if validity == False:
        status.status = 0
        status.save()
        return HttpResponse("Link Expired")
    if checkuser == True and checktoken == True:
        details = models.UserDetails.objects.get(token=ptoken)
        pr = PasswordResetTokenGenerator()
        check = pr.check_token(details, token)
        if check == True:
            html1 = redirect('resetPassword')
            html1.set_cookie('tempdata', ptoken)
            return html1
        else:
            return HttpResponse("Reset token invalid or expired. Please try resetting password again")
    else:
        return HttpResponse("Invalid Request: User or Token not found")


def resetPassword(request):
    if request.method == 'POST':
        form = forms.ResetPass(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if request.COOKIES.get('tempdata'):
                token = request.COOKIES.get('tempdata')
                form = forms.ResetPass()
                html = render(request, 'login/reset.html', {'form': form})
                html.delete_cookie('tempdata')
                details = models.UserDetails.objects.get(token=token)
            else:
                return redirect('Login')
            if data['password'] == data['confirm']:
                details.password = make_password(data['password'])
                details.save()
            elif data['password'] != data['confirm']:
                error = "password does not match"
                html = render(request, 'login/reset.html', {'form': form, 'error': error})
    else:
        form = forms.ResetPass()
        html = render(request, 'login/reset.html', {'form': form})
    return html


def forgot(request):
    error = ""
    title = "Recover Password"
    if request.method == 'POST':
        form = forms.ForgotPass(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            checkEmail = models.UserDetails.objects.filter(email=email).exists()
            if checkEmail == True:
                data = models.UserDetails.objects.filter(email=email).values()
                user = models.UserDetails.objects.get(email=email)
                pr = PasswordResetTokenGenerator()
                resetToken = pr.make_token(user)
                print("This is " + resetToken)
                checkToken = models.ResetTokens.objects.filter(token=resetToken).exists()
                if checkToken == True:
                    dataToken = models.ResetTokens.objects.get(token=resetToken)
                    dataToken.status = 1
                    dataToken.time = datetime.now()
                    dataToken.save()
                else:
                    tokenAdd = models.ResetTokens(token=resetToken, status=1, time=datetime.now())
                    tokenAdd.save()
                details = data[0]
                print(details)
                state = sendForgotEmail(details, resetToken)
                if state == True:
                    title = "Reset link set"
                else:
                    title = "Error sending email"
            else:
                error = "The Email does not exist"
    else:
        form = forms.ForgotPass()
    return render(request, 'login/forgot.html', {'form': form, 'error': error, 'title': title})


def dashboard(request):
    if request.COOKIES.get('token'):
        tokenConfirm = request.COOKIES.get('token')
        r = requests.post('http://127.0.0.1:8000/api/verify/', data={'token': tokenConfirm})
        text = r.json()
        check = text['exists']
        if check == 'true':
            print("Successfully Deleted Cookies and Logged out")
            details = models.UserDetails.objects.get(token=tokenConfirm)
            user = details.username
            email = details.email
        elif check == 'false':
            redirect('404')
        print(check)
    else:
        return redirect('404')
    return render(request, 'login/dashboard.html', {'user': user, 'email': email})

def error404(request):
    return render(request, 'login/404.html', {})

def delete(request):
    ud = models.UserDetails()
    ud.delete_everything()
    return HttpResponse("Deleted")

def tokenValidity(token):
    data = models.ResetTokens.objects.filter(token=token).values()
    validTime = (data[0])['time']
    datenow = datetime.now()
    timeAdd = validTime + timedelta(minutes=15)
    if validTime.date() < datenow.date():
        print("Token Expired - Date Changed")
        return False
    else:
        if datenow.time() > timeAdd.time():
            print("It is more than 15 minutes")
            return False
    return True
