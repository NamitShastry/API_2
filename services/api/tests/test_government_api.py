"""Unit tests for the Government & Institutional Data API (v1).

Tests endpoints, data schemas, mathematical reconciliation, non-causal evidence claims,
and institutional key authentication.
"""

import unittest
from app.api.v1.endpoints.government import (
    build_envelope,
    get_attribution_latest,
    get_carrier_intelligence,
    get_health_data,
    get_historical_index,
    get_latest_index,
    get_metadata_catalogue,
    get_monitored_routes,
    get_national_coverage_data,
    get_provenance_data,
    verify_institutional_key,
)


class TestGovernmentApi(unittest.TestCase):
    def test_health_endpoint_data(self):
        """Verify health telemetry includes status, latency, and data freshness."""
        health = get_health_data()
        self.assertEqual(health["api_status"], "HEALTHY")
        self.assertEqual(health["api_version"], "v1.0.0")
        self.assertEqual(health["operating_mode"], "SIMULATED_LIVE")
        self.assertIn("latest_quote_ingested_at", health["data_lineage"])

    def test_metadata_catalogue_structure(self):
        """Verify metadata specifies methodology standards and units."""
        meta = get_metadata_catalogue()
        self.assertEqual(meta["api_version"], "v1.0.0")
        self.assertEqual(meta["base_period"], "2026-01-01 = 100.00")
        self.assertIn("Jevons", meta["methodology_standards"]["elementary_aggregation"])
        self.assertEqual(meta["methodology_standards"]["coverage_guard"], "Index calculation suspended if basket route coverage drops below 80%")

    def test_latest_index_structure(self):
        """Verify latest index provides index value, bps changes, and lead-time curve."""
        latest = get_latest_index()
        self.assertEqual(latest["series_id"], "APIX-NAT-COMP")
        self.assertEqual(latest["index_value"], 114.82)
        self.assertEqual(latest["change_bps"], 145)
        self.assertGreater(latest["lead_time_disaggregation"]["L01"]["premium_pct"], 50.0)
        self.assertEqual(latest["lead_time_disaggregation"]["L14"]["premium_pct"], 0.0)

    def test_historical_series_pagination(self):
        """Verify historical series returns paginated points with dates and coverage."""
        hist, pagination = get_historical_index(limit=15, page=1)
        self.assertEqual(len(hist["points"]), 15)
        self.assertEqual(pagination["page"], 1)
        self.assertEqual(pagination["limit"], 15)
        self.assertTrue(pagination["has_more"])

    def test_routes_basket(self):
        """Verify 20 official DGCA passenger volume-weighted basket routes."""
        routes = get_monitored_routes()
        self.assertEqual(len(routes), 20)
        
        # Check DEL-BOM exists and has 12.5% weight
        del_bom = next(r for r in routes if r["route_id"] == "DEL-BOM")
        self.assertEqual(del_bom["dgca_volume_weight"], 0.125)
        self.assertEqual(del_bom["corridor_classification"], "TOP_20_DGCA_BASKET")

    def test_carrier_intelligence_dgca_distinction(self):
        """Verify distinction between DGCA market share and AeroIndex basket weight."""
        carrier_data = get_carrier_intelligence()
        self.assertEqual(carrier_data["carriers_count"], 5)
        self.assertIn("DGCA market share", carrier_data["concept_distinction"])
        
        indigo = next(c for c in carrier_data["carriers"] if c["carrier_code"] == "6E")
        self.assertEqual(indigo["dgca_published_market_share_pct"], 61.2)
        self.assertEqual(indigo["aeroindex_basket_weight_pct"], 61.2)

    def test_attribution_mathematical_reconciliation(self):
        """Verify strict additive reconciliation: Previous + Drivers + Residual == Current."""
        attr = get_attribution_latest()
        recon = attr["reconciliation"]
        self.assertEqual(recon["total_reconciled_bps"], 145)
        self.assertEqual(recon["reconciliation_status"], "EXACT_MATCH")
        self.assertIn("does NOT imply legal or economic causation", attr["epistemological_disclaimer"])

    def test_national_coverage_denominators(self):
        """Verify explicit denominators in National Coverage & Observability Framework."""
        cov = get_national_coverage_data()
        self.assertEqual(cov["market_universe"]["total_scheduled_flight_instances"], 12842)
        self.assertEqual(cov["coverage_metrics"]["schedule_discovery"]["denominator"], 12842)
        self.assertEqual(cov["coverage_metrics"]["schedule_discovery"]["pct"], 98.2)
        self.assertEqual(cov["basket_route_coverage"]["guard_status"], "PASSED")

    def test_provenance_cryptographic_audit(self):
        """Verify SHA-256 fingerprint and deterministic replay proof."""
        prov = get_provenance_data("APIX-2026-09-27")
        self.assertEqual(prov["record_id"], "APIX-2026-09-27")
        self.assertEqual(len(prov["cryptographic_fingerprint"]["sha256_audit_hash"]), 64)
        self.assertEqual(prov["reproducibility"]["status"], "DETERMINISTIC_REPLAY_VERIFIED")

    def test_institutional_key_verification(self):
        """Verify institutional keys for RBI, NSO, and evaluation sandbox."""
        # Success cases
        valid_rbi, rbi_rec, err = verify_institutional_key("aero_inst_rbi_research_2026")
        self.assertTrue(valid_rbi)
        self.assertEqual(rbi_rec["tier"], "INSTITUTIONAL_CENTRAL_BANK")

        valid_sandbox, sand_rec, err = verify_institutional_key("Bearer aero_eval_sandbox_key")
        self.assertTrue(valid_sandbox)
        self.assertEqual(sand_rec["tier"], "SANDBOX_EVALUATION")

        # Failure cases
        invalid, _, err = verify_institutional_key("unauthorized_key_999")
        self.assertFalse(invalid)
        self.assertEqual(err, "INVALID_API_KEY")

        missing, _, err = verify_institutional_key(None)
        self.assertFalse(missing)
        self.assertEqual(err, "MISSING_API_KEY")

    def test_standard_response_envelope(self):
        """Verify standard envelope format with metadata and error structures."""
        env = build_envelope(
            success=True,
            data={"test": 123},
            data_status="SIMULATED_LIVE",
            methodology="JEVONS-2026.1",
        )
        self.assertTrue(env["success"])
        self.assertEqual(env["data"]["test"], 123)
        self.assertEqual(env["meta"]["api_version"], "v1.0.0")
        self.assertEqual(env["meta"]["data_status"], "SIMULATED_LIVE")
        self.assertIsNone(env["error"])


if __name__ == "__main__":
    unittest.main()
