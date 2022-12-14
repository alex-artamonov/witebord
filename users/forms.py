from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    is_subscribed = forms.BooleanField(label="Подписаться на еженедельную рассылку")
    is_subscribed.initial = 1

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "guild",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "is_subscribed",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "password1": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "password2": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }
