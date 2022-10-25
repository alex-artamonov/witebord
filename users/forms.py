from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = get_user_model()
        fields = ("username", 
                "first_name", 
                "last_name", 
                "email", 
                "password1", 
                "password2", )


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields  = '__all__'
        exclude = ['user', 'email','name','otp_code']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields  = ['username','first_name','last_name', 'email', 'password1', 'password2']