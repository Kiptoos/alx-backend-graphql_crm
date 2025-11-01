# Celery Task for Generating CRM Reports

## Setup Steps

1. Install Redis and dependencies.
2. Run migrations (python manage.py migrate).
3. Start Celery worker (celery -A crm worker -l info).
4. Start Celery Beat (celery -A crm beat -l info).
5. Verify logs in /tmp/crm_report_log.txt.
