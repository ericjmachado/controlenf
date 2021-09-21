from django.db.models import Max, Sum
from django.db.models.functions import TruncMonth
from rest_framework import viewsets, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from controlenf.mixins import CompanyContextView
from core import models
from .. import serializers


class RevenueViewSet(
    CompanyContextView,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.RevenueSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return models.Revenue.objects_without_deleted.filter(
            company=self.kwargs.get("companies_pk")
        )


class TotalRevenueViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        res = models.Revenue.objects_without_deleted.filter(
            company=self.kwargs.get("companies_pk")
        ).aggregate(max_revenue_amount=Max("amount"), total_revenue=Sum("amount"))
        return Response(res)


class TotalRevenueByMonthViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.RevenueByMonthSerializer

    def get_queryset(self):
        year = self.request.query_params.get("year")
        if not year:
            raise ValidationError({"year": "Ano é obrigatório"})
        return models.Revenue.objects_without_deleted.filter(
            company=self.kwargs.get("companies_pk"), accrual_date__year=year
        )

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs = (
            qs.annotate(month=TruncMonth("accrual_date"))
            .values("month")
            .annotate(month_revenue=Sum("amount"))
            .values("month", "month_revenue")
        )
        data = self.get_serializer(qs).data
        return Response(data)


class TotalRevenueByCustomerViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.RevenueByCustomerSerializer

    def get_queryset(self):
        year = self.request.query_params.get("year")
        if not year:
            raise ValidationError({"year": "Ano é obrigatório"})
        return models.Revenue.objects_without_deleted.filter(
            company=self.kwargs.get("companies_pk"), accrual_date__year=year, customer_id__isnull=False
        )

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs = (
            qs.values("customer")
            .annotate(revenue=Sum("amount"))
            .values("customer", "revenue")
        )
        data = self.get_serializer(qs).data
        return Response(data)
