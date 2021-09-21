from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from controlenf.mixins import CompanyContextView
from controlenf.pagination import DefaultResultsSetPagination
from core import models
from .. import serializers, filters


class CustomerViewSet(CompanyContextView, viewsets.ModelViewSet):
    serializer_class = serializers.CustomerSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = DefaultResultsSetPagination
    filter_class = filters.CustomerFilter

    def get_queryset(self):
        return models.Customer.objects_without_deleted.filter(
            company=self.kwargs.get("companies_pk")
        )
