from rest_framework import serializers

from core import models


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ("id", "owner", "cnpj", "company_name",)
        extra_kwargs = {"owner": {"write_only": True}}

    def create(self, validated_data):
        if not validated_data.get("owner"):
            validated_data["owner"] = self.context.get("owner")
        return super(CompanySerializer, self).create(validated_data)
