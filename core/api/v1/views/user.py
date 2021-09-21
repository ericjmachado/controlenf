from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from core import models
from .. import serializers


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = []
        return super(UserViewSet, self).get_permissions()
