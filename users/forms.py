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
                "guild", 
                "first_name", 
                "last_name", 
                "email", 
                "password1", 
                "password2", )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control',}),
            'first_name': forms.TextInput(attrs={'class': 'form-control',}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',}),
            'email': forms.EmailInput(attrs={'class': 'form-control',}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control',}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control',}),
        }


# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields  = '__all__'
#         exclude = ['user', 'email','name','otp_code']


# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields  = ['username','first_name','last_name', 'email', 'password1', 'password2']