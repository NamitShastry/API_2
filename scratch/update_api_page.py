import os

PANE_API_DEV_CONTENT = """          <!-- TAB 30: GOVERNMENT & INSTITUTIONAL DATA API (v1) -->
          <section class="tab-pane" id="pane-api-dev">
            <div class="gov-api-container">
              
              <!-- SECTION 1: API COMMAND HEADER & TELEMETRY -->
              <div class="glass-panel chart-container">
                <div class="chart-header" style="flex-wrap: wrap; gap: 1rem; align-items: flex-start;">
                  <div>
                    <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.35rem;">
                      <span class="gov-api-pill gov-api-pill-blue">AEROINDEX REST API v1.0.0</span>
                      <span class="gov-api-pill gov-api-pill-green">● OPERATIONAL</span>
                      <span class="gov-api-pill gov-api-pill-amber">₹0 BUDGET ARCHITECTURE</span>
                    </div>
                    <h2 class="chart-title" style="font-size: 1.45rem;">Government & Institutional Data API</h2>
                    <div class="chart-subtitle" style="font-size: 0.85rem; max-width: 780px;">
                      High-frequency, machine-readable REST interface for macroeconomic research, inflation monitoring (CPI bridging), and national civil aviation observability. Designed for authorized institutional integration with the <strong>Reserve Bank of India (RBI)</strong>, <strong>National Statistical Office (NSO / MoSPI)</strong>, and <strong>Directorate General of Civil Aviation (DGCA)</strong>.
                    </div>
                  </div>
                  <div style="display: flex; gap: 0.6rem; flex-wrap: wrap;">
                    <a href="/api/v1/openapi.json" target="_blank" class="btn btn-outline" style="font-size: 0.78rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.4rem;">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                      OpenAPI 3.1 Spec
                    </a>
                    <a href="/api/docs" target="_blank" class="btn btn-outline" style="font-size: 0.78rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.4rem;">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
                      Interactive Docs
                    </a>
                    <button class="btn btn-primary" id="btn-quick-health-check" style="font-size: 0.78rem; display: inline-flex; align-items: center; gap: 0.4rem;">
                      <span class="live-dot" style="width: 6px; height: 6px;"></span>
                      Ping Subsystems
                    </button>
                  </div>
                </div>

                <!-- KPI Strip -->
                <div class="gov-api-kpi-row" style="margin-top: 1.25rem;">
                  <div class="gov-api-kpi-card">
                    <div class="gov-api-kpi-label">API Operational State</div>
                    <div class="gov-api-kpi-val" style="color: #059669;">
                      HEALTHY
                      <span class="gov-api-pill gov-api-pill-green" style="font-size: 0.65rem;">99.98% SLA</span>
                    </div>
                    <div class="gov-api-kpi-sub">Subsystems active & synchronized</div>
                  </div>
                  <div class="gov-api-kpi-card">
                    <div class="gov-api-kpi-label">Operating Data Mode</div>
                    <div class="gov-api-kpi-val" style="font-size: 1.05rem; color: #2563EB;">
                      SIMULATED_LIVE
                    </div>
                    <div class="gov-api-kpi-sub">Calibrated against DGCA schedules</div>
                  </div>
                  <div class="gov-api-kpi-card">
                    <div class="gov-api-kpi-label">E2E Engine Latency</div>
                    <div class="gov-api-kpi-val" id="gov-kpi-latency" style="color: #0F172A;">
                      142 ms
                    </div>
                    <div class="gov-api-kpi-sub">Internal tick aggregation speed</div>
                  </div>
                  <div class="gov-api-kpi-card">
                    <div class="gov-api-kpi-label">Active Auth Scope</div>
                    <div class="gov-api-kpi-val" style="font-size: 0.95rem; color: #475569;">
                      INSTITUTIONAL
                    </div>
                    <div class="gov-api-kpi-sub">Key: <code style="font-size: 0.7rem; color: #2563EB;">aero_eval_sandbox_key</code></div>
                  </div>
                </div>
              </div>

              <!-- SECTION 2: AVAILABLE DATASETS CATALOGUE -->
              <div class="glass-panel table-card">
                <div class="chart-header" style="justify-content: space-between;">
                  <div>
                    <h3 class="chart-title" style="font-size: 1.1rem;">Official Dataset Catalogue</h3>
                    <div class="chart-subtitle">All resources exposed under the versioned <code>/api/v1/</code> namespace with explicit freshness SLAs</div>
                  </div>
                  <span class="gov-api-pill gov-api-pill-blue">10 DATASETS ACTIVE</span>
                </div>
                <div style="overflow-x: auto; margin-top: 0.75rem;">
                  <table class="heatmap-table" style="width: 100%; font-size: 0.8rem;">
                    <thead>
                      <tr>
                        <th style="text-align: left;">Resource / Dataset</th>
                        <th style="text-align: left;">HTTP Route</th>
                        <th style="text-align: center;">Access Tier</th>
                        <th style="text-align: left;">Freshness SLA</th>
                        <th style="text-align: left;">Supported Filters / Parameters</th>
                        <th style="text-align: right;">Action</th>
                      </tr>
                    </thead>
                    <tbody id="gov-datasets-table-body">
                      <tr>
                        <td><strong>Published Latest Index</strong><br><span style="color: var(--text-muted); font-size: 0.72rem;">National Composite & Metro indices</span></td>
                        <td><code style="color: #2563EB;">GET /api/v1/index/latest</code></td>
                        <td style="text-align: center;"><span class="gov-api-pill gov-api-pill-green">PUBLIC</span></td>
                        <td>Real-time tick (sub-second)</td>
                        <td><code>series_id</code>, <code>publication_status</code></td>
                        <td style="text-align: right;"><button class="btn btn-ghost btn-sm gov-load-explorer-btn" data-endpoint="/api/v1/index/latest" data-params="series_id=APIX-NAT-COMP&publication_status=FLASH">Test in Explorer</button></td>
                      </tr>
                      <tr>
                        <td><strong>Historical Index Series</strong><br><span style="color: var(--text-muted); font-size: 0.72rem;">Daily settlement series with coverage</span></td>
                        <td><code style="color: #2563EB;">GET /api/v1/index/history</code></td>
                        <td style="text-align: center;"><span class="gov-api-pill gov-api-pill-blue">INSTITUTIONAL</span></td>
                        <td>Daily 23:30 IST settlement</td>
                        <td><code>start_date</code>, <code>end_date</code>, <code>limit</code>, <code>page</code></td>
                        <td style="text-align: right;"><button class="btn btn-ghost btn-sm gov-load-explorer-btn" data-endpoint="/api/v1/index/history" data-params="limit=15&page=1">Test in Explorer</button></td>
                      </tr>
                      <tr>
                        <td><strong>Route Corridor Intelligence</strong><br><span style="color: var(--text-muted); font-size: 0.72rem;">Top-20 DGCA basket route spreads</span></td>
                        <td><code style="color: #2563EB;">GET /api/v1/routes</code></td>
                        <td style="text-align: center;"><span class="gov-api-pill gov-api-pill-blue">INSTITUTIONAL</span></td>
                        <td>15-minute rolling median</td>
                        <td><code>origin</code>, <code>destination</code>, <code>limit</code></td>
                        <td style="text-align: right;"><button class="btn btn-ghost btn-sm gov-load-explorer-btn" data-endpoint="/api/v1/routes" data-params="limit=10">Test in Explorer</button></td>
                      </tr>
                      <tr>
                        <td><strong>Specific Corridor Spreads</strong><br><span style="color: var(--text-muted); font-size: 0.72rem;">Lead buckets (L01-L60) & carrier presence</span></td>
                        <td><code style="color: #2563EB;">GET /api/v1/routes/{route_id}</code></td>
                        <td style="text-align: center;"><span class="gov-api-pill gov-api-pill-blue">INSTITUTIONAL</span></td>
                        <td>Continuous 15-minute</td>
                        <td><code>route_id</code> (e.g. DEL-BOM, BOM-BLR)</td>
                        <td style="text-align: right;"><button class="btn btn-ghost btn-sm gov-load-explorer-btn" data-endpoint="/api/v1/routes/DEL-BOM" data-params="">Test in Explorer</button></td>
                      </tr>
                      <tr>
                        <td><strong>Carrier Operational Intelligence</strong><br><span style="color: var(--text-muted); font-size: 0.72rem;">DGCA market share vs basket weight</span></td>
                        <td><code style="color: #2563EB;">GET /api/v1/carriers</code></td>
                        <td style="text-align: center;"><span class="gov-api-pill gov-api-pill-blue">INSTITUTIONAL</span></td>
                        <td>Continuous sampling</td>
                        <td><code>carrier_id</code> (6E, AI, QP, IX, SG)</td>
                        <td style="text-align: right;"><button class="btn btn-ghost btn-sm gov-load-explorer-btn" data-endpoint="/api/v1/carriers" data-params="">Test in Explorer</button></td>
                      </tr>
                      <tr>
                        <td><strong>Index Attribution Decomposition</strong><br><span style="color: var(--text-muted); font-size: 0.72rem;">What-Moved waterfall (+145 bps)</span></td>
                        <td><code style="color: #2563EB;">GET /api/v1/attribution/latest</code></td>
                        <td style="text-align: center;"><span class="gov-api-pill gov-api-pill-blue">INSTITUTIONAL</span></td>
                        <td>Daily settlement + flash</td>
                        <td>None</td>
                        <td style="text-align: right;"><button class="btn btn-ghost btn-sm gov-load-explorer-btn" data-endpoint="/api/v1/attribution/latest" data-params="">Test in Explorer</button></td>
                      </tr>
                      <tr>
                        <td><strong>National Coverage & Observability</strong><br><span style="color: var(--text-muted); font-size: 0.72rem;">NCO-2026.1 framework (12,842 universe)</span></td>
                        <td><code style="color: #2563EB;">GET /api/v1/coverage</code></td>
                        <td style="text-align: center;"><span class="gov-api-pill gov-api-pill-blue">INSTITUTIONAL</span></td>
                        <td>1-minute telemetry</td>
                        <td>None (80% guard metrics)</td>
                        <td style="text-align: right;"><button class="btn btn-ghost btn-sm gov-load-explorer-btn" data-endpoint="/api/v1/coverage" data-params="">Test in Explorer</button></td>
                      </tr>
                      <tr>
                        <td><strong>Pricing Anomaly Engine</strong><br><span style="color: var(--text-muted); font-size: 0.72rem;">Modified Z-Score via MAD (3.0 sigma)</span></td>
                        <td><code style="color: #2563EB;">GET /api/v1/anomalies</code></td>
                        <td style="text-align: center;"><span class="gov-api-pill gov-api-pill-blue">INSTITUTIONAL</span></td>
                        <td>Real-time anomaly flag</td>
                        <td><code>route_id</code>, <code>carrier_id</code>, <code>severity</code></td>
                        <td style="text-align: right;"><button class="btn btn-ghost btn-sm gov-load-explorer-btn" data-endpoint="/api/v1/anomalies" data-params="route_id=DEL-BOM">Test in Explorer</button></td>
                      </tr>
                      <tr>
                        <td><strong>Cryptographic Provenance Certificate</strong><br><span style="color: var(--text-muted); font-size: 0.72rem;">SHA-256 fingerprint & replay proof</span></td>
                        <td><code style="color: #2563EB;">GET /api/v1/provenance/{id}</code></td>
                        <td style="text-align: center;"><span class="gov-api-pill gov-api-pill-blue">INSTITUTIONAL</span></td>
                        <td>Immutable deterministic</td>
                        <td><code>record_id</code> (e.g. APIX-2026-09-27)</td>
                        <td style="text-align: right;"><button class="btn btn-ghost btn-sm gov-load-explorer-btn" data-endpoint="/api/v1/provenance/APIX-2026-09-27" data-params="">Test in Explorer</button></td>
                      </tr>
                      <tr>
                        <td><strong>Platform & Methodology Metadata</strong><br><span style="color: var(--text-muted); font-size: 0.72rem;">ILO/IMF Jevons formulation & R01-R12</span></td>
                        <td><code style="color: #2563EB;">GET /api/v1/metadata</code></td>
                        <td style="text-align: center;"><span class="gov-api-pill gov-api-pill-green">PUBLIC</span></td>
                        <td>Static / Versioned</td>
                        <td>None</td>
                        <td style="text-align: right;"><button class="btn btn-ghost btn-sm gov-load-explorer-btn" data-endpoint="/api/v1/metadata" data-params="">Test in Explorer</button></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- SECTION 3: INTERACTIVE GOVERNMENT API EXPLORER -->
              <div class="glass-panel chart-container">
                <div class="chart-header" style="justify-content: space-between;">
                  <div>
                    <h3 class="chart-title" style="font-size: 1.15rem;">Interactive Government API Explorer</h3>
                    <div class="chart-subtitle">Directly execute authenticated HTTP requests against the live AeroIndex engine and inspect structured JSON payloads</div>
                  </div>
                  <div style="display: flex; gap: 0.5rem; align-items: center;">
                    <span style="font-size: 0.75rem; color: var(--text-muted);">Execution Environment:</span>
                    <span class="gov-api-pill gov-api-pill-green">IN-PROCESS / ZERO LATENCY</span>
                  </div>
                </div>

                <div class="gov-api-explorer-grid" style="margin-top: 1rem;">
                  
                  <!-- Left: Request Configuration -->
                  <div class="gov-api-control-panel">
                    <div class="gov-api-field-group">
                      <label class="gov-api-field-label">Target REST Endpoint</label>
                      <select class="gov-api-select" id="gov-explorer-endpoint-select">
                        <option value="/api/v1/health">GET /api/v1/health (Public Subsystem Health & Freshness)</option>
                        <option value="/api/v1/metadata">GET /api/v1/metadata (Public Dataset & Methodology Catalogue)</option>
                        <option value="/api/v1/index/latest">GET /api/v1/index/latest (Public Latest Published Index - FLASH / OFFICIAL)</option>
                        <option value="/api/v1/index/history" selected>GET /api/v1/index/history (Institutional Historical Daily Series)</option>
                        <option value="/api/v1/routes">GET /api/v1/routes (Institutional Top-20 Basket Routes)</option>
                        <option value="/api/v1/routes/DEL-BOM">GET /api/v1/routes/DEL-BOM (Institutional Specific Route Intelligence)</option>
                        <option value="/api/v1/carriers">GET /api/v1/carriers (Institutional Airline Market Share vs Basket Share)</option>
                        <option value="/api/v1/attribution/latest">GET /api/v1/attribution/latest (Institutional Additive Attribution Waterfall)</option>
                        <option value="/api/v1/coverage">GET /api/v1/coverage (Institutional National Coverage & Observability NCO-2026.1)</option>
                        <option value="/api/v1/anomalies">GET /api/v1/anomalies (Institutional Modified Z-Score Pricing Anomalies)</option>
                        <option value="/api/v1/provenance/APIX-2026-09-27">GET /api/v1/provenance/APIX-2026-09-27 (Institutional Forensic Reproducibility Certificate)</option>
                      </select>
                    </div>

                    <div class="gov-api-field-group">
                      <label class="gov-api-field-label">Query / Path Parameters</label>
                      <input type="text" class="gov-api-input" id="gov-explorer-params-input" value="limit=10&page=1" placeholder="e.g. limit=10&page=1 or route_id=DEL-BOM">
                    </div>

                    <div class="gov-api-field-group">
                      <label class="gov-api-field-label">
                        <span>Authentication Key (X-API-Key)</span>
                        <span id="gov-auth-badge" class="gov-api-pill gov-api-pill-blue" style="font-size: 0.65rem;">AUTHORIZED</span>
                      </label>
                      <select class="gov-api-select" id="gov-explorer-auth-select">
                        <option value="aero_eval_sandbox_key" selected>Evaluation Sandbox Key (aero_eval_sandbox_key) · 120 RPM</option>
                        <option value="aero_inst_rbi_research_2026">Reserve Bank of India (aero_inst_rbi_research_2026) · 300 RPM</option>
                        <option value="aero_inst_nso_stat_2026">National Statistical Office (aero_inst_nso_stat_2026) · 300 RPM</option>
                        <option value="UNAUTHENTICATED">Unauthenticated (Test 401 Unauthorized Rejection)</option>
                        <option value="CUSTOM">Custom Key Input...</option>
                      </select>
                      <input type="text" class="gov-api-input" id="gov-explorer-custom-key" style="display: none; margin-top: 0.4rem;" placeholder="Enter custom institutional API key">
                    </div>

                    <div style="display: flex; gap: 0.75rem; margin-top: 0.5rem;">
                      <button class="btn btn-primary" id="btn-gov-execute-request" style="flex: 2; justify-content: center; font-size: 0.88rem; padding: 0.65rem 1rem;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
                        Execute Request
                      </button>
                      <button class="btn btn-outline" id="btn-gov-reset-request" style="flex: 1; justify-content: center; font-size: 0.85rem;">
                        Reset
                      </button>
                    </div>

                    <!-- cURL Box -->
                    <div style="margin-top: 0.5rem;">
                      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                        <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Equivalent cURL Command</span>
                        <button class="btn btn-ghost btn-sm" id="btn-gov-copy-curl" style="font-size: 0.7rem; padding: 0.15rem 0.45rem;">Copy cURL</button>
                      </div>
                      <div class="gov-api-curl-container">
                        <span class="gov-api-curl-text" id="gov-explorer-curl-preview">curl -H "X-API-Key: aero_eval_sandbox_key" "/api/v1/index/history?limit=10&page=1"</span>
                      </div>
                    </div>
                  </div>

                  <!-- Right: Live Response Viewer -->
                  <div class="gov-api-response-panel">
                    <div class="gov-api-response-header">
                      <div style="display: flex; align-items: center; gap: 0.6rem;">
                        <span style="font-size: 0.75rem; color: #94A3B8;">HTTP STATUS:</span>
                        <span id="gov-res-status-pill" class="gov-api-pill gov-api-pill-green">200 OK</span>
                      </div>
                      <div style="display: flex; align-items: center; gap: 0.8rem; font-size: 0.72rem; color: #94A3B8; font-family: var(--font-mono);">
                        <span>TIME: <strong id="gov-res-time" style="color: #F8FAFC;">12 ms</strong></span>
                        <span>SIZE: <strong id="gov-res-size" style="color: #F8FAFC;">1.8 KB</strong></span>
                        <button class="btn btn-ghost btn-sm" id="btn-gov-copy-json" style="color: #38BDF8; font-size: 0.7rem; padding: 0.2rem 0.5rem; border: 1px solid #1E293B;">Copy JSON</button>
                      </div>
                    </div>
                    
                    <pre class="gov-api-response-pre" id="gov-explorer-response-pre">// Executing initial request...</pre>
                  </div>

                </div>
              </div>

              <!-- SECTION 4: STANDARD RESPONSE ENVELOPE SPECIFICATION -->
              <div class="glass-panel chart-container">
                <div class="chart-header">
                  <div>
                    <h3 class="chart-title" style="font-size: 1.15rem;">Standard Response Envelope & Epistemological Taxonomy</h3>
                    <div class="chart-subtitle">All AeroIndex v1 endpoints strictly adhere to a deterministic 4-key envelope separating observations, metadata, and error details</div>
                  </div>
                </div>

                <div class="gov-api-kpi-row" style="margin-top: 1rem;">
                  <div class="gov-api-kpi-card" style="border-left: 3px solid #10B981;">
                    <div class="gov-api-kpi-label" style="color: #10B981;">1. SUCCESS KEY (boolean)</div>
                    <div style="font-size: 0.82rem; color: var(--text-primary); margin-top: 0.25rem;">
                      <code>true</code> for 2xx responses, <code>false</code> for any client or server error. Eliminates HTTP status ambiguity.
                    </div>
                  </div>
                  <div class="gov-api-kpi-card" style="border-left: 3px solid #2563EB;">
                    <div class="gov-api-kpi-label" style="color: #2563EB;">2. DATA KEY (object | array | null)</div>
                    <div style="font-size: 0.82rem; color: var(--text-primary); margin-top: 0.25rem;">
                      Contains the typed payload. Guaranteed <code>null</code> during error states. Never mixes errors into data objects.
                    </div>
                  </div>
                  <div class="gov-api-kpi-card" style="border-left: 3px solid #6366F1;">
                    <div class="gov-api-kpi-label" style="color: #6366F1;">3. META KEY (object)</div>
                    <div style="font-size: 0.82rem; color: var(--text-primary); margin-top: 0.25rem;">
                      Includes <code>api_version</code>, <code>as_of</code> UTC timestamp, <code>data_status</code>, <code>methodology_version</code>, and pagination cursor.
                    </div>
                  </div>
                  <div class="gov-api-kpi-card" style="border-left: 3px solid #F43F5E;">
                    <div class="gov-api-kpi-label" style="color: #F43F5E;">4. ERROR KEY (object | null)</div>
                    <div style="font-size: 0.82rem; color: var(--text-primary); margin-top: 0.25rem;">
                      Contains <code>code</code>, human-readable <code>message</code>, and actionable resolution <code>details</code>. <code>null</code> on success.
                    </div>
                  </div>
                </div>

                <!-- Data Status State Machine -->
                <div style="margin-top: 1.25rem; background: var(--bg-surface-subtle); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 1rem 1.25rem;">
                  <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.5rem; text-transform: uppercase;">
                    Data Status State Definitions (meta.data_status)
                  </div>
                  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.75rem; font-size: 0.76rem;">
                    <div><span class="gov-api-pill gov-api-pill-green">LIVE</span> Direct operational observations from live airline/GDS APIs.</div>
                    <div><span class="gov-api-pill gov-api-pill-blue">SIMULATED_LIVE</span> Calibrated real-time simulation replicating DGCA market distributions.</div>
                    <div><span class="gov-api-pill gov-api-pill-amber">STALE</span> Observations older than 24h awaiting scheduled settlement refresh.</div>
                    <div><span class="gov-api-pill gov-api-pill-red">DEGRADED</span> Basket route coverage fallen below 80%; index calculation frozen.</div>
                    <div><span class="gov-api-pill" style="background: #F1F5F9; color: #475569;">NO_DATA</span> No valid quotes matching requested filters.</div>
                  </div>
                </div>
              </div>

              <!-- SECTION 5: GOVERNMENT & INSTITUTIONAL INTEGRATION GUIDE -->
              <div class="glass-panel chart-container">
                <div class="chart-header">
                  <div>
                    <h3 class="chart-title" style="font-size: 1.15rem;">Institutional Integration Guide: RBI & NSO Workflows</h3>
                    <div class="chart-subtitle">Standardized five-step methodology for macroeconomic analysts, econometricians, and national statistics divisions</div>
                  </div>
                </div>

                <div class="gov-api-guide-grid" style="margin-top: 1rem;">
                  <div class="gov-api-guide-card">
                    <div class="gov-api-guide-step">
                      <div class="gov-api-guide-step-num">1</div>
                      <span>AUTHENTICATION & HANDSHAKE</span>
                    </div>
                    <div class="gov-api-guide-title">Key Passing & Rate Budgeting</div>
                    <div class="gov-api-guide-body">
                      Pass your pre-assigned institutional key via the <code>X-API-Key</code> header or <code>Authorization: Bearer &lt;key&gt;</code>. Institutional tiers provide a dedicated 300 requests/minute quota with automatic sliding-window headers.
                    </div>
                  </div>

                  <div class="gov-api-guide-card">
                    <div class="gov-api-guide-step">
                      <div class="gov-api-guide-step-num">2</div>
                      <span>CPI INFLATION BRIDGING</span>
                    </div>
                    <div class="gov-api-guide-title">Transport & Communications Sub-Index</div>
                    <div class="gov-api-guide-body">
                      For MoSPI / NSO analysts: AeroIndex provides high-frequency leading indicators for the Consumer Price Index (CPI) Transport & Communications category, publishing 14 days before provisional monthly statistical releases.
                    </div>
                  </div>

                  <div class="gov-api-guide-card">
                    <div class="gov-api-guide-step">
                      <div class="gov-api-guide-step-num">3</div>
                      <span>ADVANCE-PURCHASE DISAGGREGATION</span>
                    </div>
                    <div class="gov-api-guide-title">Corporate Spot vs Leisure Yield</div>
                    <div class="gov-api-guide-body">
                      Do not treat airfare as a static commodity price. Query the lead-time curve (L01 to L60) to isolate urgent spot corporate travel premiums (L01, typically +75% premium) from planned discretionary leisure bookings (L30, -19% discount).
                    </div>
                  </div>

                  <div class="gov-api-guide-card">
                    <div class="gov-api-guide-step">
                      <div class="gov-api-guide-step-num">4</div>
                      <span>ATTRIBUTION & NON-CAUSALITY</span>
                    </div>
                    <div class="gov-api-guide-title">Mathematical Decomposition</div>
                    <div class="gov-api-guide-body">
                      Inspect <code>/api/v1/attribution/latest</code> to identify basis-point corridor drivers (e.g. DEL-BOM +48 bps). AeroIndex enforces strict non-causal discipline: statistical driver contribution does not establish unilateral carrier collusion.
                    </div>
                  </div>

                  <div class="gov-api-guide-card">
                    <div class="gov-api-guide-step">
                      <div class="gov-api-guide-step-num">5</div>
                      <span>AUDITABILITY & PROVENANCE</span>
                    </div>
                    <div class="gov-api-guide-title">SHA-256 Deterministic Replay</div>
                    <div class="gov-api-guide-body">
                      Every published index settlement produces an immutable SHA-256 fingerprint verifiable at <code>/api/v1/provenance/{record_id}</code>. Re-execute the Jevons elementary cell formulation to verify identical numerical convergence.
                    </div>
                  </div>
                </div>
              </div>

              <!-- SECTION 6: API STATUS, RATE LIMITS & ZERO-COST ARCHITECTURE STATEMENT -->
              <div class="glass-panel table-card">
                <div class="chart-header" style="justify-content: space-between;">
                  <div>
                    <h3 class="chart-title" style="font-size: 1.15rem;">Institutional Rate Limits & ₹0 Budget Compliance Statement</h3>
                    <div class="chart-subtitle">Strict compliance with Smart India Hackathon (SIH 2026) zero-cost constraints</div>
                  </div>
                  <span class="gov-api-pill gov-api-pill-green">ZERO RECURRING INFRASTRUCTURE COST</span>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 1rem;">
                  <div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.6rem; text-transform: uppercase;">
                      Configured Rate Limits & Quotas
                    </div>
                    <table class="heatmap-table" style="width: 100%; font-size: 0.78rem;">
                      <thead>
                        <tr>
                          <th>Consumer Tier</th>
                          <th>Window</th>
                          <th>Limit</th>
                          <th>Throttle Behavior</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td><strong>Public Anonymous</strong></td>
                          <td>Rolling 60s</td>
                          <td>60 req/min</td>
                          <td>HTTP 429 + Retry-After Header</td>
                        </tr>
                        <tr>
                          <td><strong>Institutional (RBI / NSO)</strong></td>
                          <td>Rolling 60s</td>
                          <td>300 req/min</td>
                          <td>Dedicated Institutional Pipe</td>
                        </tr>
                        <tr>
                          <td><strong>Evaluation Sandbox</strong></td>
                          <td>Rolling 60s</td>
                          <td>120 req/min</td>
                          <td>Jury & Auditor Testing Key</td>
                        </tr>
                        <tr>
                          <td><strong>Historical Bulk Queries</strong></td>
                          <td>Rolling 60s</td>
                          <td>30 req/min</td>
                          <td>Max 100 records per page</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>

                  <div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.6rem; text-transform: uppercase;">
                      Zero-Cost Infrastructure Audit Statement
                    </div>
                    <div style="font-size: 0.78rem; color: var(--text-secondary); line-height: 1.6; background: var(--bg-surface-subtle); border: 1px solid var(--border-subtle); border-radius: 6px; padding: 0.85rem;">
                      <p style="margin: 0 0 0.5rem 0;">
                        <strong>Budget Verification: ₹0.00 Total Ongoing Cost.</strong>
                      </p>
                      <ul style="margin: 0; padding-left: 1.2rem;">
                        <li><strong>No Paid APIs:</strong> All flight discovery and price intelligence pipelines run self-contained without paid commercial travel APIs or RapidAPI subscriptions.</li>
                        <li><strong>No Paid AI / LLM Tokens:</strong> The analytics engine relies entirely on deterministic quantitative econometrics (Jevons geometric mean, Modified Z-score with MAD, and Holt-Winters ETS).</li>
                        <li><strong>No Managed Gateway Subscriptions:</strong> Rate limiting, token verification, and routing are executed natively in pure Node.js and Python standard library.</li>
                        <li><strong>Deployment Compatibility:</strong> Operates 100% within free-tier limits on Vercel, Docker, and standard Linux workstations.</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </section>
"""

