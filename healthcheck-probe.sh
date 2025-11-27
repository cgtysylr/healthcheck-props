#!/bin/bash

# Basit liveness probe script
# Database durumunu kontrol eder

HEALTH_ENDPOINT="http://localhost:8080/health/ready"

# Healthcheck endpoint'inden JSON'u al
health_json=$(curl -s -f "$HEALTH_ENDPOINT" 2>/dev/null)

if [ -z "$health_json" ]; then
    echo "ERROR: Cannot reach health endpoint"
    exit 1
fi

# Database durumunu kontrol et
db_status=$(python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    db_entry = data.get('entries', {}).get('Database', {})
    status = db_entry.get('status', 'Healthy')
    print(status.lower())
except Exception as e:
    print('healthy')
" <<< "$health_json" 2>/dev/null)

# Database unhealthy ise exit 1 (Kubernetes restart edecek)
if [ "$db_status" != "healthy" ]; then
    echo "CRITICAL: Database is unhealthy (status: $db_status)"
    exit 1
fi

# Database healthy
exit 0
