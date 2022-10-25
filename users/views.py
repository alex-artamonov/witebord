from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from Witebord.settings import AUTHENTICATION_BACKENDS
from django.core.mail import send_mail

from users.forms import BaseRegisterForm
import random

# Create your views here.

class BaseRegisterView(CreateView):
    model = get_user_model()
    form_class = BaseRegisterForm
    success_url = 'ads:home'


def loginUser(request): 
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = AUTHENTICATION_BACKENDS(username=username, password=password)
            if user is not None:
                user = User.objects.get(username=username)
                otp= random.randrange(100000,999999)
                user.customer.otp_code = otp
                user.customer.save()
                request.session['username'] = username
                body = f"Dear {username}, your OTP for login is {otp}. Use this OTP to validate your login."
                send_mail('OTP request',body,'email@gmail.com',[username], fail_silently=False)
                messages.success(request, "Your OTP has been send to your email.")
                return redirect("/otp_verification")
            else:
                messages.error(request, "Wrong Credentials!!")
                return render(request,'login.html')
        except:
            messages.error(request, "Please enter email and password for login!")
            return render(request,'login.html')
    context={}    
    return render(request, "login.html", context)
