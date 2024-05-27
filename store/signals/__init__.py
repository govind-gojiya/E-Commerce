from django.dispatch import Signal

# custome event which we can fire in our app see seializers.py > CreateOrderSerializer > save method
order_created = Signal() 