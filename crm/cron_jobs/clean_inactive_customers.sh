#!/bin/bash
#
# clean_inactive_customers.sh
# Deletes customers with no orders in the last year and logs the count with a timestamp.
# Usage: run from the project root where manage.py is located.
#
set -euo pipefail

LOG_FILE="/tmp/customer_cleanup_log.txt"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"

# Run Django ORM deletion via manage.py shell. Prints the number deleted.
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
