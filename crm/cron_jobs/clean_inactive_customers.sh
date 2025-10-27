    #!/bin/bash
    # Deletes customers with no orders since a year ago and logs the count.
    # Run from repo root (where manage.py lives) or adjust the cd path below.
    set -euo pipefail

    REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
    cd "$REPO_ROOT"

    LOG_FILE="/tmp/customer_cleanup_log.txt"
    TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"

    COUNT=$(python manage.py shell <<'PYCODE'
from django.utils import timezone
from datetime import timedelta
try:
    from crm.models import Customer, Order
except Exception as e:
    print(0)
else:
    cutoff = timezone.now() - timedelta(days=365)
    # Customers that do NOT have orders within the last year
    qs = Customer.objects.exclude(order__order_date__gte=cutoff).distinct()
    deleted = qs.count()
    qs.delete()
    print(deleted)
PYCODE
    )

    echo "$TIMESTAMP deleted_customers=$COUNT" >> "$LOG_FILE"
