from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from controlenf.mixins import ControlModel


class User(ControlModel, AbstractUser):
    objects = UserManager()

    name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=16)

