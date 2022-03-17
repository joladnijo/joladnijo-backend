'''joladnijo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
'''
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

handler400 = 'joladnijo.views.handle_400'
handler403 = 'joladnijo.views.handle_403'
handler404 = 'joladnijo.views.handle_404'
handler500 = 'joladnijo.views.handle_500'

router = SimpleRouter()
router.register(r'aid-centers', views.AidCenterViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('auth0.urls')),  # Only for testing auth0
    # TODO: FE tesztelés után törölni innentől
    path('test', views.test),
    path('test/400', views.handle_400),
    path('test/403', views.handle_403),
    path('test/404', views.handle_404),
    path('test/500', views.handle_500),
    path('test/<slug:slug>', views.test),
    # TODO: FE tesztelés után törölni idáig
    path('', include(router.urls)),
]
