# mqtt_listener.py
import paho.mqtt.client as mqtt
import json
import logging
import time
import threading
from django.conf import settings
from .models import DomofonCall

class MQTTListener:
    def __init__(self):
        self.client = mqtt.Client()
        self._running = False
        self._reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.setup_logging()
        self.configure_callbacks()
        
    def setup_logging(self):
        """Настройка логирования"""
        self.logger = logging.getLogger('MQTTListener')
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)
    
    def configure_callbacks(self):
        """Настройка обработчиков событий"""
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
    
    def _on_connect(self, client, userdata, flags, rc):
        """Обработка подключения"""
        self._reconnect_attempts = 0
        if rc == 0:
            self.logger.info("Connected to MQTT Broker")
            client.subscribe("domofon/#")
        else:
            self.logger.error(f"Connection failed with code {rc}")
            if self._running:
                self._reconnect()
    
    def _on_disconnect(self, client, userdata, rc):
        """Обработка отключения"""
        if rc != 0:
            self.logger.warning(f"Unexpected disconnection (code: {rc})")
            if self._running:
                self._reconnect()
    
    def _on_message(self, client, userdata, msg):
        """Обработка входящих сообщений"""
        try:
            payload = self._parse_payload(msg.payload)
            self._process_message(msg.topic, payload)
        except Exception as e:
            self.logger.error(f"Message processing error: {str(e)}", exc_info=True)
    
    def _parse_payload(self, payload):
        """Парсинг содержимого сообщения"""
        try:
            return json.loads(payload.decode('utf-8'))
        except json.JSONDecodeError:
            return {"raw_data": payload.decode('utf-8', errors='ignore')}
    
    def _process_message(self, topic, payload):
        """Обработка и вывод сообщения"""
        if isinstance(payload, dict):
            try:
                govno2 = []
                for k, v in payload.items():
                    govno2.append(v)
                DomofonCall.objects.create(mac_address=govno2[0], apartment_number=int(govno2[1]), is_active=True if govno2[3] == 'on' else False, open_closed=True if govno2[4] == 'on' else False)
                
                print("Данные, полученные с помощью MQTT сохранены в БД")
            except:
                print("Ошибка при добавлении данных в бд из mqtt запроса")


        try:
            print("\n" + "="*60)
            print(f"MQTT Message from {topic}:")
            if isinstance(payload, dict):
                for k, v in payload.items():
                    print(f"  {k}: {v}")
            else:
                print(f"  {payload}")
            print("="*60)
            
            self.logger.info(f"Processed message from {topic}")
        except Exception as e:
            self.logger.error(f"Error displaying message: {str(e)}")
    
    def _reconnect(self):
        """Логика переподключения"""
        if self._reconnect_attempts < self.max_reconnect_attempts:
            self._reconnect_attempts += 1
            wait = min(2 ** self._reconnect_attempts, 30)  # Макс 30 сек
            self.logger.info(f"Reconnecting attempt #{self._reconnect_attempts} in {wait}s...")
            time.sleep(wait)
            self._connect()
        else:
            self.logger.error("Max reconnection attempts reached")
            self.stop()
    
    def _connect(self):
        """Установка соединения"""
        try:
            self.logger.info(f"Connecting to {settings.MQTT_BROKER}:{settings.MQTT_PORT}")
            self.client.connect(
                settings.MQTT_BROKER,
                settings.MQTT_PORT,
                settings.MQTT_KEEPALIVE
            )
        except Exception as e:
            self.logger.error(f"Connection error: {str(e)}")
            if self._running:
                self._reconnect()
    
    def start(self):
        """Запуск слушателя"""
        if not self._running:
            self._running = True
            self.logger.info("Starting MQTT listener")
            self._connect()
            
            # Запуск сетевого цикла в отдельном потоке
            self._network_thread = threading.Thread(
                target=self._network_loop,
                daemon=True,
                name="MQTT-Network-Thread"
            )
            self._network_thread.start()
    
    def _network_loop(self):
        """Бесконечный цикл обработки сообщений"""
        while self._running:
            try:
                self.client.loop(timeout=1.0)
            except Exception as e:
                self.logger.error(f"Network loop error: {str(e)}")
                time.sleep(1)
    
    def stop(self):
        """Остановка слушателя"""
        if self._running:
            self._running = False
            self.client.disconnect()
            self.logger.info("MQTT listener stopped")

# Глобальный экземпляр
mqtt_listener = MQTTListener()

def start_mqtt_listener():
    """Функция для запуска из других модулей"""
    mqtt_listener.start()

def stop_mqtt_listener():
    """Функция для остановки"""
    mqtt_listener.stop()