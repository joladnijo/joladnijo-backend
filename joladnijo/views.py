from rest_framework import permissions, viewsets

from . import models
from . import serializers


class AidCenterViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = models.AidCenter.objects.all()
    serializer_class = serializers.AidCenterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

