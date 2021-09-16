from django.db import models

from controlenf.mixins import ControlModel


class Category(ControlModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
