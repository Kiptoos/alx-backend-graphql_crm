# crm/tasks.py
from datetime import datetime
import os
from celery import shared_task

# Optional: import Django settings or GraphQL schema if needed
try:
    from crm.schema import schema  # adjust if your schema lives elsewhere
except ImportError:
    schema = None

# Log file path
LOG_PATH = "/tmp/crm_report_log.txt"


@shared_task
def generate_crm_report():
    """
    Celery task to generate a weekly CRM report.

    Fetches data (via GraphQL) for:
      - total customers
      - total orders
      - total revenue

    Logs the report to /tmp/crm_report_log.txt with timestamp.
    """
    if schema is None:
        _write_log(f"{_timestamp()} - ERROR: GraphQL schema not found; cannot generate report.\n")
        return

    # Example GraphQL query — adjust to match your schema fields
    query = """
    query CRMReport {
      customersCount
      ordersAggregate {
        totalCount
        totalRevenue
      }
    }
    """

    result = schema.execute(query)
    if result.errors:
        _write_log(f"{_timestamp()} - ERROR: {result.errors}\n")
        return

    data = result.data or {}
    total_customers = data.get("customersCount", 0)
    orders_agg = data.get("ordersAggregate") or {}
    total_orders = orders_agg.get("totalCount", 0)
    total_revenue = orders_agg.get("totalRevenue", 0)

    log_line = (
        f"{_timestamp()} - Report: {total_customers} customers, "
        f"{total_orders} orders, {total_revenue} revenue\n"
    )
    _write_log(log_line)


def _write_log(message: str):
    """Append message to log file at /tmp/crm_report_log.txt."""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as log_file:
        log_file.write(message)


def _timestamp():
    """Return current timestamp string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
