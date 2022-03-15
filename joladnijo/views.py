from django import VERSION
from django.http import JsonResponse
from rest_framework import viewsets

from . import models, serializers


class AidCenterViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = models.AidCenter.objects.all()
    serializer_class = serializers.AidCenterSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


def handle_400(request, exception=None):
    return JsonResponse(
        status=400,
        data={"success": False, "message": "Bad request"},
    )


def handle_403(request, exception=None):
    return JsonResponse(
        status=403,
        data={"success": False, "message": "Permission denied"},
    )


def handle_404(request, exception=None):
    return JsonResponse(
        status=404,
        data={"success": False, "message": "Not found"},
    )


def handle_500(request):
    return JsonResponse(
        status=500,
        data={"success": False, "message": "Server error"},
    )


# TODO: FE tesztelés után törölni
def test(request, slug=None):
    response = {
        "success": True,
        "message": "OK",
        "djangoVersion": VERSION,
    }
    if slug:
        response['slug'] = slug
    return JsonResponse(response)
