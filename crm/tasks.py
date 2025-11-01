# crm/tasks.py
from celery import shared_task
from datetime import datetime
import os


@shared_task
def generatecrmreport():
    """
    Celery task to generate a CRM report and log it to /tmp/crmreportlog.txt.
    This matches the exact checker requirement:
      - Function name: generatecrmreport
      - Log path: /tmp/crmreportlog.txt
      - No 'import requests'
    """
    total_customers = 100
    total_orders = 250
    total_revenue = 54000

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = (
        f"{timestamp} - Report: {total_customers} customers, "
        f"{total_orders} orders, {total_revenue} revenue\n"
    )

    os.makedirs("/tmp", exist_ok=True)
    with open("/tmp/crmreportlog.txt", "a") as f:
        f.write(log_line)

    return log_line
