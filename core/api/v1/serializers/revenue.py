import calendar

from rest_framework import serializers

from controlenf.mixins.view import CompanyContextView
from core import models


class RevenueSerializer(serializers.ModelSerializer):
    customer_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = models.Revenue
        fields = (
            "id",
            "amount",
            "customer",
            "customer_id",
            "description",
            "accrual_date",
            "transaction_date",
        )

    def create(self, validated_data):
        validated_data["company"] = self.context["company"]
        return super(RevenueSerializer, self).create(validated_data)


class RevenueByMonthSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        sum_revenue = []
        payload = {
            "revenue": [],
        }
        for data in instance:
            payload["revenue"].append({
                "month_name": calendar.month_name[data.get("month").month],
                "month_revenue": data.get("month_revenue")
            })
            sum_revenue.append(data.get("month_revenue"))

        payload["max_revenue_amount"] = sum(sum_revenue)
        return payload


class RevenueByCustomerSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        sum_revenue = []
        payload = {
            "revenue": [],
        }
        for data in instance:
            payload["revenue"].append({
                "customer_name": models.Customer.objects_without_deleted.get(pk=data.get("customer")).name,
                "revenue": data.get("revenue")
            })
            sum_revenue.append(data.get("revenue"))

        payload["max_revenue_amount"] = sum(sum_revenue)
        return payload
