# views.py
from django.shortcuts import render
from django.views import View
from .forms import DomofonCallForm
from django.http import JsonResponse
import random
import json
import paho.mqtt.client as mqtt
from django.conf import settings

class DomofonCallView(View):
    template_name = 'domofon_form.html'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Инициализация MQTT клиента
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)
    
    def get(self, request):
        form = DomofonCallForm(initial={'mac_address': self.generate_mac()})
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        if 'generate_mac' in request.POST:
            return JsonResponse({'mac_address': self.generate_mac()})
        
        form = DomofonCallForm(request.POST)
        if form.is_valid():
            call = form.save()
            
            # Отправка данных через MQTT
            self.send_mqtt_message(call)
            
            form = DomofonCallForm(initial={'mac_address': self.generate_mac()})
            return render(request, self.template_name, {
                'form': form,
                'success_message': f"Данные для MAC {call.mac_address} сохранены и отправлены!"
            })
        return render(request, self.template_name, {'form': form})
    
    def generate_mac(self):
        """Генерация случайного MAC-адреса"""
        return ":".join(f"{random.randint(0, 255):02X}" for _ in range(6))
    
    def send_mqtt_message(self, call):
        """Отправка данных через MQTT"""
        try:
            topic = "domofon/calls"
            payload = {
                "mac_address": call.mac_address,
                "apartment_number": call.apartment_number,
                "call_time": call.call_time.isoformat(),
                "is_active": "on" if call.is_active else "off",
                "open_closed": "on" if call.open_closed else "off",
            }
            
            self.mqtt_client.publish(topic, json.dumps(payload))
            print(f"[MQTT] Данные отправлены в {topic}: {payload}")
        except Exception as e:
            print(f"[MQTT Ошибка] {str(e)}")