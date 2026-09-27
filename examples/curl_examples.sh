#!/usr/bin/env bash
# ==============================================================================
# AeroIndex / FareOS — Government & Institutional REST API cURL Examples
# Consumers: RBI (DEPR), NSO (MoSPI), DGCA, Macroeconomic Researchers
# ==============================================================================

set -e
BASE_URL="${1:-http://localhost:8080}"
API_KEY="${2:-aero_eval_sandbox_key}"

echo "======================================================================"
echo "AeroIndex / FareOS — Government Data API cURL Demonstration"
echo "Base URL: ${BASE_URL}"
echo "API Key:  ${API_KEY}"
echo "======================================================================"

echo -e "\n1. System Health & Telemetry (Public)"
curl -s "${BASE_URL}/api/v1/health" | head -n 25

echo -e "\n\n2. Dataset & Methodology Metadata Catalogue (Public)"
curl -s "${BASE_URL}/api/v1/metadata" | head -n 35

echo -e "\n\n3. Latest Published Index (Public)"
curl -s "${BASE_URL}/api/v1/index/latest?series_id=APIX-NAT-COMP&publication_status=FLASH" | head -n 30

echo -e "\n\n4. Historical Daily Index Series (Institutional)"
curl -s -H "X-API-Key: ${API_KEY}" "${BASE_URL}/api/v1/index/history?limit=5&page=1" | head -n 30

echo -e "\n\n5. Monitored Top-20 Basket Routes (Institutional)"
curl -s -H "X-API-Key: ${API_KEY}" "${BASE_URL}/api/v1/routes?limit=3" | head -n 30

echo -e "\n\n6. Specific Route Intelligence: DEL-BOM (Institutional)"
curl -s -H "X-API-Key: ${API_KEY}" "${BASE_URL}/api/v1/routes/DEL-BOM" | head -n 35

echo -e "\n\n7. Carrier Market Share vs Basket Share (Institutional)"
curl -s -H "X-API-Key: ${API_KEY}" "${BASE_URL}/api/v1/carriers" | head -n 35

echo -e "\n\n8. What-Moved Attribution Decomposition (+145 bps) (Institutional)"
curl -s -H "X-API-Key: ${API_KEY}" "${BASE_URL}/api/v1/attribution/latest" | head -n 35

echo -e "\n\n9. National Coverage & Observability NCO-2026.1 (Institutional)"
curl -s -H "X-API-Key: ${API_KEY}" "${BASE_URL}/api/v1/coverage" | head -n 35

echo -e "\n\n10. Pricing Anomalies via Modified Z-score (Institutional)"
curl -s -H "X-API-Key: ${API_KEY}" "${BASE_URL}/api/v1/anomalies?route_id=DEL-BOM" | head -n 35

echo -e "\n\n11. Forensic Provenance & SHA-256 Audit Certificate (Institutional)"
curl -s -H "X-API-Key: ${API_KEY}" "${BASE_URL}/api/v1/provenance/APIX-2026-09-27" | head -n 35

echo -e "\n\n12. Security Test: Unauthorized Request (Expected 401)"
curl -s "${BASE_URL}/api/v1/routes" | head -n 25

echo -e "\n======================================================================"
echo "cURL Demonstration Complete."
echo "======================================================================"
