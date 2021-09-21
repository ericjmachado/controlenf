from django.db.models import Max, Sum
from django.db.models.functions import TruncMonth
from rest_framework import viewsets, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from controlenf.mixins import CompanyContextView
from core import models
from .. import serializers


class ExpenseViewSet(
    CompanyContextView,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.ExpenseSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return models.Expense.objects_without_deleted.filter(
            company=self.kwargs.get("companies_pk")
        )


class TotalExpenseViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        res = models.Expense.objects_without_deleted.filter(
            company=self.kwargs.get("companies_pk")
        ).aggregate(max_expense_amount=Max("amount"), total_expense=Sum("amount"))
        return Response(res)


class TotalExpenseByMonthViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ExpenseByMonthSerializer

    def get_queryset(self):
        year = self.request.query_params.get("year")
        if not year:
            raise ValidationError({"year": "Ano é obrigatório"})
        return models.Expense.objects_without_deleted.filter(
            company=self.kwargs.get("companies_pk"), accrual_date__year=year
        )

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs = (
            qs.annotate(month=TruncMonth("accrual_date"))
            .values("month")
            .annotate(month_expense=Sum("amount"))
            .values("month", "month_expense")
        )
        data = self.get_serializer(qs).data
        return Response(data)


class TotalExpenseByCustomerViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ExpenseByCustomerSerializer

    def get_queryset(self):
        year = self.request.query_params.get("year")
        if not year:
            raise ValidationError({"year": "Ano é obrigatório"})
        return models.Expense.objects_without_deleted.filter(
            company=self.kwargs.get("companies_pk"), accrual_date__year=year, category_id__isnull=False
        )

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs = (
            qs.values("category")
            .annotate(expense=Sum("amount"))
            .values("category", "expense")
        )
        data = self.get_serializer(qs).data
        return Response(data)
