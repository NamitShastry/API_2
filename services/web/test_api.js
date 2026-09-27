/**
 * Automated Test Suite for AeroIndex Government Data API (v1)
 * Tests all endpoints, response envelopes, error handling, rate limiting, and institutional auth.
 */

const assert = require('assert');
const govApi = require('./api_v1_gov');

function createMockReqRes({ pathname, method = 'GET', headers = {}, query = {} }) {
  const req = {
    method,
    headers,
    socket: { remoteAddress: '127.0.0.1' }
  };
  let responseData = '';
  let statusCode = 200;
  const resHeaders = {};

  const res = {
    setHeader: (k, v) => { resHeaders[k.toLowerCase()] = v; },
    writeHead: (code, headersObj) => {
      statusCode = code;
      if (headersObj) {
        Object.entries(headersObj).forEach(([k, v]) => { resHeaders[k.toLowerCase()] = v; });
      }
    },
    write: (chunk) => { responseData += chunk; },
    end: (chunk) => {
      if (chunk) responseData += chunk;
    }
  };

  return {
    req,
    res,
    execute: () => {
      govApi.handleGovApiRequest(req, res, pathname, query);
      let parsed = null;
      try {
        parsed = JSON.parse(responseData);
      } catch (e) {
        parsed = responseData;
      }
      return { statusCode, headers: resHeaders, body: parsed };
    }
  };
}

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`  ✓ ${name}`);
    passed++;
  } catch (e) {
    console.error(`  ✗ ${name}`);
    console.error(`    ${e.message}`);
    failed++;
  }
}

console.log('\n--- Running AeroIndex Government Data API (v1) Test Suite ---');

// 1. Health endpoint (Public)
test('GET /api/v1/health returns 200 and standard envelope with HEALTHY status', () => {
  const { execute } = createMockReqRes({ pathname: '/api/v1/health' });
  const result = execute();
  assert.strictEqual(result.statusCode, 200);
  assert.strictEqual(result.body.success, true);
  assert.strictEqual(result.body.data.api_status, 'HEALTHY');
  assert.strictEqual(result.body.data.api_version, 'v1.0.0');
  assert.strictEqual(result.body.meta.data_status, 'SIMULATED_LIVE');
  assert.strictEqual(result.body.meta.methodology_version, 'JEVONS-2026.1');
  assert.strictEqual(result.body.error, null);
});

// 2. Metadata endpoint (Public)
test('GET /api/v1/metadata returns 200 and complete dataset catalogue', () => {
  const { execute } = createMockReqRes({ pathname: '/api/v1/metadata' });
  const result = execute();
  assert.strictEqual(result.statusCode, 200);
  assert.strictEqual(result.body.success, true);
  assert.ok(Array.isArray(result.body.data.datasets));
  assert.ok(result.body.data.datasets.length >= 8);
  assert.ok(result.body.data.supported_series.some(s => s.id === 'APIX-NAT-COMP'));
  assert.strictEqual(result.body.data.methodology_standards.elementary_aggregation.includes('Jevons'), true);
});

// 3. OpenAPI Spec (Public)
test('GET /api/v1/openapi.json returns valid OpenAPI 3.1.0 specification', () => {
  const { execute } = createMockReqRes({ pathname: '/api/v1/openapi.json' });
  const result = execute();
  assert.strictEqual(result.statusCode, 200);
  assert.strictEqual(result.body.openapi, '3.1.0');
  assert.ok(result.body.paths['/index/latest']);
  assert.ok(result.body.paths['/routes']);
  assert.ok(result.body.paths['/attribution/latest']);
});

// 4. Latest Index (Public)
test('GET /api/v1/index/latest returns 200 with index values, changes and lead curve', () => {
  const { execute } = createMockReqRes({ pathname: '/api/v1/index/latest' });
  const result = execute();
  assert.strictEqual(result.statusCode, 200);
  assert.strictEqual(result.body.success, true);
  assert.strictEqual(result.body.data.series_id, 'APIX-NAT-COMP');
  assert.strictEqual(result.body.data.index_value, 114.82);
  assert.strictEqual(result.body.data.change_bps, 145);
  assert.ok(result.body.data.lead_time_disaggregation.L01.premium_pct > 50);
});

// 5. Auth Protection on Institutional Endpoints (Failure without key)
test('GET /api/v1/index/history without key returns 401 UNAUTHORIZED', () => {
  const { execute } = createMockReqRes({ pathname: '/api/v1/index/history' });
  const result = execute();
  assert.strictEqual(result.statusCode, 401);
  assert.strictEqual(result.body.success, false);
  assert.strictEqual(result.body.error.code, 'UNAUTHORIZED');
  assert.strictEqual(result.body.meta.data_status, 'NO_DATA');
});

test('GET /api/v1/routes with invalid key returns 401 UNAUTHORIZED', () => {
  const { execute } = createMockReqRes({
    pathname: '/api/v1/routes',
    headers: { 'x-api-key': 'invalid_secret_key_12345' }
  });
  const result = execute();
  assert.strictEqual(result.statusCode, 401);
  assert.strictEqual(result.body.error.code, 'UNAUTHORIZED');
});

