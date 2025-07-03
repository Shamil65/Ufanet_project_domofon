from django.shortcuts import render, get_object_or_404, redirect
from .models import DomofonCall
import paho.mqtt.publish as publish

def mqtt_monitor(request):
    macs = DomofonCall.objects.all().order_by('-call_time')

    if request.method == 'POST':
        call_id = request.POST.get('call_id')
        if 'open' in request.POST and call_id:
            call = get_object_or_404(DomofonCall, id=call_id)
            call.open_closed = True  # меняем статус двери на "открыта"
            call.save()
            
            # Можно дополнительно отправить MQTT сообщение о том, что дверь открыта
            topic = "your/mqtt/topic"  # укажи нужный топик
            message = f"Door opened for apartment {call.apartment_number}"
            publish.single(topic, payload=message, hostname="localhost")

            return redirect('mqtt-monitor')  # чтобы избежать повторного отправления при обновлении страницы

    data = {
        'title': 'Вызовы',
        'mac_address': macs,
    }
    return render(request, 'mqtt_monitor.html', data)
