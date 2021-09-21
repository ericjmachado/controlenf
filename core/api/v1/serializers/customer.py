from rest_framework import serializers

from core import models


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ("id", "cnpj", "commercial_name", "legal_name",)

    def create(self, validated_data):
        validated_data["company"] = self.context["company"]
        return super(CustomerSerializer, self).create(validated_data)
