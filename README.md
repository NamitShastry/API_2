# AeroIndex / FareOS

> **Real-Time Airfare Price Intelligence & Daily Index Platform for India**
> An enterprise-grade, high-frequency airfare intelligence system replacing manual, slow airfare reporting with an automated, robust Jevons elementary price index and continuous streaming price signals.

---

## 1. System Overview

AeroIndex operates across two distinct real-time dimensions:
1. **Continuous Live Observation Layer**: Ingests freshly observed flight quotes from airlines, OTAs, and the calibrated continuous simulator into the pipeline with sub-second timestamps and latency tracking.
2. **Real-Time FLASH Index**: Continuous index recalculation using an atomic Redis pipeline with sub-second publication over WebSockets to dashboards and enterprise consumers.
3. **Official Daily Settlement**: Methodology-grounded daily index freeze at 23:30 IST based on the four scheduled collection cycles (00:30, 06:30, 12:30, 18:30 IST) with an 80% coverage guard.

---

## 2. Architecture & Data Flow

```text
[Airlines / OTAs / Calibrated Simulator]
                  │
                  ▼
         Unified Collector (Live & Scheduled)
                  │
                  ▼
         Cleaning & Deduplication Engine (R01-R12)
                  │
                  ▼
   ┌──────────────┴────────────────────────┐
   ▼                                       ▼
PostgreSQL (Raw/Clean Quotes)       Redis FLASH Engine (Sub-second)
                                           │
                                           ▼
                                   IndexTick Publication
                                           │
                                           ▼
                                 WebSocket Channel
                                           │
                                           ▼
                             Next.js 14 Mission Control UI
```

---

## 3. Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- PostgreSQL 15+ and Redis 7+ (or Docker)

### Setup
```bash
# Copy environment configuration
cp .env.example .env

# Install dependencies and prepare DB
make setup

# Run migrations and seed data
make migrate
make seed

# Run backend API and Next.js frontend
make dev
```

---

## 4. Operational Modes
- `LIVE`: Live web scraping adapter enabled (requires proxy pool and headless browsers).
- `SIMULATED_LIVE`: Deterministic synthetic simulator generating realistic Indian domestic flight price quotes at configurable tick frequencies with realistic seasonality, lead-time elasticity, and carrier behaviors.
- `REPLAY`: Historical replay for backtesting and algorithm validation.

---

## 5. Security & Governance
- **Authentication**: Argon2id password hashing, JWT token rotation, TOTP MFA.
- **RBAC**: 10 hierarchical and functional roles.
- **Data Governance**: Tamper-evident hash-chained audit log, automated provenance tracking ("Reproduce this number").

---

## 6. Government-Grade Data API (v1) | ₹0 Budget Architecture (SIH 2026)

AeroIndex provides a versioned, machine-readable REST API designed for potential institutional consumers including the **Reserve Bank of India (RBI)**, **National Statistical Office (NSO / MoSPI)**, and **Directorate General of Civil Aviation (DGCA)**.

### A. Core Endpoints & Implementation Status

All endpoints adhere to a standardized 4-key JSON response envelope (`success`, `data`, `meta`, `error`).

| Endpoint | HTTP | Access | Availability | Freshness SLA | Description |
|:---|:---:|:---:|:---:|:---:|:---|
| `/api/v1/health` | GET | Public | **Class A (Full)** | Real-time | Subsystem health, freshness, e2e latency, data lineage |
| `/api/v1/metadata` | GET | Public | **Class A (Full)** | Static / Versioned | Complete dataset catalogue, methodology definitions, units |
| `/api/v1/openapi.json` | GET | Public | **Class A (Full)** | Versioned | Machine-readable OpenAPI 3.1.0 specification |
| `/api/v1/index/latest` | GET | Public | **Class A (Full)** | Real-time (sub-sec) | Latest National Composite & Metro indices (FLASH & OFFICIAL) |
| `/api/v1/index/history` | GET | Institutional | **Class A (Full)** | Daily 23:30 IST | Paginated historical daily settlement series |
| `/api/v1/routes` | GET | Institutional | **Class A (Full)** | 15-minute | Top-20 official DGCA passenger volume-weighted basket routes |
| `/api/v1/routes/{route_id}` | GET | Institutional | **Class A (Full)** | 15-minute | Route corridor detail, carrier spreads, advance lead curve |
| `/api/v1/routes/{route_id}/history` | GET | Institutional | **Class A (Full)** | Daily | Route-specific historical median fare and index trend |
| `/api/v1/carriers` | GET | Institutional | **Class A (Full)** | Continuous | 5 operating airlines: DGCA market share vs basket weight |
| `/api/v1/carriers/{carrier_id}`| GET | Institutional | **Class A (Full)** | Continuous | Carrier fleet, volatility, corridor coverage, contribution |
| `/api/v1/attribution/latest` | GET | Institutional | **Class A (Full)** | Daily + Flash | What-Moved waterfall (+145 bps) with exact reconciliation |
| `/api/v1/attribution/history`| GET | Institutional | **Class B (Limited)**| Daily | Historical daily driver attribution snapshots |
| `/api/v1/coverage` | GET | Institutional | **Class A (Full)** | 1-minute | National Observability (12,842 universe, 80% guard pass) |
| `/api/v1/anomalies` | GET | Institutional | **Class A (Full)** | Real-time | Modified Z-score with MAD (3.0 sigma, non-causal statement)|
| `/api/v1/provenance/{id}` | GET | Institutional | **Class A (Full)** | Immutable | Forensic cryptographic certificate & SHA-256 replay proof |
| `/api/docs` | GET | Public | **Class A (Full)** | Versioned | Interactive institutional HTML documentation dashboard |

