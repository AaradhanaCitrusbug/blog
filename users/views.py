from django.shortcuts import render,redirect
from .forms import UserRegisterForm
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
from .models import user_details
from django.utils import timezone
import base64
import pytz

utc=pytz.UTC
#FERNET_KEY = 'H-gvBa31So7ZWRlIleY7q5xYPIytGnRHRcBpRbASyao='
#fernet = Fernet(FERNET_KEY)
DATE_FORMAT = '%Y-%m-%d %H-%M-%S'
EXPIRATION_DAYS = 1

def _get_time():
    """Returns a string with the current UTC time"""
    #return datetime.utcnow().strftime(DATE_FORMAT)
    return datetime.utcnow()

# def _parse_time(d):
#     """Parses a string produced by _get_time and returns a datetime object"""
#     return datetime.strptime(d,DATE_FORMAT)

def generate_token(text):
    """Generates an encrypted token"""
    full_text = text
    #token = fernet.encrypt(bytes(full_text, 'utf8'))
    #full_text = full_text.encode("utf-8")
    #token = base64.b64encode(full_text)
    #token=base64.encodestring(full_text)
    token = base64.b64encode(bytes(full_text, 'utf-8'))
    print(token)
    print(token.decode("utf-8") )
    return token.decode("utf-8")

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save(commit=False)
            user.is_active= False
            user.save()
            #print(user)
            current_site = get_current_site(request)
            entered_username = form.cleaned_data.get('username')
            mail_subject = 'Activate your account.'

            b = user_details(user=user, mail_sent_time=timezone.now())
            b.save()
            message = render_to_string('../templates/users/acc_active_email.html',{
                'user' : user,
                'domain' : current_site.domain,
                #'token': account_activation_token.make_token(user),
                'token': generate_token(entered_username),
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


def activate(request, b64_string):
    try:
        print("INSIDE TRY BLOCK")
        #value =fernet.decrypt(bytes(token, 'utf8'))
        #value = base64.b64decode(token)
        #value = temp.decode("utf-8")
        #value= base64.decodestring(token)
        #value = base64.b64encode(bytes(full_text, 'utf-8'))
        value = base64.b64decode(b64_string)
        print("value",value.decode("utf-8"))
        user_object = user_details.objects.get(user__username=value.decode("utf-8"))
        sent_time = user_object.mail_sent_time
        sent_time_date=sent_time.date()
        sent_time_time=sent_time.time()
        oneday=timedelta(EXPIRATION_DAYS)
        today= datetime.utcnow()
        sent_time = utc.localize(sent_time) 
        today = utc.localize(today) 
        
        #if sent_time + timedelta(EXPIRATION_DAYS) < datetime.utcnow():
        if sent_time + timedelta(days=1)  < today:
            b = user_details(status=True)
            b.save()
            display_message="Thank you for your email confirmation. You can login to your account from"
            return render(request, 'thankyou.html', {'display_message': display_message})             
        else:
            return HttpResponse('Token has Expired')   

    except cryptography.fernet.InvalidToken:
        print("INSIDE EXCEPT BLOCK")
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

    
    
