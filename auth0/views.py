from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from joladnijo.auth0 import requires_permission


@api_view(["GET"])
@permission_classes([AllowAny])
def public(request):
    return JsonResponse(
        {
            "message": "Hello from a public endpoint! You don't need to be authenticated to see this."
        }
    )


@api_view(["GET"])
def private(request):
    return JsonResponse(
        {
            "message": "Hello from a private endpoint! You need to be authenticated to see this."
        }
    )


@api_view(["GET"])
@requires_permission("asset-request:r:a")
def restricted(request):
    return JsonResponse(
        {
            "message": "Hello from a restricted endpoint! You need to be authenticated and have a specific permission to see this."
        }
    )
