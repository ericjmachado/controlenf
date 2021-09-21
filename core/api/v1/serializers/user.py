from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core import models
from .. import serializers as core_serializer


class UserSerializer(serializers.ModelSerializer):
    cnpj = serializers.CharField(write_only=True, required=False)
    company_name = serializers.CharField(write_only=True, required=False)
    companies = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.User
        fields = ("id", "username", "password", "name", "phone_number", "email", "cnpj", "company_name", "companies")
        extra_kwargs = {"password": {"write_only": True}}

    def get_companies(self, obj: models.User):
        from core.api.v1.serializers import CompanySerializer
        return CompanySerializer(obj.companies.all(), many=True).data

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop("password")
        cnpj, company_name = (
            validated_data.pop("cnpj", None),
            validated_data.pop("company_name", None),
        )
        user = models.User(**validated_data)
        user.set_password(password)
        user.save()
        if all([cnpj, company_name]):
            payload = {"cnpj": cnpj, "company_name": company_name, "owner": user.get_pk}
            serializer = core_serializer.CompanySerializer(data=payload)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            raise ValidationError(
                {"user": "Insira cnpj e nome da companhia para criar usuario!"}
            )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
            instance.save()
        return super(UserSerializer, self).update(instance, validated_data)
