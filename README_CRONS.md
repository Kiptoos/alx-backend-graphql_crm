# Crons: Scheduling and Automating Tasks (Django + GraphQL)

This package provides all files required by the tasks:

## Files Created
- **Task 0**
  - `crm/cron_jobs/clean_inactive_customers.sh` (executable)
  - `crm/cron_jobs/customer_cleanup_crontab.txt`
- **Task 1**
  - `crm/cron_jobs/send_order_reminders.py`
  - `crm/cron_jobs/order_reminders_crontab.txt`
- **Task 2**
  - `crm/cron.py`
  - `crm/settings.py` (append the django-crontab config)
  - `requirements.txt`
- **Task 3**
  - `crm/schema.py` (adds UpdateLowStockProducts mutation)

## Cron entries (absolute path placeholders)
- Edit `/opt/alx-backend-graphql_crm` in the two *.txt crontab files to the **absolute path** of your repo.

## Apply django-crontab jobs
```bash
# After adding django_crontab and CRONJOBS in settings.py:
python manage.py crontab add
python manage.py crontab show
# (later) python manage.py crontab remove
```

## Time window
Start: Oct 27, 2025 — End: Nov 3, 2025
