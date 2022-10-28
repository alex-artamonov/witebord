from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate, login
from django.views.generic import CreateView

# from Witebord.settings import AUTHENTICATION_BACKENDS
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import DetailView
import random

from .models import User
from users.forms import BaseRegisterForm


# Create your views here.

# class BaseRegisterView(CreateView):
#     model = get_user_model()
#     form_class = BaseRegisterForm
#     success_url = 'ads:home'


def signup(request):
    if request.method == "POST":
        form = BaseRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            code = random.randrange(100000, 999999)
            request.session["username1"] = username
            request.session["raw_password"] = raw_password
            request.session["otp1"] = code
            user = authenticate(username=username, password=raw_password)
            body = f"Уважаемый/ая {username}, одноразовый код для регистрации: {code}. Введите его в форму на сайте."
            send_mail(
                message=body,
                subject="Регистрация на сайте examle.com: запрос одноразового пароля",
                from_email="sat.arepo@yandex.ru",
                recipient_list=[user.email],
            )

            return redirect("otp_verification")
        else:
            messages.error(request, "Ошибка регистрации")
    else:
        form = BaseRegisterForm()
    return render(request, "account/signup.html", {"form": form})


def otp_verification(request):

    username = request.session["username1"]
    if request.method == "POST":
        otp1 = request.session["otp1"]
        otp2 = request.POST.get("otp2")
        user = get_user_model().objects.get(username=username)
        if str(otp2) == str(otp1):
            messages.success(request, "Вы успешно зарегистрированы")
            login(request, user)
            messages.success(request, f" Добро пожаловать, {username}!")
            return redirect("/")
        else:
            messages.error(request, "Неверный одноразоый код!")
    return render(request, "account/otp.html")


class UserProfileView(DetailView):
    model = get_user_model()
    context_object_name = "user"
