from django.db import models
from django.contrib.auth.models import AbstractUser
from ads.models import Guild


# Create your models here.

class User(AbstractUser):
    guild = models.ForeignKey(
        to=Guild, 
        null=True, 
        blank=True,
        on_delete=models.PROTECT)

    def __dir__(self):
        return self.username
