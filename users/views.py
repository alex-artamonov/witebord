from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate, login
from django.views.generic import CreateView
from Witebord.settings import AUTHENTICATION_BACKENDS
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import DetailView

from users.forms import BaseRegisterForm
import random

# Create your views here.

class BaseRegisterView(CreateView):
    model = get_user_model()
    form_class = BaseRegisterForm
    success_url = 'ads:home'


def signup(request):
    if request.method == 'POST':
        form = BaseRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.is_active = False
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            code = random.randrange(100000,999999)
            request.session['username1'] = username
            request.session['raw_password'] = raw_password
            request.session['otp1'] = code
            # user = authenticate(username=username, password=raw_password)
            
            print(code)
            # otp = OTP.objects.create(code=code, user=user)
            # user.otp = otp
            body = f"Dear {username}, your OTP for login is {otp.code}. Use this OTP to validate your login."
            send_mail(
                message=body,
                subject='registration at examle.com: OTP request',
                from_email='sat.arepo@yandex.ru',
                recipient_list=[user.email]
            )
            # send_mail('OTP request',body,'email@gmail.com',[username], fail_silently=False)
            messages.success(request, "Your OTP has been send to your email.")
            # login(request, user)
            return redirect('otp_verification')
    else:
        form = BaseRegisterForm()
    return render(request, 'accounts/signup.html', {'form': form})


def otp_verification(request):
    # for i in request.session:
    #     print(i)
    username = request.session['username1']
    print('username:')
    print(username)
    if request.method == "POST":
        otp1 = request.session['otp1']
        otp2 = request.POST.get('otp2')
        print("request.session['otp1']:")
        print(otp1 )
        print(otp2)
        # otp2 = request.POST.get('username')
        # print('otp', otp)
        # user = User.objects.filter(username = username).first()
        user = get_user_model().objects.get(username = username)
        if str(otp2) == str(otp1):
            print('hi from if otp2==otp1')
            messages.success(request, "OTP Success. Please login with your credentials!")
            # user.is_active = True
            print('user.is_authenticated', user.is_authenticated)
            print('user.is_active ', user.is_active)
            login(request, user)
            # user.save()
            print('user.is_authenticated', user.is_authenticated)
            messages.success(request, f' Wecome {username}')
            return redirect("/")
        else:
            print('hi from else')
            messages.error(request, "Wrong OTP!!")
    return render(request, "accounts/otp.html")



