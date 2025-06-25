# apps.py
from django.apps import AppConfig
import os
import threading

class ClientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client'

    def ready(self):
        """Запуск при инициализации приложения"""
        if self._is_main_process():
            self._start_mqtt_listener()

    def _is_main_process(self):
        """Проверка, что это основной процесс (не reloader)"""
        return os.environ.get('RUN_MAIN') == 'true'

    def _start_mqtt_listener(self):
        """Запуск MQTT слушателя в отдельном потоке"""
        from .mqtt_listener import start_mqtt_listener
        
        # Создаем и запускаем поток
        mqtt_thread = threading.Thread(
            target=start_mqtt_listener,
            daemon=True,
            name="MQTT-Listener-Thread"
        )
        mqtt_thread.start()
        print("MQTT listener initialization complete")