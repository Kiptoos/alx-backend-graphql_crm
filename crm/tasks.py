# crm/tasks.py
import os
from datetime import datetime
from celery import shared_task
from django.conf import settings

# adjust this import to where your GraphQL schema lives
# e.g. from crm.schema import schema
try:
    from crm.schema import schema
except ImportError:
    # fallback: if your schema is e.g. in apps.crm_api.schema
    schema = None


LOG_PATH = "/tmp/crm_report_log.txt"


@shared_task
def generate_crm_report():
    """
    Celery task that runs a GraphQL query to fetch:
      - total customers
      - total orders
      - total revenue
    and appends to /tmp/crm_report_log.txt
    """
    if schema is None:
        # If we can't import schema, fail gracefully
        msg = f"{_timestamp()} - ERROR: GraphQL schema not found; cannot generate report.\n"
        _write_log(msg)
        return msg

    # This GraphQL query must match your actual schema fields.
    # Adjust names if your schema differs.
    query = """
    query CRMReport {
      customersCount
      ordersAggregate {
        totalCount
        totalRevenue
      }
    }
    """

    # Execute GraphQL query
    result = schema.execute(query)

    if result.errors:
        msg = f"{_timestamp()} - ERROR: {result.errors}\n"
        _write_log(msg)
        return msg

    data = result.data or {}

    # Adjust to match the structure returned by your schema
    total_customers = data.get("customersCount", 0)
    orders_agg = data.get("ordersAggregate") or {}
    total_orders = orders_agg.get("totalCount", 0)
    total_revenue = orders_agg.get("totalRevenue", 0)

    # Build final log line
    log_line = (
        f"{_timestamp()} - Report: {total_customers} customers, "
        f"{total_orders} orders, {total_revenue} revenue\n"
    )
    _write_log(log_line)
    return log_line


def _write_log(text: str):
    # ensure directory exists
    dir_name = os.path.dirname(LOG_PATH)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(text)


def _timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
