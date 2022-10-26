from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy
from django import forms
from django.conf import settings
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from ads.models import Guild


# Create your models here.

class User(AbstractUser):
    guild = models.ForeignKey(
        to=Guild, 
        null=True, 
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Гильдия")

    def __str__(self): 
        return self.username

    def get_absolute_url(self):
        return reverse_lazy('ads:user_profile', kwargs={'pk': self.pk})

    
# class BaseRegisterForm(UserCreationForm):
#     email = forms.EmailField(label = "Email")
#     first_name = forms.CharField(label = "Имя")
#     last_name = forms.CharField(label = "Фамилия")

#     class Meta:
#         model = settings.AUTH_USER_MODEL
#         fields = ("username", 
#                 "first_name", 
#                 "last_name", 
#                 "email", 
#                 "password1", 
#                 "password2", )
