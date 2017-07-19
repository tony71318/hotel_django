"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
admin.autodiscover()     

from restaurants.views import menu  
from ethereum.views import get,multiply_contract,booking_contract
from owlting_hotel.views import hotel_menu

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^menu/$', menu),
    url(r'^ethereum/(?P<title>[\w\-]+)/$', get),
    url(r'^ethereum/multiply_contract/(?P<function>[\w\-]+)/$', multiply_contract),
    url(r'^ethereum/booking_contract/orders/(?P<function>[\w\-]+)/$', booking_contract),
    url(r'^owlting_hotel/menu$', hotel_menu),
]
