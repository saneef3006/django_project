from django.shortcuts import render, get_object_or_404, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
import re

from studentlogin.models import User
# Create your views here.

def index(request):
    if request.session.has_key('username'):
        username = request.session['username']
        if checkIfUserExists(username):
            user = User.objects.get(user_name=username)
            context = {'user': user}
            return render(request, 'studentlogin/dashboard.html',context)
        else:
            if request.session.has_key('username'):
                del request.session['username']    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if checkIfUserExists(username):
            passwordMismatch = checkForPasswordMismatch(username, password)
            if passwordMismatch:
                context = {'error_message': 'Incorrect username or password'}
                return render(request, 'studentlogin/index.html', context)
            else:
                user = User.objects.get(user_name=username)
                context = {'user': user}
                request.session['username'] = user.user_name
                return render(request, 'studentlogin/dashboard.html',context)
        else:
            context = {'error_message': 'Incorrect username or password'}
            return render(request, 'studentlogin/index.html', context)
    else:
        return render(request, 'studentlogin/index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')
        context = {}
        if not validateEmail(email):
            context['error_message'] = 'Invalid email address'
            return render(request, 'studentlogin/register.html', context)
        if not validatePhoneNumber(phone):
            context['error_message'] = 'Invalid phone number'
            return render(request, 'studentlogin/register.html', context)
        if checkIfUserExists(username):
            context['error_message'] = 'Username already taken.'
            return render(request, 'studentlogin/register.html', context)
        else:
            addUser(username, password, phone, email, image)
            sendMail(email)
            context['success_message'] = 'User created successfully.'
            return render(request, 'studentlogin/register.html', context)

    else:
        return render(request, 'studentlogin/register.html')

def logout(request):
    if request.session.has_key('username'):
        del request.session['username']
    return render(request, 'studentlogin/logout.html')

def validateEmail(email):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def validatePhoneNumber(phone):
    validPhone = re.match(r'^[789]\d{9}$', phone)
    if validPhone is None:
        return False
    else:
        return True

def checkIfUserExists(username):
    try:
        user = User.objects.get(user_name=username)
        return True
    except User.DoesNotExist:
        return False

def checkForPasswordMismatch(username, password):
    user = User.objects.get(user_name=username)
    if user.password == password:
        return False
    else:
        return True

def addUser(username, password, phoneNumber, email, image):
    user = User(user_name=username, password=password, phone=phoneNumber, email=email, image=image)
    user.save()

def sendMail(email):
    subject = 'Student App Admin'
    body = 'Congragulations! You have been added to the student app site.'
    emailObj = EmailMessage(subject, body, to=[email])
    emailObj.send()
