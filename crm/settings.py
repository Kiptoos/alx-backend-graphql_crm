# crm/settings.py

INSTALLED_APPS = [
    # ...
    "django_celery_beat",
]

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_TIMEZONE = "Africa/Nairobi"
CELERY_ENABLE_UTC = False

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "generate-crm-report": {
        "task": "crm.tasks.generate_crm_report",
        "schedule": crontab(day_of_week="mon", hour=6, minute=0),
    },
}
