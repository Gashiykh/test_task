from django.db.models.signals import pre_save
from django.dispatch import receiver

import logging

from api.models import Order

logger = logging.getLogger("order_events")

@receiver(pre_save, sender=Order)
def order_status_events(sender, instance, **kwargs):

    if instance.pk:
        previous = Order.objects.get(pk=instance.pk)
        old = previous.status
        new = instance.status

        if old != new:
            logger.info(f"Событие: статус заказа {instance.order_id} изменен с {old} на {new}")

            