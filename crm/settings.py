# crm/settings.py

INSTALLED_APPS = [
    # ...
    "django_celery_beat",
    # ...
]
from celery.schedules import crontab
# Celery broker & backend
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

# Optional: so tasks run in local timezone
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = "Africa/Nairobi"



CELERY_BEAT_SCHEDULE = {
    "generate-crm-report": {
        "task": "crm.tasks.generate_crm_report",
        # Monday 06:00 (Nairobi time, since we set CELERY_TIMEZONE)
        "schedule": crontab(day_of_week="mon", hour=6, minute=0),
        # optional: pass kwargs
        "options": {
            "queue": "default",
        },
    },
}
