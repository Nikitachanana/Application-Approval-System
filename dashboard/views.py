from django.shortcuts import render, redirect
# from .forms import SignUp, SignIn, AdminReg, Edit
from .forms import AdminReg, Edit, UserForm, Remark
# from .models import UserDetails, Session
from login.models import UserDetails, Details
import ast
import requests
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
#
#
# # Create your views here.
#

def hello(request):
    return HttpResponse("Hello")

#
# def registerView(request):
#     html = "Registration Form"
#     check = ""
#     if request.method == 'POST':
#         form = SignUp(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['Aname']
#             email = form.cleaned_data['Aemail']
#             phone = form.cleaned_data['Aphone']
#             user = form.cleaned_data['Auser']
#             password = form.cleaned_data['Apass']
#             role = "primary"
#             status = 1
#             perms = 7
#             ref = "Master"
#             userCheck = UserDetails.objects.filter(adminUser=user).exists()
#             emailCheck = UserDetails.objects.filter(adminEmail=email).exists()
#             ph = str(phone)
#             if userCheck == True:
#                 check = "The username exists already. Use a different one"
#             elif emailCheck == True:
#                 check = "The phone number is not valid. Enter a 10 digit phone number"
#             elif len(ph) != 10:
#                 check = "The phone number is not valid. Enter a 10 digit phone number"
#             else:
#                 html = "Thank you for registering! You can login now"
#                 passwordSave = make_password(password)
#                 check = ""
#                 userDetails = UserDetails(
#                     adminName=name.strip(),
#                     adminEmail=email.strip(),
#                     adminPhone=ph,
#                     adminUser=user.strip(),
#                     adminPass=passwordSave.strip(),
#                     adminRole=role,
#                     adminStatus=status,
#                     adminPerms=perms,
#                     adminRef=ref)
#                 userDetails.save()
#     else:
#         form = SignUp()
#     return render(request, 'user/register.html', {'html': html, 'form': form, 'check': check})
#
#
# def loginView(request):
#     sessionCheck = Session.objects.filter(sessionStat=1).exists()
#     text = ""
#     if sessionCheck == True:
#         return HttpResponseRedirect('dashboard/')
#     else:
#         if request.method == 'POST':
#             form = SignIn(request.POST)
#             if form.is_valid():
#                 email = form.cleaned_data['Lemail']
#                 password = form.cleaned_data['Lpass']
#
#                 emailCheck = UserDetails.objects.filter(adminEmail=email).exists()
#                 if emailCheck != True:
#                     text = "The email does not exist in the database"
#                 else:
#                     b = UserDetails.objects.get(adminEmail=email)
#                     passCheck = check_password(password, b.adminPass)
#                     if passCheck == False:
#                         text = "The email and password does not match"
#                     else:
#                         import datetime
#                         b = UserDetails.objects.get(adminEmail=email)
#                         now = datetime.datetime.now()
#                         ses = Session.objects.create(sessionID=b, sessionStat=1, sessionIn=now)
#                         return HttpResponseRedirect('/dashboard/')
#         else:
#             form = SignIn()
#     return render(request, 'user/login.html', {'html': text, 'form': form})
#
#
def dashboardView(request):
    sessionCheck = authenticate(request)
    if sessionCheck == "true":
        token = request.COOKIES.get('token')
        user = UserDetails.objects.get(token=token)
    text = ''
    if sessionCheck == False:
        return HttpResponseRedirect('/error404')
    return render(request, 'user/dashboard.html', {'user': user})
#
#
def errorView(request):
    text = "You are not authorized to access this page. Please login."
    return render(request, 'user/404.html', {'html': text})

#
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

def authenticate(request):
    if request.COOKIES.get('token'):
        tokenConfirm = request.COOKIES.get('token')
        r = requests.post('http://127.0.0.1:8000/api/verify/', data={'token': tokenConfirm})
        text = r.json()
        check = text['exists']
    return check
