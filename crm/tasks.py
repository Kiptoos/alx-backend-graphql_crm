from celery import shared_task
from datetime import datetime
from pathlib import Path
from decimal import Decimal

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG = Path("/tmp/crm_report_log.txt")
GRAPHQL_URL = "http://localhost:8000/graphql"

@shared_task
def generate_crm_report():
    """Fetch totals via GraphQL and log a weekly CRM report."""
    transport = RequestsHTTPTransport(url=GRAPHQL_URL, verify=False, retries=3, timeout=20)
    client = Client(transport=transport, fetch_schema_from_transport=False)

    query = gql('''
        query CRMReport {
          totals {
            customers
            orders
            revenue
          }
        }
    ''')

    try:
        data = client.execute(query)
        totals = data.get("totals", {}) if data else {}
        customers = totals.get("customers", 0)
        orders = totals.get("orders", 0)
        revenue = totals.get("revenue", 0)
    except Exception:
        customers = orders = 0
        revenue = 0

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{now} - Report: {customers} customers, {orders} orders, {revenue} revenue\n")
