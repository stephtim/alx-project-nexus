from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem

@receiver(post_save, sender=OrderItem)
def reduce_inventory_on_order(sender, instance, created, **kwargs):
    if not created:
        return
    variant = instance.variant
    inv = getattr(variant, "inventory", None)
    if inv:
        inv.quantity = max(inv.quantity - instance.quantity, 0)
        inv.save()
