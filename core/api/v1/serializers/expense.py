import calendar

from rest_framework import serializers

from controlenf.mixins.view import CompanyContextView
from core import models


class ExpenseSerializer(serializers.ModelSerializer):
    category_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = models.Expense
        fields = (
            "id",
            "amount",
            "category",
            "category_id",
            "description",
            "accrual_date",
            "transaction_date",
        )

    def create(self, validated_data):
        validated_data["company"] = self.context["company"]
        return super(ExpenseSerializer, self).create(validated_data)


class ExpenseByMonthSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        sum_expense = []
        payload = {
            "expense": [],
        }
        for data in instance:
            payload["expense"].append({
                "month_name": calendar.month_name[data.get("month").month],
                "month_expense": data.get("month_expense")
            })
            sum_expense.append(data.get("month_expense"))

        payload["max_expense_amount"] = sum(sum_expense)
        return payload


class ExpenseByCustomerSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        sum_expense = []
        payload = {
            "expense": [],
        }
        for data in instance:
            payload["expense"].append({
                "category_name": models.Category.objects_without_deleted.get(pk=data.get("category")).name,
                "expense": data.get("expense")
            })
            sum_expense.append(data.get("expense"))

        payload["max_expense_amount"] = sum(sum_expense)
        return payload
