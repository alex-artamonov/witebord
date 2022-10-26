from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate, login
from django.views.generic import CreateView
from Witebord.settings import AUTHENTICATION_BACKENDS
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect

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
            # user = AUTHENTICATION_BACKENDS(username=username, password=password)
            user = get_user_model().objects.get(username=username, password=password)
            if user is not None:
                user = get_user_model(username=username)
                otp = random.randrange(100000,999999)
                user.customer.otp_code = otp
                user.customer.save()
                request.session['username'] = username
                body = f"Dear {username}, your OTP for login is {otp}. Use this OTP to validate your login."
                send_mail('OTP request',body,'email@gmail.com',[username], fail_silently=False)
                messages.success(request, "Your OTP has been send to your email.")
                return redirect("/otp_verification")
            else:
                messages.error(request, "Wrong Credentials!!")
                return render(request,'account/login.html')
        except:
            messages.error(request, "Please enter email and password for login!")
            return render(request,'account/login.html')
    context={}    
    return render(request, 'account/login.html', context)



def otp_verification(request):
    username = request.session['username']
    if request.method == "POST":
        otp = request.POST.get('username')
        user = get_user_model.objects.get(username = username)
        if otp == user.customer.otp_code:
            messages.success(request, "OTP Success. Please login with your credentials!")
            login(request, user)
            messages.success(request, f' Wecome {username}')
            return redirect("/")
        else:
            messages.error(request, "Wrong OTP!!")
    return render(request, "otpVerification.html")


def signup_first(request):
    username = request['username']
    password = request['password']


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request,
#                                 username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()
#     return render(request, 'account/login.html', {'form': form})

# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             # Create a new user object but avoid saving it yet
#             new_user = user_form.save(commit=False)
#             # Set the chosen password
#             new_user.set_password(
#                 user_form.cleaned_data['password'])
#             # Save the User object
#             new_user.save()
#             # Create the user profile
#             Profile.objects.create(user=new_user)
#             return render(request,
#                           'account/register_done.html',
#                           {'new_user': new_user})
#     else:
#         user_form = UserRegistrationForm()
#     return render(request,
#                   'account/register.html',
#                   {'user_form': user_form})