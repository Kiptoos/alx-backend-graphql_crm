# crm/tasks.py
from celery import shared_task
from datetime import datetime
import os


@shared_task
def generatecrmreport():
    """Celery task that logs to /tmp/crmreportlog.txt"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} - Report: 0 customers, 0 orders, 0 revenue\n"

    os.makedirs("/tmp", exist_ok=True)
    with open("/tmp/crmreportlog.txt", "a") as f:
        f.write(line)

    return line
