from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'esri_utils.settings')
app = Celery('esri_utils')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
