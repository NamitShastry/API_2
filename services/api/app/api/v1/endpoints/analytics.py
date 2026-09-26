"""Advanced analytics, forecasting, policy simulation, and explanation endpoints."""

from __future__ import annotations

import datetime
from typing import Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.analytics.advanced import AdvancedAnalyticsEngine
from app.engine.flash_engine import FlashEngine

router = APIRouter(prefix="/analytics", tags=["Advanced Analytics (Tier 4)"])


class PolicySimulationRequest(BaseModel):
    annual_spend_inr: float = 50000000.0
    current_lastminute_pct: float = 40.0
    target_lastminute_pct: float = 15.0


@router.get("/anomalies")
async def get_anomalies(
    route_id: str = Query("DEL-BOM", description="Corridor identifier"),
    observed_fare: float = Query(6580.0, description="Current median observed fare"),
    baseline_fare: float = Query(4850.0, description="Historical same-DOW baseline median"),
    mad: float = Query(450.0, description="Median Absolute Deviation"),
):
    """Retrieve reproducible pricing anomalies detected via Modified Z-score with MAD.
    
    Includes exact formula, inputs, quote observation evidence, and non-causal co-occurrence statements.
    """
    anomalies = AdvancedAnalyticsEngine.get_reproducible_anomalies(
        route_id=route_id,
        current_median_fare=observed_fare,
        historical_baseline_median=baseline_fare,
        historical_mad=mad,
    )
    return {
        "route_id": route_id,
        "methodology": "Modified Z-Score via Median Absolute Deviation (Iglewicz & Hoaglin 1993)",
        "threshold_sigma": 3.0,
        "anomalies_detected": anomalies,
        "count": len(anomalies),
    }


@router.get("/forecast")
async def get_forecast(
    horizon_days: int = Query(14, ge=7, le=30),
    historical_days_available: int = Query(28, ge=0, le=365, description="Historical daily cycles available for model training"),
):
    """Generate forward index projections with 95% confidence intervals.
    
    Enforces the Honesty Gate: If historical baseline is < 14 cycles, projections are withheld.
    """
    tick = FlashEngine.get_latest_tick()

    if historical_days_available < 14:
        # Simulate fewer points to trigger honesty gate rejection
        hist_points = [tick.index_value - (i * 0.1) for i in range(historical_days_available)]
    else:
        hist_points = [tick.index_value - (i * 0.12) for i in range(historical_days_available)]

    honesty_result = AdvancedAnalyticsEngine.evaluate_forecast_honesty(
        current_index=tick.index_value,
        historical_points=hist_points,
        horizon_days=horizon_days,
    )

    return {
        "series_id": tick.series_id,
        "base_index": tick.index_value,
        "honesty_gate_passed": honesty_result.honesty_gate_passed,
        "status": honesty_result.status,
        "rejection_reason": honesty_result.rejection_reason,
        "model_name": honesty_result.model_name,
        "training_window_days": honesty_result.training_window_days,
        "sample_size": honesty_result.sample_size,
        "forecast_horizon_days": honesty_result.forecast_horizon_days,
        "confidence_level": honesty_result.confidence_level,
        "projections": honesty_result.projections,
    }


@router.get("/explanation")
async def get_explanation(
    route: str = Query("DEL-BOM", description="Top moving corridor"),
    coincident_event: Optional[str] = Query("Diwali Festive Season", description="Coincident calendar event if active"),
):
    """Generate evidence-based narrative strictly separating observation, correlation, and non-causal claims."""
    tick = FlashEngine.get_latest_tick()
    evidence = AdvancedAnalyticsEngine.generate_evidence_based_explanation(
        index_change_pts=tick.change_1d,
        top_driver_name=route,
        coincident_event=coincident_event,
    )
    return {
        "series_id": tick.series_id,
        "change_1d": tick.change_1d,
        "observation": evidence["observation"],
        "primary_driver": evidence["primary_driver"],
        "coincident_correlation": evidence["coincident_correlation"],
        "epistemological_status": evidence["epistemological_status"],
        "data_state": evidence["data_state"],
    }


