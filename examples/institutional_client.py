#!/usr/bin/env python3
"""AeroIndex / FareOS — Institutional Python Demonstration Client.

Demonstrates programmatic data access for government consumers (RBI, NSO/MoSPI, DGCA).
Zero dependencies: built using Python 3 standard library (urllib.request, json).

Usage:
    python3 institutional_client.py [base_url] [api_key]

Default:
    Base URL: http://localhost:8080
    API Key:  aero_eval_sandbox_key
"""

import json
import sys
import time
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "http://localhost:8080"
DEFAULT_API_KEY = "aero_eval_sandbox_key"


class AeroIndexClient:
    def __init__(self, base_url: str = DEFAULT_BASE_URL, api_key: str = DEFAULT_API_KEY):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _request(self, path: str, authenticated: bool = True) -> dict:
        url = f"{self.base_url}{path}"
        headers = {
            "Accept": "application/json",
            "User-Agent": "AeroIndex-Institutional-Client/1.0.0 (Government-Evaluation)",
        }
        if authenticated and self.api_key:
            headers["X-API-Key"] = self.api_key

        req = urllib.request.Request(url, headers=headers)
        start_time = time.perf_counter()
        try:
            with urllib.request.urlopen(req) as resp:
                elapsed_ms = round((time.perf_counter() - start_time) * 1000, 1)
                data = json.loads(resp.read().decode("utf-8"))
                return {"status": resp.status, "elapsed_ms": elapsed_ms, "payload": data}
        except urllib.error.HTTPError as e:
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 1)
            raw = e.read().decode("utf-8")
            try:
                data = json.loads(raw)
            except Exception:
                data = {"raw": raw}
            return {"status": e.code, "elapsed_ms": elapsed_ms, "payload": data}
        except Exception as e:
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 1)
            return {"status": 0, "elapsed_ms": elapsed_ms, "payload": {"error": str(e)}}


