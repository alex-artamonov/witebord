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
        verbose_name="Гильдия",
    )
    avatar = models.ImageField(
        verbose_name="Аватар", upload_to="pics/%Y/%m/%d/", null=True, blank=True
    )
    is_subscribed = models.BooleanField(
        verbose_name="Подписан на рассылку",
        null=False,
        blank=False
    )

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse_lazy("user_profile", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["username"]