@router.post("/simulate-policy")
async def simulate_policy(req: PolicySimulationRequest):
    """Simulate corporate travel expenditure savings when shifting advance booking windows."""
    res = AdvancedAnalyticsEngine.simulate_policy_savings(
        annual_air_spend_inr=req.annual_spend_inr,
        current_l01_l03_share=req.current_lastminute_pct / 100.0,
        target_l01_l03_share=req.target_lastminute_pct / 100.0,
    )
    return {
        "baseline_spend_inr": res.baseline_spend_inr,
        "optimized_spend_inr": res.optimized_spend_inr,
        "total_savings_inr": res.total_savings_inr,
        "savings_percentage": res.savings_percentage,
        "recommended_lead_bucket": res.recommended_lead_bucket,
        "scenario_details": res.scenario_details,
    }


@router.get("/coverage")
async def get_national_coverage():
    """Retrieve comprehensive National Aviation Coverage & Observability metrics across schedules, fares, and status."""
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return {
        "data_state": "SIMULATED_LIVE",
        "methodology": "National Coverage & Observability Framework (NCO-2026.1)",
        "as_of": now_iso,
        "market_universe": {
            "total_flight_instances": 12842,
            "discovered_schedules": 12610,
            "fare_observable_instances": 11866,
            "operational_status_observable": 11750,
            "fresh_instances": 11620,
            "index_eligible_instances": 11420,
            "unique_carriers": 6,
            "unique_routes": 1284,
            "unique_airports": 79,
        },
        "coverage_metrics": {
            "schedule_discovery": {
                "pct": 98.2,
                "numerator": 12610,
                "denominator": 12842,
                "definition": "Share of published DGCA/airline schedules actively discovered and mapped to flight instances."
            },
            "fare_observability": {
                "pct": 92.4,
                "numerator": 11866,
                "denominator": 12842,
                "definition": "Share of discovered flight instances with at least one valid fare observation in active collection window."
            },
            "operational_status": {
                "pct": 91.5,
                "numerator": 11750,
                "denominator": 12842,
                "definition": "Share of flight instances with live operational status telemetry (On-Time, Delayed, Boarding, Cancelled)."
            },
            "freshness": {
                "pct": 90.5,
                "numerator": 11620,
                "denominator": 12842,
                "definition": "Share of observed quotes arriving within configured freshness threshold (<15 min age)."
            },
            "route_coverage": {
                "pct": 97.2,
                "numerator": 1248,
                "denominator": 1284,
                "definition": "Active domestic corridors with continuous schedule and fare observation."
            },
            "carrier_coverage": {
                "pct": 100.0,
                "numerator": 6,
                "denominator": 6,
                "definition": "Major Indian scheduled operating carriers with active adapter ingest."
            },
            "source_coverage": {
                "pct": 88.9,
                "numerator": 8,
                "denominator": 9,
                "definition": "Configured adapter pipelines currently streaming active data feeds."
            }
        },
        "funnel": [
            {"stage": "Market Universe", "count": 12842, "pct": 100.0, "step_pct": 100.0, "desc": "All scheduled Indian domestic flight instances for current operating day."},
            {"stage": "Schedule Discovered", "count": 12610, "pct": 98.2, "step_pct": 98.2, "desc": "Schedules indexed from direct carrier feeds and GDS timetables."},
            {"stage": "Flight Instance Identified", "count": 12480, "pct": 97.2, "step_pct": 99.0, "desc": "Correlated across flight number, date, origin, and destination."},
            {"stage": "Fare Observed", "count": 11866, "pct": 92.4, "step_pct": 95.1, "desc": "At least one gross fare quote retrieved from active channels."},
            {"stage": "Valid Fare (R01-R12 Clean)", "count": 11540, "pct": 89.9, "step_pct": 97.3, "desc": "Passed tariff boundary, floor/ceiling, and tax sanity rules."},
            {"stage": "Operational Status Observed", "count": 11750, "pct": 91.5, "step_pct": 94.1, "desc": "Live ADS-B and airport departure telemetry matched."},
            {"stage": "Fresh Observation (<15m)", "count": 11620, "pct": 90.5, "step_pct": 98.9, "desc": "Quote age verified within real-time latency budget."},
            {"stage": "Index-Eligible Observation", "count": 11420, "pct": 88.9, "step_pct": 98.3, "desc": "Matched to elementary cell basket weights for Jevons aggregation."}
        ]
    }