def run_demonstration():
    base_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BASE_URL
    api_key = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_API_KEY

    print("=" * 76)
    print("AEROINDEX / FAREOS — GOVERNMENT & INSTITUTIONAL DATA API DEMONSTRATION")
    print("=" * 76)
    print(f"Target Gateway:    {base_url}")
    print(f"Active Credential: {api_key}")
    print(f"Jurisdiction:      Republic of India Domestic Aviation (DGCA Scheduled)")
    print("-" * 76)

    client = AeroIndexClient(base_url, api_key)

    # STEP 1: Discovery & Telemetry
    print("\n[STEP 1/8] DISCOVER API HEALTH & TELEMETRY")
    print("  Endpoint: GET /api/v1/health (Public)")
    res = client._request("/api/v1/health", authenticated=False)
    print(f"  HTTP Status: {res['status']} | Latency: {res['elapsed_ms']} ms")
    if res["status"] == 200:
        d = res["payload"]["data"]
        print(f"  API Status:      {d['api_status']} (v{d['api_version']})")
        print(f"  Operating Mode:  {d['operating_mode']}")
        print(f"  Data Freshness:  {d['data_freshness']}")
        print(f"  Active Sources:  {d['source_coverage']['active_sources']} adapters")

    # STEP 2: Platform Metadata
    print("\n[STEP 2/8] PLATFORM & DATASET METADATA DISCOVERY")
    print("  Endpoint: GET /api/v1/metadata (Public)")
    res = client._request("/api/v1/metadata", authenticated=False)
    print(f"  HTTP Status: {res['status']} | Latency: {res['elapsed_ms']} ms")
    if res["status"] == 200:
        meta = res["payload"]["data"]
        print(f"  Standard:        {meta['methodology_standards']['elementary_aggregation']}")
        print(f"  Coverage Guard:  {meta['methodology_standards']['coverage_guard']}")
        print(f"  Active Series:   {len(meta['supported_series'])} series ({', '.join(s['id'] for s in meta['supported_series'])})")

    # STEP 3: Latest Published Index
    print("\n[STEP 3/8] RETRIEVE LATEST PUBLISHED INDEX (FLASH / OFFICIAL)")
    print("  Endpoint: GET /api/v1/index/latest?series_id=APIX-NAT-COMP (Public)")
    res = client._request("/api/v1/index/latest?series_id=APIX-NAT-COMP", authenticated=False)
    print(f"  HTTP Status: {res['status']} | Latency: {res['elapsed_ms']} ms")
    if res["status"] == 200:
        idx = res["payload"]["data"]
        print(f"  Composite Index: {idx['index_value']} ({idx['change_bps']:+d} bps / {idx['change_percent']:+.2f}%)")
        print(f"  Settlement Tier: {idx['publication_status']} · Coverage: {idx['coverage_pct']}%")
        print(f"  Lead Time Curve: L01={idx['lead_time_disaggregation']['L01']['avg_fare_inr']} INR ({idx['lead_time_disaggregation']['L01']['premium_pct']:+.1f}%) | L30={idx['lead_time_disaggregation']['L30']['avg_fare_inr']} INR ({idx['lead_time_disaggregation']['L30']['premium_pct']:+.1f}%)")

    # STEP 4: Historical Series
    print("\n[STEP 4/8] RETRIEVE PAGINATED HISTORICAL SERIES")
    print("  Endpoint: GET /api/v1/index/history?limit=5&page=1 (Institutional)")
    res = client._request("/api/v1/index/history?limit=5&page=1")
    print(f"  HTTP Status: {res['status']} | Latency: {res['elapsed_ms']} ms")
    if res["status"] == 200:
        points = res["payload"]["data"]["points"]
        pag = res["payload"]["meta"].get("pagination", {})
        print(f"  Records Returned: {len(points)} (Page {pag.get('page')}/{pag.get('total_pages')})")
        for p in points[:3]:
            print(f"    • {p['date']}: {p['index_value']} ({p['change_bps']:+d} bps, {p['coverage_pct']}%) [{p['publication_status']}]")

    # STEP 5: Route Intelligence
    print("\n[STEP 5/8] QUERY CORRIDOR INTELLIGENCE (DEL-BOM)")
    print("  Endpoint: GET /api/v1/routes/DEL-BOM (Institutional)")
    res = client._request("/api/v1/routes/DEL-BOM")
    print(f"  HTTP Status: {res['status']} | Latency: {res['elapsed_ms']} ms")
    if res["status"] == 200:
        route = res["payload"]["data"]
        print(f"  Route:           {route['route_id']} ({route['origin_city']} -> {route['destination_city']})")
        print(f"  DGCA Weight:     {route['dgca_volume_weight'] * 100:.1f}% | Distance: {route['distance_km']} km")
        print(f"  Current Median:  {route['current_median_fare_inr']} INR (Index: {route['route_index']})")
        print(f"  Active Airlines: {', '.join(c['code'] + ' (' + str(c['flight_count']) + ' flt)' for c in route['carriers'])}")

    # STEP 6: Index Attribution Decomposition
    print("\n[STEP 6/8] ADDITIVE ATTRIBUTION WATERFALL RECONCILIATION")
    print("  Endpoint: GET /api/v1/attribution/latest (Institutional)")
    res = client._request("/api/v1/attribution/latest")
    print(f"  HTTP Status: {res['status']} | Latency: {res['elapsed_ms']} ms")
    if res["status"] == 200:
        attr = res["payload"]["data"]
        recon = attr["reconciliation"]
        print(f"  Total Movement:  {attr['total_index_movement_bps']:+d} bps (+{attr['total_index_movement_pts']} pts)")
        print(f"  Reconciliation:  {recon['previous_index']} + ({recon['sum_of_route_contributions_bps']} + {recon['sum_of_carrier_contributions_bps']} + {recon['unexplained_residual_bps']}) = {recon['current_index']} [{recon['reconciliation_status']}]")
        print(f"  Top Route Move:  {attr['route_drivers'][0]['route_id']} ({attr['route_drivers'][0]['impact_bps']:+d} bps) — {attr['route_drivers'][0]['reason']}")
        print(f"  Non-Causality:   \"{attr['epistemological_disclaimer'][:65]}...\"")

    # STEP 7: National Coverage
    print("\n[STEP 7/8] NATIONAL OBSERVABILITY MATRIX (NCO-2026.1)")
    print("  Endpoint: GET /api/v1/coverage (Institutional)")
    res = client._request("/api/v1/coverage")
    print(f"  HTTP Status: {res['status']} | Latency: {res['elapsed_ms']} ms")
    if res["status"] == 200:
        cov = res["payload"]["data"]
        m = cov["coverage_metrics"]
        print(f"  Flight Universe: {cov['market_universe']['total_scheduled_flight_instances']} daily instances across {cov['market_universe']['unique_airports_monitored']} airports")
        print(f"  Schedule Disc.:  {m['schedule_discovery']['pct']}% ({m['schedule_discovery']['numerator']}/{m['schedule_discovery']['denominator']})")
        print(f"  Fare Observ.:    {m['fare_observability']['pct']}% ({m['fare_observability']['numerator']}/{m['fare_observability']['denominator']})")
        print(f"  80% Guard:       {cov['basket_route_coverage']['guard_status']} ({cov['basket_route_coverage']['coverage_pct']}%)")

    # STEP 8: Security Test (Unauthenticated Rejection)
    print("\n[STEP 8/8] SECURITY VERIFICATION: UNAUTHORIZED REJECTION")
    print("  Endpoint: GET /api/v1/routes (WITHOUT Key)")
    res_unauth = client._request("/api/v1/routes", authenticated=False)
    print(f"  HTTP Status: {res_unauth['status']} (Expected: 401 UNAUTHORIZED)")
    if res_unauth["status"] == 401:
        err = res_unauth["payload"].get("error", {})
        print(f"  Security Enforced: code='{err.get('code')}' message='{err.get('message')}'")
        print(f"  Envelope Meta:     success={res_unauth['payload'].get('success')} data_status='{res_unauth['payload']['meta'].get('data_status')}'")

    print("\n" + "=" * 76)
    print("INSTITUTIONAL DEMONSTRATION COMPLETE: ALL DATASETS CONSUMED SUCCESSFULLY")
    print("=" * 76)


if __name__ == "__main__":
    run_demonstration()
