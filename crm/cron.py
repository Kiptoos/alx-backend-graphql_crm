import datetime
from pathlib import Path
import requests

HEARTBEAT_LOG = Path("/tmp/crm_heartbeat_log.txt")
GRAPHQL_URL = "http://localhost:8000/graphql"

def log_crm_heartbeat():
    """Append a heartbeat line and optionally ping GraphQL 'hello'."""
    ts = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    line = f"{ts} CRM is alive"
    try:
        # Optional GraphQL health ping
        r = requests.post(GRAPHQL_URL, json={"query": "{ hello }"}, timeout=5)
        if r.ok:
            data = r.json()
            hello = (data.get("data") or {}).get("hello")
            if hello:
                line += f" (hello={hello})"
    except Exception:
        # ignore connectivity errors to avoid failing the cron
        pass
    HEARTBEAT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with HEARTBEAT_LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def update_low_stock():
    """Invokes the UpdateLowStockProducts mutation and logs updates."""
    from pathlib import Path
    import datetime
    import requests

    url = GRAPHQL_URL
    log = Path("/tmp/low_stock_updates_log.txt")
    mutation = {"query": "mutation { updateLowStockProducts { success updatedProducts { name stock } } }"}
    try:
        resp = requests.post(url, json=mutation, timeout=20)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if resp.ok:
            data = resp.json().get("data", {}) or {}
            upd = (data.get("updateLowStockProducts") or {}).get("updatedProducts", []) or []
            with log.open("a", encoding="utf-8") as f:
                for p in upd:
                    f.write(f"{now} updated name={p.get('name')} stock={p.get('stock')}\n")
        else:
            with log.open("a", encoding="utf-8") as f:
                f.write(f"{now} update failed status={resp.status_code}\n")
    except Exception as e:
        # swallow errors to keep cron robust, but still log
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with log.open("a", encoding="utf-8") as f:
            f.write(f"{now} update exception={e}\n")
