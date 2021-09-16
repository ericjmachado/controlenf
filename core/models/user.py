from django.contrib.auth.models import AbstractUser
from django.db import models

from controlenf.mixins import ControlModel


class User(ControlModel, AbstractUser):
    name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=16)


