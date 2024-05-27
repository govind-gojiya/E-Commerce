from time import sleep
# from storefront.celery import celery
from celery import shared_task

# @celery.task # One way to do but it will create dependencies
@shared_task
def notify_customers(message):
    print("Sending 10K Notifications to the customer")
    print(message)
    sleep(10)
    print("Message notification sent succesfully.")