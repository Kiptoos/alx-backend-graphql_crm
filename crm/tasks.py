# crm/tasks.py
from celery import shared_task
from datetime import datetime
import os

# try to import your GraphQL schema if it exists
try:
    from crm.schema import schema
except ImportError:
    schema = None


@shared_task
def generate_crm_report():
    """
    Celery task to generate a CRM report and log it to /tmp/crm_report_log.txt
    Format:
    2025-11-01 06:00:00 - Report: 10 customers, 25 orders, 12000 revenue
    """
    # default values if schema is not available
    total_customers = 0
    total_orders = 0
    total_revenue = 0

    # if a GraphQL schema is present, try to fetch the actual values
    if schema is not None:
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
        if not result.errors and result.data:
            total_customers = result.data.get("customersCount", 0)
            agg = result.data.get("ordersAggregate") or {}
            total_orders = agg.get("totalCount", 0)
            total_revenue = agg.get("totalRevenue", 0)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = (
        f"{timestamp} - Report: {total_customers} customers, "
        f"{total_orders} orders, {total_revenue} revenue\n"
    )

    os.makedirs("/tmp", exist_ok=True)
    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(line)

    return line
