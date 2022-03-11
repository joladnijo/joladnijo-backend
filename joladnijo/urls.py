"""joladnijo URL Configuration

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
"""
from django.contrib import admin
from django.urls import path
from . import views


handler400 = 'joladnijo.views.handle_400'
handler403 = 'joladnijo.views.handle_403'
handler404 = 'joladnijo.views.handle_404'
handler500 = 'joladnijo.views.handle_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/400', views.handle_400),
    path('test/403', views.handle_403),
    path('test/404', views.handle_404),
    path('test/500', views.handle_500),
    path('test', views.test),
    path('test/<slug:slug>', views.test),
]
