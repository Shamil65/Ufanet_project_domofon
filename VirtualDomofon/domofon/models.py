from django.db import models
from django.utils import timezone

class DomofonCall(models.Model):
    mac_address = models.CharField(max_length=17, verbose_name="MAC адрес домофона")
    apartment_number = models.PositiveIntegerField(verbose_name="Номер квартиры")
    call_time = models.DateTimeField(default=timezone.now, verbose_name="Время звонка")
    is_active = models.BooleanField(default=True, verbose_name="Домофон включен")
    open_closed = models.BooleanField(default=False, verbose_name="Открытие двери")

    def __str__(self):
        status = "включен" if self.is_active else "выключен"
        return f"Звонок в кв. {self.apartment_number} (MAC: {self.mac_address}) в {self.call_time}. Домофон {status}"

    class Meta:
        verbose_name = "Звонок домофона"
        verbose_name_plural = "Звонки домофона"