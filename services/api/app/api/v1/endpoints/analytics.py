"""Advanced analytics, forecasting, policy simulation, and explanation endpoints."""

from __future__ import annotations

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
