import django_filters
from django.db.models import Q

from core import models


class CustomerFilter(django_filters.FilterSet):
    cnpj = django_filters.CharFilter(lookup_expr="icontains")
    name = django_filters.CharFilter(method="filter_name")

    class Meta:
        model = models.Customer
        fields = (
            "cnpj",
            "name",
        )

    def filter_name(self, queryset, name, value):
        return queryset.filter(
            Q(commercial_name__icontains=value) | Q(legal_name__icontains=value)
        )