// 6. Institutional Key Success
test('GET /api/v1/index/history with valid evaluation key returns 200 paginated series', () => {
  const { execute } = createMockReqRes({
    pathname: '/api/v1/index/history',
    headers: { 'x-api-key': 'aero_eval_sandbox_key' },
    query: { limit: '10', page: '1' }
  });
  const result = execute();
  assert.strictEqual(result.statusCode, 200);
  assert.strictEqual(result.body.success, true);
  assert.strictEqual(result.body.data.points.length, 10);
  assert.strictEqual(result.body.meta.pagination.limit, 10);
  assert.strictEqual(result.body.meta.pagination.page, 1);
  assert.ok(result.headers['x-ratelimit-limit']);
});

test('GET /api/v1/routes with Bearer auth returns 200 and 20 basket routes', () => {
  const { execute } = createMockReqRes({
    pathname: '/api/v1/routes',
    headers: { 'authorization': 'Bearer aero_inst_rbi_research_2026' }
  });
  const result = execute();
  assert.strictEqual(result.statusCode, 200);
  assert.strictEqual(result.body.success, true);
  assert.strictEqual(result.body.data.routes.length, 20);
  const delBom = result.body.data.routes.find(r => r.route_id === 'DEL-BOM');
  assert.ok(delBom);
  assert.strictEqual(delBom.dgca_volume_weight, 0.125);
});

// 7. Route detail & Route not found
test('GET /api/v1/routes/DEL-BOM returns specific route intelligence and carriers', () => {
  const { execute } = createMockReqRes({
    pathname: '/api/v1/routes/DEL-BOM',
    headers: { 'x-api-key': 'aero_eval_sandbox_key' }
  });
  const result = execute();
  assert.strictEqual(result.statusCode, 200);
  assert.strictEqual(result.body.data.route_id, 'DEL-BOM');
  assert.ok(result.body.data.lead_time_buckets.L01);
  assert.ok(result.body.data.carriers.length >= 2);
});

test('GET /api/v1/routes/XYZ-ABC returns 404 ROUTE_NOT_FOUND', () => {
  const { execute } = createMockReqRes({
    pathname: '/api/v1/routes/XYZ-ABC',
    headers: { 'x-api-key': 'aero_eval_sandbox_key' }
  });
  const result = execute();
  assert.strictEqual(result.statusCode, 404);
  assert.strictEqual(result.body.error.code, 'ROUTE_NOT_FOUND');
});

// 8. Carriers Endpoint
test('GET /api/v1/carriers returns 5 domestic airlines with DGCA share distinction', () => {
  const { execute } = createMockReqRes({
    pathname: '/api/v1/carriers',
    headers: { 'x-api-key': 'aero_inst_nso_stat_2026' }
  });
  const result = execute();
  assert.strictEqual(result.statusCode, 200);
  assert.strictEqual(result.body.data.carriers.length, 5);
  const indigo = result.body.data.carriers.find(c => c.carrier_code === '6E');
  assert.strictEqual(indigo.dgca_published_market_share_pct, 61.2);
  assert.ok(result.body.data.concept_distinction.includes('DGCA market share'));
});

// 9. Attribution Decomposition & Mathematical Reconciliation
test('GET /api/v1/attribution/latest returns exact mathematical reconciliation (+145 bps)', () => {
  const { execute } = createMockReqRes({
    pathname: '/api/v1/attribution/latest',
    headers: { 'x-api-key': 'aero_eval_sandbox_key' }
  });
  const result = execute();
  assert.strictEqual(result.statusCode, 200);
  const recon = result.body.data.reconciliation;
  assert.strictEqual(recon.total_reconciled_bps, 145);
  assert.strictEqual(recon.reconciliation_status, 'EXACT_MATCH');
  assert.ok(result.body.data.epistemological_disclaimer.includes('does NOT imply legal or economic causation'));
});

// 10. National Coverage (NCO-2026.1)
test('GET /api/v1/coverage returns explicit denominators and 80% guard pass', () => {
  const { execute } = createMockReqRes({
    pathname: '/api/v1/coverage',
    headers: { 'x-api-key': 'aero_eval_sandbox_key' }
  });
  const result = execute();
  assert.strictEqual(result.statusCode, 200);
  assert.strictEqual(result.body.data.market_universe.total_scheduled_flight_instances, 12842);
  assert.strictEqual(result.body.data.coverage_metrics.schedule_discovery.denominator, 12842);
  assert.strictEqual(result.body.data.coverage_metrics.schedule_discovery.pct, 98.2);
  assert.strictEqual(result.body.data.basket_route_coverage.guard_status, 'PASSED');
});

// 11. Anomalies with Non-Causal Evidence
test('GET /api/v1/anomalies returns Modified Z-Score anomalies with non-causal evidence statement', () => {
  const { execute } = createMockReqRes({
    pathname: '/api/v1/anomalies',
    headers: { 'x-api-key': 'aero_eval_sandbox_key' }
  });
  const result = execute();
  assert.strictEqual(result.statusCode, 200);
  assert.ok(result.body.data.anomalies.length >= 1);
  const delBom = result.body.data.anomalies.find(a => a.route_id === 'DEL-BOM');
  assert.ok(delBom.statistical_parameters.calculated_modified_z >= 3.0);
  assert.ok(delBom.epistemological_statement.includes('does not establish'));
});

