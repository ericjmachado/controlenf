from rest_framework import serializers

from core import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ("id", "name", "description")

    def create(self, validated_data):
        validated_data["company"] = self.context["company"]
        return super(CategorySerializer, self).create(validated_data)
