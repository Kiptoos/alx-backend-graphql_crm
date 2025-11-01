# Celery Task for Generating CRM Reports

This project uses Celery and django-celery-beat to run a periodic task that generates a CRM report and logs it to a file.

## Setup Steps

1. **Install Redis and dependencies.**

   On Ubuntu/Debian:
   ```bash
   sudo apt-get update
   sudo apt-get install redis-server
   sudo systemctl enable redis-server
   sudo systemctl start redis-server
