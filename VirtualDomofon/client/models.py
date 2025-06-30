from django.db import models
from django.utils import timezone

class DomofonCall(models.Model):
    mac_address = models.CharField(max_length=17, verbose_name="MAC адрес домофона")
    apartment_number = models.PositiveIntegerField(verbose_name="Номер квартиры")
    call_time = models.DateTimeField(default=timezone.now, verbose_name="Время звонка")
    is_active = models.BooleanField(default=True, verbose_name="Домофон включен")

    def __str__(self):
        return self.mac_address

    class Meta:
        verbose_name = 'MAC адрес домофона'
        verbose_name_plural = 'MAC адрес домофона'
