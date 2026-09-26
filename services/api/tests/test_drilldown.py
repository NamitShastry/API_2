"""Unit and integration tests for DEL Network, 11-Level Drill-Down, and Enforcement Requirements."""

import unittest
from app.analytics.drilldown import RouteIntelligenceWorkspace, DEL_DOMESTIC_DESTINATIONS
from app.analytics.advanced import AdvancedAnalyticsEngine


class TestDrilldownAndEnforcement(unittest.TestCase):
    def test_del_network_master_registry(self):
        """Verify the master registry contains all 42 domestic destinations with correct statuses."""
        self.assertEqual(len(DEL_DOMESTIC_DESTINATIONS), 42)
        
        overview = RouteIntelligenceWorkspace.get_del_network_overview()
        metrics = overview["network_metrics"]
        
        self.assertEqual(metrics["total_domestic_destinations"], 42)
        self.assertEqual(metrics["covered_destinations"], 24)
        self.assertEqual(metrics["partial_destinations"], 8)
        self.assertEqual(metrics["unavailable_destinations"], 10)
        self.assertEqual(metrics["full_coverage_pct"], 57.1)
        self.assertEqual(metrics["total_monitored_pct"], 76.2)
        
        # Verify honest provenance disclaimer
        self.assertIn("INDEX BASKET", overview["provenance"]["disclaimer"])
        self.assertIn("LIVE DEL NETWORK", overview["provenance"]["disclaimer"])

    def test_11_level_hierarchical_drilldown(self):
        """Verify end-to-end drill-down chain down to quote observations and R01-R12 rules."""
        drilldown = RouteIntelligenceWorkspace.get_hierarchical_drilldown(
            destination_iata="BOM",
            target_airline="6E",
            target_flight="6E-204",
            target_bucket="L07",
        )
        
        # Level 1 & 2: India & DEL Context
        self.assertIn("national_composite_index", drilldown["india_context"])
        
        # Level 3: Route Context
        self.assertEqual(drilldown["route_context"]["route_id"], "DEL-BOM")
        self.assertEqual(drilldown["route_context"]["city"], "Mumbai")
        
        # Level 4: Airlines
        self.assertGreater(len(drilldown["airlines"]), 0)
        
        # Level 5: Flights
        self.assertGreater(len(drilldown["flights"]), 0)
        
        # Level 6: Fare Families
        families = [f["family_code"] for f in drilldown["fare_families"]]
        self.assertIn("SAVER", families)
        self.assertIn("FLEXI", families)
        self.assertIn("CORPORATE", families)
        
        # Level 7: Lead Buckets
        self.assertEqual(len(drilldown["lead_buckets"]), 7)
        
        # Level 8: Quote Observation
        quote = drilldown["quote_observation"]
        self.assertIn("quote_hash", quote)
        self.assertIn("data_state", quote)
        
        # Level 9: Cleaning Decisions (R01-R12)
        decisions = drilldown["cleaning_decisions"]
        self.assertEqual(len(decisions), 12)
        rule_codes = [d["rule_code"] for d in decisions]
        for i in range(1, 13):
            expected_prefix = f"R{i:02d}_"
            self.assertTrue(any(rc.startswith(expected_prefix) for rc in rule_codes), f"Missing rule {expected_prefix}")

        # Level 10: Index Contribution
        self.assertIn("contribution_to_national_index_bps", drilldown["index_contribution"])
        
        # Level 11: Provenance & Signature
        self.assertIn("signature_sha256", drilldown["provenance"])
        self.assertEqual(len(drilldown["provenance"]["signature_sha256"]), 64)

    def test_forecast_honesty_gate_rejection(self):
        """Verify the honesty gate strictly blocks forecast when historical points < 14."""
        # 10 days of data (insufficient)
        hist_10 = [100.0 + i * 0.1 for i in range(10)]
        res = AdvancedAnalyticsEngine.evaluate_forecast_honesty(
            current_index=101.0,
            historical_points=hist_10,
            horizon_days=14,
        )
        self.assertFalse(res.honesty_gate_passed)
        self.assertEqual(res.status, "UNAVAILABLE_DATA_GATE")
        self.assertIn("Honesty Gate Active", res.rejection_reason)
        self.assertEqual(len(res.projections), 0)

    def test_forecast_honesty_gate_acceptance(self):
        """Verify the honesty gate allows projection when historical points >= 14."""
        hist_20 = [100.0 + i * 0.1 for i in range(20)]
        res = AdvancedAnalyticsEngine.evaluate_forecast_honesty(
            current_index=102.0,
            historical_points=hist_20,
            horizon_days=14,
        )
        self.assertTrue(res.honesty_gate_passed)
        self.assertEqual(res.status, "AVAILABLE")
        self.assertIsNone(res.rejection_reason)
        self.assertEqual(len(res.projections), 14)
        for p in res.projections:
            self.assertLess(p["lower_ci_95"], p["predicted_index"])
            self.assertGreater(p["upper_ci_95"], p["predicted_index"])

    def test_reproducible_anomalies_and_non_causal_statement(self):
        """Verify modified Z-score anomaly detection and strict non-causal evidence language."""
        # Big price surge: observed 7200 vs baseline 4800, MAD 400
        anomalies = AdvancedAnalyticsEngine.get_reproducible_anomalies(
            route_id="DEL-BOM",
            current_median_fare=7200.0,
            historical_baseline_median=4800.0,
            historical_mad=400.0,
        )
        self.assertEqual(len(anomalies), 1)
        anom = anomalies[0]
        self.assertGreaterEqual(anom["anomaly_score"], 3.0)
        self.assertEqual(anom["classification"], "PRICE_SURGE")
        
        # Enforce non-causal wording: "observed alongside", not "caused"
        evidence = anom["evidence_statement"]
        self.assertIn("observed alongside", evidence)
        self.assertIn("coincident event", evidence)
        self.assertIn("causal inference not asserted", evidence)
        
        # Verify supporting observations
        self.assertGreaterEqual(len(anom["supporting_observations"]), 1)


if __name__ == "__main__":
    unittest.main()
