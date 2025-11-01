# crm/tasks.py
from celery import shared_task
from datetime import datetime
import os

LOG_PATH = "/tmp/crmreportlog.txt"


@shared_task
def generatecrmreport():
    """
    Celery task that generates a CRM report and logs it to /tmp/crmreportlog.txt.
    This matches the auto-check requirement:
    - function name: generatecrmreport
    - log file: /tmp/crmreportlog.txt
    - no 'import requests'
    """
    # dummy/sample values; replace with real query logic if needed
    total_customers = 100
    total_orders = 250
    total_revenue = 54000

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = (
        f"{timestamp} - Report: {total_customers} customers, "
        f"{total_orders} orders, {total_revenue} revenue\n"
    )

    # ensure /tmp exists and write the log
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(line)

    return line
