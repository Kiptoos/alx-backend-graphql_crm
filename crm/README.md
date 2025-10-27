# Celery + Celery Beat (Optional Task 4)

## Install Redis & dependencies
- Install Redis locally, e.g. on Ubuntu: `sudo apt-get install redis-server`
- Python dependencies are in `requirements.txt`

## Run migrations
```bash
python manage.py migrate
```

## Start Celery worker
```bash
celery -A crm worker -l info
```

## Start Celery Beat
```bash
celery -A crm beat -l info
```

## Verify weekly report logs
- Check `/tmp/crm_report_log.txt` after the scheduled time (Mon 06:00).
