from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.conf import settings
import socket
socket.getaddrinfo('localhost', 8080)
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .forms import UserLoginForm
from blog import views as blog_views
from django.contrib.auth.views import LogoutView
#New token libraries
from datetime import datetime, timedelta
import cryptography
from cryptography.fernet import Fernet
from django.contrib import admin


FERNET_KEY = 'H-gvBa31So7ZWRlIleY7q5xYPIytGnRHRcBpRbASyao='
fernet = Fernet(FERNET_KEY)
DATE_FORMAT = '%Y-%m-%d %H-%M-%S'
EXPIRATION_DAYS = 1

def _get_time():
    """Returns a string with the current UTC time"""
    return datetime.utcnow().strftime(DATE_FORMAT)

def _parse_time(d):
    """Parses a string produced by _get_time and returns a datetime object"""
    return datetime.strptime(d,DATE_FORMAT)

def generate_token(text):
    """Generates an encrypted token"""
    full_text = text + '|' + _get_time()
    a=type(full_text)
    b=type(_get_time())
    token = fernet.encrypt(bytes(full_text, 'utf8'))
    return token


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save(commit=False)
            user.is_active= False
            user.save()
            current_site = get_current_site(request)
            username = form.cleaned_data.get('username')
            mail_subject = 'Activate your account.'

            message = render_to_string('../templates/users/acc_active_email.html',{
                'user' : user,
                'domain' : current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)).decode() ,
                #'token': account_activation_token.make_token(user),
                'token': generate_token(username),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject,message, to=[to_email]
            )
            email.send()
            return HttpResponse('Confirm your email to complete registration')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        print("inside try")
        value =fernet.decrypt(bytes(token, 'utf8'))
        separator_pos = value.rfind('|')
        print('value........................',value)
        text = value[: separator_pos]
        print('text.........................', text)
        token_time = _parse_time(value[separator_pos + 1: ])

        if token_time + timedelta(EXPIRATION_DAYS) < datetime.utcnow():   
              
            print("inside if----------------------------------------------------")     
            display_message="Thank you for your email confirmation. You can login to your account from"
            return render(request, 'thankyou.html', {'display_message': display_message})
              
        else:
            return HttpResponse('Token has Expired')   

    except cryptography.fernet.InvalidToken:
        return HttpResponse('Invalid Token')

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        
        if form.is_valid():
            return render(request, 'blog_views.post_list')
        else:
            return HttpResponse('Incorrect credentials')
        # return form with entered data, display messages at the top
    else:
        form = UserLoginForm(request.POST)
    return render(request, 'users/login.html', {'form': form})

def thankyou(request, msg):

    return render(request, 'thankyou', {'msg': msg})

    
    
