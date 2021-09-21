from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from controlenf.pagination import DefaultResultsSetPagination
from core import models
from .. import serializers


class CompanyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    pagination_class = DefaultResultsSetPagination
    serializer_class = serializers.CompanySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return models.Company.objects_without_deleted.filter(owner=self.request.user)

    def get_serializer_context(self):
        context = super(CompanyViewSet, self).get_serializer_context()
        context["owner"] = self.request.user
        return context
