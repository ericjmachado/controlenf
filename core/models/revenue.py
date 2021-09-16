from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from controlenf.mixins import ControlModel
from helpers.validators import CNPJValidator


class Revenue(ControlModel):
    amount = models.FloatField()
    company = models.ForeignKey(
        "Company", on_delete=models.CASCADE, blank=True, related_name="reveneues"
    )
    customer = models.ForeignKey(
        "Customer",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reveneues",
    )
    description = models.CharField(max_length=255, blank=True)
    accrual_date = models.DateField()
    transaction_date = models.DateField()
