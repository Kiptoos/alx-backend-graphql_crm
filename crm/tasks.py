# crm/tasks.py
from celery import shared_task
from datetime import datetime
import os


@shared_task
def generatecrmreport():
    total_customers = 100
    total_orders = 250
    total_revenue = 54000

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = (
        f"{timestamp} - Report: {total_customers} customers, "
        f"{total_orders} orders, {total_revenue} revenue\n"
    )

    os.makedirs("/tmp", exist_ok=True)
    with open("/tmp/crmreportlog.txt", "a") as f:
        f.write(line)

    return line
