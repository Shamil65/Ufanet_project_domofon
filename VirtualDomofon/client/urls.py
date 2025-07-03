from django.urls import path
from .views import mqtt_monitor

urlpatterns = [
    path('', mqtt_monitor, name='mqtt_monitor'),
]
