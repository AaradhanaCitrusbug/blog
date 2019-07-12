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
                'token': account_activation_token.make_token(user),
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
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request)
        # return redirect('home')
        display_message="Thank you for your email confirmation. You can login to your account from"
        
        return render(request, 'users/thankyou.html', {'display_message': display_message,
                                                    'user': user})
    else:
        return HttpResponse('Activation link is invalid!')

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        
        if form.is_valid:
            data = request.POST.copy()
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username, password)
        
        if user is not None:
            return render(request, 'blog_views.post_list')
        else:
            return HttpResponse('Incorrect credentials')
        # return form with entered data, display messages at the top
    else:
        form = UserLoginForm(request.POST)
    return render(request, 'login', {'form': form})
    
    
