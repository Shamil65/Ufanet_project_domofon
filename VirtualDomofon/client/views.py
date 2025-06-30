# client/views.py
from django.shortcuts import render
from .models import DomofonCall

def mqtt_monitor(request):
    
    macs = DomofonCall.objects.all()

    data = {
        'title': f'Вызовы',
        'mac_address': macs,
    }
    return render(request, 'mqtt_monitor.html', data)

