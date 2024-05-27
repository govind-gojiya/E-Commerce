from django.dispatch import receiver
from store.signals import order_created

@receiver(order_created)
def order_created_handler(sender, **kwargs):
    print(f"Order created: {kwargs['order']}")