// 12. Provenance Certificate & Cryptographic Digest
test('GET /api/v1/provenance/APIX-2026-09-27 returns deterministic replay proof and SHA-256 hash', () => {
  const { execute } = createMockReqRes({
    pathname: '/api/v1/provenance/APIX-2026-09-27',
    headers: { 'x-api-key': 'aero_eval_sandbox_key' }
  });
  const result = execute();
  assert.strictEqual(result.statusCode, 200);
  assert.strictEqual(result.body.data.record_id, 'APIX-2026-09-27');
  assert.strictEqual(result.body.data.reproducibility.status, 'DETERMINISTIC_REPLAY_VERIFIED');
  assert.strictEqual(result.body.data.cryptographic_fingerprint.sha256_audit_hash.length, 64);
});

// 13. Rate Limiter Enforcement
test('Rate Limiter blocks excessive requests with 429 RATE_LIMIT_EXCEEDED', () => {
  // Exhaust sandbox key quota (limit 60) by testing with mock high count
  const testId = 'exhaust_test_ip';
  for (let i = 0; i < 60; i++) {
    govApi.applyRateLimit(testId, 60);
  }
  const overflow = govApi.applyRateLimit(testId, 60);
  assert.strictEqual(overflow.allowed, false);
  assert.strictEqual(overflow.remaining, 0);
});

// 14. API Key Lifecycle: List, Generate, Authenticate, Revoke
test('API Key Lifecycle: generates key, authenticates, lists, and revokes cleanly', () => {
  // 1. Generate key
  const genRes = createMockReqRes({
    pathname: '/api/v1/auth/keys/generate',
    query: { name: 'Audit Team Test Key', org: 'SIH 2026 Jury' }
  }).execute();
  assert.strictEqual(genRes.statusCode, 201);
  assert.ok(genRes.body.data.raw_key.startsWith('aero_inst_'));
  assert.ok(genRes.body.data.key_id);
  assert.ok(genRes.body.data.security_warning);

  const newKey = genRes.body.data.raw_key;
  const newKeyId = genRes.body.data.key_id;

  // 2. Use newly generated key to fetch protected endpoint
  const authRes = createMockReqRes({
    pathname: '/api/v1/index/history',
    headers: { 'x-api-key': newKey }
  }).execute();
  assert.strictEqual(authRes.statusCode, 200);

  // 3. List keys and confirm presence
  const listRes = createMockReqRes({ pathname: '/api/v1/auth/keys' }).execute();
  assert.strictEqual(listRes.statusCode, 200);
  const foundKey = listRes.body.data.keys.find(k => k.key_id === newKeyId);
  assert.ok(foundKey);
  assert.strictEqual(foundKey.status, 'ACTIVE');
  assert.ok(foundKey.last_used);

  // 4. Revoke key
  const revokeRes = createMockReqRes({
    pathname: '/api/v1/auth/keys/revoke',
    query: { key_id: newKeyId }
  }).execute();
  assert.strictEqual(revokeRes.statusCode, 200);
  assert.strictEqual(revokeRes.body.data.status, 'REVOKED');

  // 5. Verify revoked key is rejected
  const rejectedRes = createMockReqRes({
    pathname: '/api/v1/index/history',
    headers: { 'x-api-key': newKey }
  }).execute();
  assert.strictEqual(rejectedRes.statusCode, 401);
});

// 15. Reserve Bank of India (RBI) Key Verification
test('Reserve Bank of India (RBI) API Key authenticates and queries attribution with 300 RPM quota', () => {
  const { execute } = createMockReqRes({
    pathname: '/api/v1/attribution/latest',
    headers: { 'x-api-key': 'aero_inst_rbi_research_2026' }
  });
  const result = execute();
  assert.strictEqual(result.statusCode, 200);
  assert.strictEqual(result.body.success, true);
  assert.strictEqual(result.headers['x-ratelimit-limit'], 300);
  assert.strictEqual(result.body.data.reconciliation.reconciliation_status, 'EXACT_MATCH');
});

// 16. National Statistical Office (NSO) Key Verification
test('National Statistical Office (NSO) API Key authenticates and queries coverage with 300 RPM quota', () => {
  const { execute } = createMockReqRes({
    pathname: '/api/v1/coverage',
    headers: { 'x-api-key': 'aero_inst_nso_stat_2026' }
  });
  const result = execute();
  assert.strictEqual(result.statusCode, 200);
  assert.strictEqual(result.body.success, true);
  assert.strictEqual(result.headers['x-ratelimit-limit'], 300);
  assert.strictEqual(result.body.data.basket_route_coverage.guard_status, 'PASSED');
});

console.log(`\nResults: ${passed} passed, ${failed} failed.\n`);
if (failed > 0) process.exit(1);