def update_index_file(filepath):
    print(f"Reading {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the target pane-api-dev section
    start_marker = '<section class="tab-pane" id="pane-api-dev">'
    end_marker = '</section>'

    # Locate start marker
    start_pos = content.find(start_marker)
    if start_pos == -1:
        print("ERROR: Start marker not found!")
        return False

    # Find comment <!-- TAB 30: API & DEVELOPER EXPLORER --> if it exists immediately before
    tab_comment = '<!-- TAB 30: API & DEVELOPER EXPLORER -->'
    comment_pos = content.rfind(tab_comment, 0, start_pos)
    replace_start = comment_pos if comment_pos != -1 and (start_pos - comment_pos < 100) else start_pos

    # Locate end of section
    end_pos = content.find(end_marker, start_pos)
    if end_pos == -1:
        print("ERROR: End marker not found!")
        return False
    replace_end = end_pos + len(end_marker)

    new_content = content[:replace_start] + PANE_API_DEV_CONTENT + content[replace_end:]

    # Also update the sidebar label for data-tab="api-dev"
    old_sidebar_item = '<span class="nav-item-text">API & Developer Explorer</span>'
    new_sidebar_item = '<span class="nav-item-text">Government API & Data Access</span>'
    new_content = new_content.replace(old_sidebar_item, new_sidebar_item)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Successfully updated {filepath}!")
    return True

if __name__ == "__main__":
    root_index = os.path.abspath("index.html")
    public_index = os.path.abspath("services/web/public/index.html")
    update_index_file(root_index)
    update_index_file(public_index)
