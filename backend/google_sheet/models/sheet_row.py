from django.db import models
from django.utils import timezone


class SheetRow(models.Model):
    sheet_id = models.PositiveIntegerField(verbose_name='айди в таблице', default=0)
    order_num = models.PositiveIntegerField(verbose_name='заказ №', default=0)
    cost = models.PositiveIntegerField(verbose_name='стоимость,$', default=0)
    cost_in_rur = models.PositiveIntegerField(verbose_name='стоимость в рублях', default=0)
    delivery_time = models.DateField(verbose_name='Срок поставки', default=timezone.now)
    informed_about_rancid = models.BooleanField(verbose_name='Проинформарован о том, что заказ протух', default=False)

    class Meta:
        verbose_name = 'Строчка таблицы google'
        verbose_name_plural = 'Строчки таблицы google'

    def __str__(self):
        return f'{self.order_num} | {self.cost} | {self.delivery_time}'
