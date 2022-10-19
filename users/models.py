from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy
from ads.models import Guild


# Create your models here.

class User(AbstractUser):
    guild = models.ForeignKey(
        to=Guild, 
        null=True, 
        blank=True,
        on_delete=models.PROTECT)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse_lazy('user_profile', kwargs={'pk': self.pk})
