# CRM Celery Setup

This project uses **Celery** + **Redis** + **django-celery-beat** to run scheduled background tasks.
The scheduled task generates a **weekly CRM report** from the GraphQL API and appends it to
`/tmp/crm_report_log.txt`.

## 1. Prerequisites

- Python 3.10+ (recommended)
- Django installed
- Redis installed and running locally on default port

### Install Redis (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
