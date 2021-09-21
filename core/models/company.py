from django.db import models
from django.utils.translation import ugettext_lazy as _

from controlenf.mixins import ControlModel
from helpers.validators import CNPJValidator


class Company(ControlModel):
    owner = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, related_name="companies")
    cnpj = models.CharField(
        max_length=14,
        blank=True,
        verbose_name=_("cnpj"),
        validators=[CNPJValidator()],
    )
    company_name = models.CharField(max_length=255)

