from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from controlenf.mixins import ControlModel
from helpers.validators import CNPJValidator


class Customer(ControlModel):
    cnpj = models.CharField(
        max_length=14,
        blank=True,
        verbose_name=_("cnpj"),
        validators=[CNPJValidator()],
    )
    commercial_name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255)
    company = models.ForeignKey("Company", on_delete=models.CASCADE, blank=True)
