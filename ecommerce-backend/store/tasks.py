from celery import shared_task
from .models import Order

@shared_task
def send_order_confirmation(order_id):
    try:
        order = Order.objects.get(id=order_id)
        # Minimal demo: print
        print(f"Order confirmation for {order.order_number}")
    except Order.DoesNotExist:
        print("Order not found")
