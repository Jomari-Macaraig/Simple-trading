from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order, BulkOrder
from .tasks import process_order, process_bulk_order


@receiver(post_save, sender=Order)
def process_order_background_tasks(sender, instance, created, **kwargs):
    if created:
        process_order.apply_async(kwargs={"order_id": instance.id})


@receiver(post_save, sender=BulkOrder)
def process_order_background_tasks(sender, instance, created, **kwargs):
    if created:
        process_bulk_order.apply_async(kwargs={"bulk_order_id": instance.id})