*Data Availability Classification:*
- **Class A:** Fully supported by existing data and calculations in active codebase.
- **Class B:** Supported with limited historical fields.
- **Class C:** Derived on-demand using existing raw observation tables.
- **Class D:** Unavailable / honestly excluded (never fabricated).

---

### B. Institutional Authentication & Pre-Configured Keys

Institutional endpoints require an API Key passed via `X-API-Key: <key>` or `Authorization: Bearer <key>`. Keys are verified server-side against SHA-256 hashes (never stored in plaintext).

| Pre-Seeded Key | Organization / Institution | Scope Tier | Rate Limit |
|:---|:---|:---|:---:|
| `aero_eval_sandbox_key` | **SIH 2026 Evaluation Jury & Auditors** | `SANDBOX_EVALUATION` | 120 req/min |
| `aero_inst_rbi_research_2026` | **Reserve Bank of India (DEPR - Monetary Policy)** | `INSTITUTIONAL_CENTRAL_BANK` | 300 req/min |
| `aero_inst_nso_stat_2026` | **National Statistical Office (MoSPI - CPI Division)** | `INSTITUTIONAL_STATISTICAL_OFFICE` | 300 req/min |

*Security Enforcement:* Unauthenticated requests to protected endpoints return `401 UNAUTHORIZED` with the standard error envelope. Public endpoints (`/health`, `/metadata`, `/index/latest`, `/openapi.json`) permit unauthenticated access with a 60 req/min rate limit.

---

### C. Zero-Cost Infrastructure Statement (₹0 Budget)

AeroIndex strictly satisfies the SIH 2026 ₹0 budget constraint:
1. **Zero External Paid APIs:** Flight discovery and price intelligence pipelines are self-contained without commercial flight aggregators or RapidAPI subscriptions.
2. **Zero Paid LLM / AI Tokens:** Analytics are generated via deterministic quantitative econometrics (Jevons geometric mean, Modified Z-score with MAD, and Holt-Winters ETS).
3. **Zero Paid Gateways:** Rate limiting, token verification, and routing run natively in standard library Node.js and Python.
4. **Zero Cloud Database Hosting Costs:** Operates 100% within free-tier limits on Vercel, Docker, and standard developer workstations.

---

### D. Automated Testing & Verification

AeroIndex includes comprehensive automated test suites verifying mathematical consistency, API security, and response envelopes:

```bash
# Run Python backend test suite (38 tests)
python3 services/api/run_tests.py

# Run Node.js API test suite (16 tests)
node services/web/test_api.js
```
*Total: 54 automated tests passing with 0 failures.*

---

### E. SIH 2026 Jury Demonstration Checklist

1. **API Command Header & Telemetry:** Navigate to **Workspace → Tab 30 (Government API & Data Access)**. Observe live operational state, latency, and auth scope.
2. **Interactive API Explorer:**
   - Select `GET /api/v1/index/latest` and click **Execute Request**. View sub-second response, latency, and lead-time curve.
   - Select `GET /api/v1/attribution/latest`. Observe exact mathematical reconciliation (`113.37 + 109 bps + 36 bps = 114.82`).
   - Select `GET /api/v1/anomalies`. Verify Modified Z-Score calculation and strictly non-causal evidence statement.
3. **Security & Auth Enforcement:**
   - In the API Explorer, switch auth key to `Unauthenticated` and execute `GET /api/v1/routes`. Verify instant `401 UNAUTHORIZED` rejection with standard error envelope.
   - Switch back to `aero_eval_sandbox_key` and verify immediate `200 OK` authorization.
4. **External CLI Execution:** Run the automated Python client demonstration script:
   ```bash
   python3 examples/institutional_client.py http://localhost:8080 aero_eval_sandbox_key
   ```
5. **OpenAPI 3.1 & Interactive Docs:**
   - Open `/api/v1/openapi.json` to inspect raw machine-readable JSON specification.
   - Open `/api/docs` to inspect interactive Swagger-style documentation.
