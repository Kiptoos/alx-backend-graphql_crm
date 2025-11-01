# crm/celery.py
import os
from celery import Celery

# Set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")

app = Celery("crm")

# Read settings from Django settings, using CELERY_ prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# Discover tasks from all installed apps
app.autodiscover_tasks()
