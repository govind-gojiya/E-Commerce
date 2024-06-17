# import dj_database_url
from .common import *
# import os
# os.environ['DATABASE_URL'] = 'postgres://expense_manager:Hff7F5TIncPLGJ0lpHHxRGLPB1vJE10S@dpg-cotiss7109ks73alljag-a.oregon-postgres.render.com/expense_tracker_3m5h'

DEBUG = True

SECRET_KEY = 'django-insecure-pvj49yk8p0jhd-72+x#l=8f3cif5kwxpt$yki)fjz(dxj(gvin'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'storefront',
        'HOST': 'localhost',
        'USER': 'postgres',
        'PASSWORD': 'abc123',
        'PORT': '5432',
    }
    # 'default': dj_database_url.config()
}

CELERY_BROKER_URL = 'redis://localhost:6379/1'# last 1 show database name it can be any 1,2,3...
# To run scheduler cmd: celery -A storefront beat
CELERY_BEAT_SCHEDULE = {
    'notify_customers': {
        'task': 'playground.tasks.notify_customers',
        # For 5sec give 5
        'schedule': 5,
        # For perticular time can do likewise
        # 'schedule': crontab(minute='5', hour='0', day_of_week='3'),
        'args': ['This is running via scheduler'],
        # 'kwargs': {}
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "TIMEOUT": 10 * 60 # Default is 5 minutes we can change to 10 minutes like this
    }
}

ALLOWED_HOSTS = ["asked-solved-sheets-activists.trycloudflare.com"]