#
#
def adminRegister(request):
    sessionCheck = authenticate(request)
    if sessionCheck == "false":
        return HttpResponseRedirect('/error404')
    else:
        temp = UserDetails.objects.get(token=request.COOKIES.get('token'))
        perms = 0
        html = "Make a User Account"
        check = ""
        if request.method == 'POST':
            form = AdminReg(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                data['role'] = "secondary"
                data['status'] = 1
                data['ref'] = temp.name + " (" + temp.username + ")"
                userCheck = UserDetails.objects.filter(username=data['username']).exists()
                emailCheck = UserDetails.objects.filter(email=data['email']).exists()
                for i in data['perms']:
                    perms = perms + int(i)
                data['perms'] = perms
                ph = str(data['phone'])
                if userCheck == True or emailCheck == True or len(ph) != 10:
                    if userCheck == True:
                        check = "The username exists already. Use a different one"
                    elif emailCheck == True:
                        check = "The email exists already. Use a different one"
                    elif len(ph) != 10:
                        check = "The phone number is not valid. Enter a 10 digit phone number"
                else:
                    data['password'] = make_password(data['password'])
                    r = requests.post('http://127.0.0.1:8000/api/token/', data=data)
                    text = r.json()
                    token = text['token']
                    print("Token is as follows: ", token)
                    query = UserDetails.objects.get(username=data['username'])
                    query.token = token
                    query.save()
                    check = ""
                    html = "Thank you for registering! You can login now"
        else:
            form = AdminReg()
    return render(request, 'user/account.html', {'html': html, 'form': form, 'check': check, 'admin':temp})
#
#
def deleteView(request, user):
    sessionCheck = authenticate(request)
    check2 = ''
    if sessionCheck == "false":
        return HttpResponseRedirect('/error404')
    else:
        current_user = UserDetails.objects.get(token=request.COOKIES.get('token'))
        if request.method == 'POST':
            edit = Edit(request.POST)
            if edit.is_valid():
                # check2 = editForm(edit)
                pass
        details = UserDetails.objects.filter()
        check = UserDetails.objects.get(username=user)
        if check.role == "secondary" and current_user.perms > 4:
            check.status = 0
            check.save()
            value = 1
        else:
            value = 0
    return redirect('DetailsV', value=value)
    return render(request, 'user/details.html', {'forms': details, 'value': value, 'check': check2})
#
def editView(request, user):
    check = ''
    sessionCheck = authenticate(request)
    if sessionCheck == "false":
        return HttpResponseRedirect('/error404')
    else:
        current_user = UserDetails.objects.get(token=request.COOKIES.get('token'))
        details = UserDetails.objects.filter()
        check = UserDetails.objects.get(username=user)
        if check.role == "secondary" and current_user.perms > 4:
            check.delete()
            value = 1
            return redirect('DetailsV', value=value)
        else:
            value = 0
            return redirect('DetailsV', value=value)
    return render(request, 'user/details.html', {'forms': details, 'value': value})
#
def editForm(edit, current_user):
    user = edit.cleaned_data['Eusername']
    name = edit.cleaned_data['Ename']
    email = edit.cleaned_data['Eemail']
    phone = edit.cleaned_data['Ephone']
    # user = edit.cleaned_data['Euser']
    password = edit.cleaned_data['Epass']
    choice = edit.cleaned_data['Eperms']
    team = edit.cleaned_data['Eteam']
    row = UserDetails.objects.get(username=user)
    enPass = make_password(password)
    perms = 0
    for i in choice:
        perms = perms + int(i)
    emailCheck = UserDetails.objects.filter(email=email).exists()
    ph = str(phone)
    if row.role == "Master" and current_user.perms > 4:
        check = "You are not authorized to edit this user"
    elif current_user.role == "secondary":
        check = "You are not allowed to edit as a secondary user"
    elif emailCheck == True:
        check = "The email is registered already"
    elif len(ph) != 10:
        check = "The phone number is not valid. Enter a 10 digit phone number"
    else:
        row.name = name
        row.email = email
        row.phone = phone
        row.user = user
        row.password = enPass
        row.perms = perms
        row.team = team
        row.save()
        check = "1"
    return check


def adminDetails(request, value=None):
    check = ''
    sessionCheck = authenticate(request)
    if sessionCheck == "false":
        return HttpResponseRedirect('/error404')
    else:
        current_user = UserDetails.objects.get(token=request.COOKIES.get('token'))
        if current_user.role != "Master":
            return HttpResponseRedirect('/error404')
        details = UserDetails.objects.all()
        edit = Edit()
        if request.method == 'POST':
            edit = Edit(request.POST)
            if edit.is_valid():
                check = editForm(edit, current_user)
                if check == 1:
                    value = "1"
        html = "Changed"
    print("Value =", value)
    return render(request, 'user/details.html', {'html': html, 'forms': details, 'editForm': edit,
                                                 'check': check, 'value': value, 'admin': current_user})

#Approve Request


def approveView(request):
    sessionCheck = authenticate(request)
    if sessionCheck == "false":
        return HttpResponse("Error 404")
    else:
        current_user = UserDetails.objects.get(token=request.COOKIES.get('token'))
        print(current_user)
        # if current_user.role == "Master":
        #     return redirect("AdminApproval")
        rowApprove = Details.objects.filter(uid=current_user.pk, status=1).values()
        rowPending = Details.objects.filter(uid=current_user.pk, status=0).values()
        rowDisapproved = Details.objects.only('admin1', 'requestId').values()
        disapprovedList = []
        for i in rowDisapproved:
            if i['admin1'] != '':
                dictCheck = ast.literal_eval(i['admin1'])
                for j in dictCheck:
                    if j == current_user.username:
                        if dictCheck[j] == "Disapproved":
                            disapprovedList.append(i['requestId'])
        print("List is", disapprovedList)
        pendingList = newList(rowPending)
        approvedList = newList(rowApprove)
        details = Details.objects.all()
        check = False
        remark = Remark()
        for i in details:
            if i.approve < 3:
                check = True
        if request.method == "POST":
            form = UserForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data['title']
                picture = form.cleaned_data['picture']
                description = form.cleaned_data['description']
                details = Details(uid=current_user, title=title, picture=picture, description=description, status=0, approve=0, remark="")
                details.save()
        else:
            form = UserForm()
    return render(request, "user/approval.html", {'form': form, 'approved': approvedList,
                                                  'pending': pendingList, 'details': details,
                                                  'check': check, 'remark': remark, 'admin':current_user,
                                                  'disapproved': disapprovedList})

def approve(request, id, email):
    row = Details.objects.get(requestId=id)
    current_user = UserDetails.objects.get(email=email)
    print("Working")
    if request.method == 'POST':
        admin = {}
        if 'Approve' in request.POST:
            row.approve += 1
            if row.approve == 3:
                row.status = 1
            if row.admin1 is None or row.admin1 is "":
                admin.update({current_user.username: "Approved"})
                row.admin1 = admin
            else:
                dict = ast.literal_eval(row.admin1)
                dict.update({current_user.username: "Approved"})
                row.admin1 = dict
        if 'Disapprove' in request.POST:
            row.disapprove += 1
            if row.disapprove == 3:
                row.status = -1
            if row.admin1 is None or row.admin1 is "":
                admin.update({current_user.username: "Disapproved"})
                row.admin1 = admin
            else:
                dict = ast.literal_eval(row.admin1)
                dict.update({current_user.username: "Disapproved"})
                row.admin1 = dict
        remarks = {}
        remark = Remark(request.POST)
        print("Remark is", remark)
        if remark.is_valid():
            print("Valid", remark.cleaned_data['remark'])
            if row.remark is None or row.remark is "" or row.remark == []:
                print("Is None")
                remarks.update({current_user.username: remark.cleaned_data['remark']})
                entry = remarks
                row.remark = entry
                row.save()
            else:
                dict = eval(str(row.remark))
                dict.update({current_user.username: remark.cleaned_data['remark']})
                entry = dict
                row.remark = entry
                row.save()
    return redirect('Approval')

def unapprove(request, id, email):
    obj1 = Details.objects.get(requestId=id)
    current_user = UserDetails.objects.get(email=email)
    detect = ast.literal_eval(obj1.admin1)
    detect.pop(current_user.username)
    remark = ast.literal_eval(obj1.remark)
    remark.pop(current_user.username)
    if len(remark) < 1:
        obj1.remark = ""
    else:
        obj1.remark = remark
    if len(detect) < 1:
        obj1.admin1 = ""
    else:
        obj1.admin1 = detect
    obj1.approve -= 1
    obj1.save()
    return redirect('Approval')

def newList(rawdata):
    pendingList = []
    for i in rawdata:
        tempdic = i
        if i['remark'] is not "":
            remarks = ast.literal_eval(i['remark'])
            smalllist = []
            for remark in remarks:
                smalllist.append(remarks[remark])
            tempdic.update({'remarks': smalllist})
        pendingList.append(tempdic)
    return pendingList