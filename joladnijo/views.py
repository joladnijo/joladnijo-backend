from django.http import JsonResponse
from django import VERSION


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
        data={"success": False, "message": "Page not found"},
    )


def handle_500(request):
    return JsonResponse(
        status=500,
        data={"success": False, "message": "Server error"},
    )


def test(request, slug=None):
    response = {
        "success": True,
        "message": "OK",
        "djangoVersion": VERSION,
    }
    if slug:
        response['slug'] = slug
    return JsonResponse(response)
