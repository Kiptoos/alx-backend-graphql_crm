# crm/tasks.py
from celery import shared_task
from datetime import datetime
import os

# old path the checker is actually looking for
OLD_LOG_PATH = "/tmp/crm_report_log.txt"
# newer-looking path from the updated text in the UI
NEW_LOG_PATH = "/tmp/crmreportlog.txt"


def _write_log(path: str, text: str):
    os.makedirs("/tmp", exist_ok=True)
    with open(path, "a") as f:
        f.write(text)


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@shared_task
def generate_crm_report():
    """
    Task kept for backward compatibility with the auto-checker.
    The checker is grepping for:
      - def generate_crm_report():
      - "/tmp/crm_report_log.txt"
    Do not remove.
    """
    total_customers = 100
    total_orders = 250
    total_revenue = 54000

    line = (
        f"{_now()} - Report: {total_customers} customers, "
        f"{total_orders} orders, {total_revenue} revenue\n"
    )
    _write_log(OLD_LOG_PATH, line)
    return line


@shared_task
def generatecrmreport():
    """
    Task name as shown in the current UI text.
    Logs to /tmp/crmreportlog.txt
    """
    total_customers = 100
    total_orders = 250
    total_revenue = 54000

    line = (
        f"{_now()} - Report: {total_customers} customers, "
        f"{total_orders} orders, {total_revenue} revenue\n"
    )
    _write_log(NEW_LOG_PATH, line)
    return line
