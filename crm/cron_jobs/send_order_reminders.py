#!/usr/bin/env python3
"""
send_order_reminders.py
Queries a GraphQL endpoint for orders within the last 7 days and logs reminders.
"""
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    from gql import gql, Client
    from gql.transport.requests import RequestsHTTPTransport
except Exception as e:
    print("Missing dependency 'gql'. Please add it to requirements and install.", file=sys.stderr)
    sys.exit(1)

ENDPOINT = "http://localhost:8000/graphql"
LOG_FILE = Path("/tmp/order_reminders_log.txt")

transport = RequestsHTTPTransport(url=ENDPOINT, verify=False, retries=3, timeout=20)
client = Client(transport=transport, fetch_schema_from_transport=False)

cutoff = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")

query = gql(
    '''
    query RecentOrders($since: DateTime!) {
      orders(since: $since) {
        id
        customerEmail
        orderDate
      }
    }
    '''
)

try:
    result = client.execute(query, variable_values={"since": cutoff})
    orders = result.get("orders", []) or []
except Exception as e:
    orders = []

now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
with LOG_FILE.open("a", encoding="utf-8") as f:
    for o in orders:
        oid = o.get("id")
        email = o.get("customerEmail")
        f.write(f"{now} reminder_for_order_id={oid} email={email}\n")

print("Order reminders processed!")
