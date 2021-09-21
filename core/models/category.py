from django.db import models

from controlenf.mixins import ControlModel


class Category(ControlModel):
    company = models.ForeignKey("Company", blank=True, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
