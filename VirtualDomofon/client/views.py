# client/views.py
from django.shortcuts import render

def mqtt_monitor(request):
    return render(request, 'client/mqtt_monitor.html')