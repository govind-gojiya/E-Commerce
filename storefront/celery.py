import os
from celery import Celery

# don't forget to import this (import inside projectfolder/__init__.py)
# also set broker url in settigs and install redis from pip as celery does
# To start work : celery -A celery_given_name worker --loglevel=info
# To start schedule work : celery -A celery_name beat 
# Beat only schedule work log of that also in worker terminal
# For monitoring using flower (Here w is silent):
# pip install flower > celery -A celery_name flower > localhost:5555 > monitore tasks

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings.dev') # Set this env variable

celery = Celery('storefront') # Give any name to celery
celery.config_from_object('django.conf:settings', namespace='CELERY') # Fist arg show from where to load data and second show only take variable start from this word
celery.autodiscover_tasks() # This will find all task in tasks.py file

