from rest_framework import viewsets

from . import models
from . import serializers


class AidCenterViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = models.AidCenter.objects.all()
    serializer_class = serializers.AidCenterSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

