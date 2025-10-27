INSTALLED_APPS = []

# --- django-crontab integration (added for scheduling) ---
INSTALLED_APPS = list(INSTALLED_APPS) + ['django_crontab']

CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]
