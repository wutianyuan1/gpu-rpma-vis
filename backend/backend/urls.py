"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from backend.views import get_model_info, get_pmem_usage, switch_device, get_devs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('models/', get_model_info),
    path('pmemusage/', get_pmem_usage),
    path('switchdevice/', switch_device),
    path('getdevs/', get_devs)
]
