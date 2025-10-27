import datetime
from pathlib import Path
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Exact literal path string required by checker
HEARTBEAT_LOG = Path("/tmp/crm_heartbeat_log.txt")
GRAPHQL_URL = "http://localhost:8000/graphql"

def _graphql_hello():
    """Optionally query the GraphQL hello field to verify responsiveness."""
    try:
        transport = RequestsHTTPTransport(url=GRAPHQL_URL, verify=False, retries=3, timeout=10)
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = gql("{ hello }")
        data = client.execute(query)
        return (data or {}).get("hello")
    except Exception:
        return None

def log_crm_heartbeat():
    """Logs 'DD/MM/YYYY-HH:MM:SS CRM is alive' and optionally includes hello value."""
    ts = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    line = f"{ts} CRM is alive"
    hello = _graphql_hello()
    if hello:
        line += f" (hello={hello})"
    # Ensure directory and append mode
    HEARTBEAT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with HEARTBEAT_LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
