"""TravelX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

app_name = 'Booking'

urlpatterns = [
    path(r'',views.booking_home),
    path(r'Data_submit/',views.Data_submit),
    path(r'booking-confirmed/',views.bookingconfirm),
    path(r'passenger-info/',views.passengerinfo),
    path(r'direct-price/',views.pricedisplay),
    path(r'<slug:slug>/',views.choice,name='capture'),

]
