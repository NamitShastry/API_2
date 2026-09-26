"""
Part IV: Analytical Intelligence & Attribution Engine (Pages 15 - 20)
"""

import pymupdf as fitz
from .theme import (
    PAGE_WIDTH, PAGE_HEIGHT, MARGIN_LEFT, MARGIN_RIGHT, CONTENT_WIDTH,
    MARGIN_TOP, MARGIN_BOTTOM, C_DARK_BG, C_DARK_CARD, C_DARK_BORDER,
    C_BG_PAGE, C_BG_CARD, C_BG_CARD_ALT, C_BORDER_CARD, C_BORDER_LINE,
    C_TEXT_MAIN, C_TEXT_MUTED, C_TEXT_LIGHT, C_BLUE, C_BLUE_LIGHT, C_CYAN,
    C_CYAN_LIGHT, C_EMERALD, C_EMERALD_LIGHT, C_AMBER, C_AMBER_LIGHT, C_ROSE,
    C_ROSE_LIGHT, C_PURPLE, C_PURPLE_LIGHT, C_SLATE_DARK,
    ASSET_MAP_TRANSPARENT,
    init_page, draw_header, draw_footer, draw_badge, draw_card, draw_kpi,
    draw_table, draw_formula_box, draw_bullet_list, draw_pipeline_step
)

def render_page_15(doc):
    """PAGE 15 -- FLASH VS OFFICIAL INDEX"""
    page = init_page(doc)
    top_y = draw_header(
        page, 
        part_title="PART IV -- ANALYTICAL INTELLIGENCE",
        page_title="Dual-State Publication: FLASH vs. OFFICIAL Index",
        page_subtitle="Latency profiles, revision mechanics, audit settlement, and publication lifecycle",
        status="IMPLEMENTED IN API CONTRACTS", status_type="implemented"
    )

    # Narrative Introduction
    page.insert_textbox(fitz.Rect(MARGIN_LEFT, top_y, MARGIN_RIGHT, top_y + 35),
        "AeroIndex operates an institutional dual-state publication architecture. Financial risk analysts and algorithmic traders require real-time signal velocity, whereas corporate travel managers, government regulators, and macroeconomists require finalized, immutable, audited settlement benchmarks.",
        fontsize=7.8, fontname="helv", color=C_TEXT_MAIN
    )

    # Dual Column Comparison: FLASH vs OFFICIAL
    comp_y = top_y + 40
    cw = (CONTENT_WIDTH - 12) / 2
    ch = 195

    # Left: FLASH Index
    draw_card(page, MARGIN_LEFT, comp_y, cw, ch, bg=C_AMBER_LIGHT, border=C_AMBER, left_accent=C_AMBER)
    page.insert_text((MARGIN_LEFT + 12, comp_y + 14), "1. THE FLASH INDEX (REAL-TIME STREAM)", fontname="hebo", fontsize=8.0, color=C_AMBER)
    draw_badge(page, MARGIN_LEFT + cw - 75, comp_y + 5, 68, 12, "REAL-TIME", "flash")

    flash_attrs = [
        ("Target Latency", "< 150 milliseconds via Redis Pub/Sub"),
        ("Update Trigger", "Continuous event-driven per quote ingestion"),
        ("Imputation Model", "Zero imputation; uses live available quotes"),
        ("Revision Policy", "Open to continuous intra-day adjustments"),
        ("Coverage Threshold", "Corridor indexed if >= 65% quotes fresh"),
        ("Use Case", "Algorithmic monitoring, anomaly triggers, live alerts"),
        ("Persistence State", "Volatile cache in Redis with 72h snapshot roll")
    ]
    fay = comp_y + 26
    for label, val in flash_attrs:
        page.insert_text((MARGIN_LEFT + 12, fay + 8), label, fontname="hebo", fontsize=6.8, color=C_TEXT_MAIN)
        page.insert_text((MARGIN_LEFT + 12, fay + 17), val, fontname="menlo", fontsize=6.2, color=C_TEXT_MUTED)
        fay += 23

    # Right: OFFICIAL Index
    draw_card(page, MARGIN_LEFT + cw + 12, comp_y, cw, ch, bg=C_BLUE_LIGHT, border=C_BLUE, left_accent=C_BLUE)
    page.insert_text((MARGIN_LEFT + cw + 22, comp_y + 14), "2. THE OFFICIAL INDEX (DAILY SETTLEMENT)", fontname="hebo", fontsize=8.0, color=C_BLUE)
    draw_badge(page, MARGIN_RIGHT - 75, comp_y + 5, 68, 12, "SETTLED", "official")

    off_attrs = [
        ("Release Schedule", "Daily at 23:59:59 IST (EOD Settlement)"),
        ("Verification Gate", "Full R01-R12 audit and cross-channel reconciliation"),
        ("Imputation Model", "Synthetic carryover for missing flight instances"),
        ("Revision Policy", "Immutable once published (v1.0 sealed)"),
        ("Coverage Threshold", "Strict 80% coverage guard enforced"),
        ("Use Case", "Corporate contracts, hedging benchmarks, inflation metrics"),
        ("Persistence State", "PostgreSQL TimescaleDB permanent hypertable")
    ]
    oay = comp_y + 26
    for label, val in off_attrs:
        page.insert_text((MARGIN_LEFT + cw + 22, oay + 8), label, fontname="hebo", fontsize=6.8, color=C_TEXT_MAIN)
        page.insert_text((MARGIN_LEFT + cw + 22, oay + 17), val, fontname="menlo", fontsize=6.2, color=C_TEXT_MUTED)
        oay += 23

    # Lifecycle Progression Flow (Middle)
    flow_y = comp_y + ch + 12
    draw_card(page, MARGIN_LEFT, flow_y, CONTENT_WIDTH, 115, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=C_PURPLE)
    page.insert_text((MARGIN_LEFT + 12, flow_y + 14), "INTRA-DAY PUBLICATION & CONVERGENCE LIFECYCLE", fontname="hebo", fontsize=8.0, color=C_PURPLE)

    stages = [
        ("06:00 IST: Morning Flash", "Early morning departures update index; initial morning spike captured."),
        ("12:00 IST: Midday Flash", "High corporate booking density; corridor weights dynamically balanced."),
        ("18:00 IST: Evening Flash", "Peak evening business departures; load factors reach terminal daily values."),
        ("23:59 IST: Official Seal", "Batch audit re-runs R01-R12, verifies SHA-256 hashes, seals official value.")
    ]
    sw = (CONTENT_WIDTH - 24 - 18) / 4
    for idx, (s_title, s_desc) in enumerate(stages):
        sx = MARGIN_LEFT + 12 + idx * (sw + 6)
        s_rect = fitz.Rect(sx, flow_y + 24, sx + sw, flow_y + 105)
        page.draw_rect(s_rect, color=C_BORDER_CARD, fill=C_BG_PAGE, width=0.5)
        page.insert_text((sx + 6, flow_y + 38), s_title, fontname="hebo", fontsize=6.2, color=C_PURPLE)
        page.insert_textbox(fitz.Rect(sx + 6, flow_y + 44, sx + sw - 6, flow_y + 100), s_desc, fontsize=5.8, fontname="helv", color=C_TEXT_MUTED)

    # Revision Drift Tolerance Policy (Bottom Table)
    bot_y = flow_y + 125
    headers = ["Corridor Tier", "Max Expected Flash Drift", "Settlement Window", "Audit Trigger Bound", "Historical Variance"]
    cols = [100, 110, 95, 110, 100]
    rows = [
        ["Metro Trunk (DEL-BOM)", "+/- 0.45 index pts", "23:59 IST", "|Drift| > 1.20 pts", "Low (+/- 0.28 pts)"],
        ["Metro Secondary (BLR-DEL)", "+/- 0.65 index pts", "23:59 IST", "|Drift| > 1.50 pts", "Moderate (+/- 0.42 pts)"],
        ["Tier-1 Non-Metro (PNQ-DEL)", "+/- 1.10 index pts", "23:59 IST", "|Drift| > 2.20 pts", "Moderate (+/- 0.85 pts)"],
        ["Regional (DED-DEL)", "+/- 2.40 index pts", "23:59 IST", "|Drift| > 4.50 pts", "High (+/- 1.80 pts)"]
    ]
    draw_table(page, MARGIN_LEFT, bot_y, CONTENT_WIDTH, headers, rows, cols, row_height=18, font_size=6.8)

    draw_footer(page, 15)

def render_page_16(doc):
    """PAGE 16 -- WHAT MOVED TODAY'S INDEX"""
    page = init_page(doc)
    top_y = draw_header(
        page, 
        part_title="PART IV -- ANALYTICAL INTELLIGENCE",
        page_title="What Moved Today's Index: Attribution Hierarchy",
        page_subtitle="Decomposing national index movements into multi-level mathematical contributions",
        status="IMPLEMENTED IN WHAT_MOVED ENGINE", status_type="implemented"
    )

    # Narrative & Non-Causal Manifesto
    page.insert_textbox(fitz.Rect(MARGIN_LEFT, top_y, MARGIN_RIGHT, top_y + 35),
        "When the AeroIndex changes by +145 basis points (+1.45%), market participants demand to know the exact source of movement. AeroIndex implements a hierarchical attribution engine that decomposes movements across Corridors, Carriers, Lead Times, and Fare Components.",
        fontsize=7.8, fontname="helv", color=C_TEXT_MAIN
    )

    # The Non-Causal Cardinal Rule (Warning Box)
    warn_rect = fitz.Rect(MARGIN_LEFT, top_y + 40, MARGIN_RIGHT, top_y + 96)
    page.draw_rect(warn_rect, color=C_ROSE, fill=C_ROSE_LIGHT, width=0.8)
    page.insert_text((MARGIN_LEFT + 12, top_y + 53), "THE CARDINAL PRINCIPLE: MATHEMATICAL CONTRIBUTION != CAUSATION", fontname="hebo", fontsize=7.8, color=C_ROSE)
    page.insert_textbox(fitz.Rect(MARGIN_LEFT + 12, top_y + 57, MARGIN_RIGHT - 12, top_y + 92),
        "A statement that 'DEL-BOM contributed +42 basis points to today's index move' is a rigorous mathematical identity. It states that the weighted price change in that corridor accounts for 42 bps of the total net move. It does NOT assert why prices rose (e.g. weather delays, festival demand, fuel spikes). AeroIndex never fabricates narrative market stories without verifiable news feeds.",
        fontsize=6.2, fontname="helv", color=C_TEXT_MAIN
    )

    # Hierarchical Decomposition Tree (Visual Flow)
    tree_y = top_y + 104
    draw_card(page, MARGIN_LEFT, tree_y, CONTENT_WIDTH, 172, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=C_BLUE)
    page.insert_text((MARGIN_LEFT + 12, tree_y + 14), "HIERARCHICAL ATTRIBUTION DRILLDOWN TREE", fontname="hebo", fontsize=8.0, color=C_BLUE)

    levels = [
        ("Level 1: National Index", "Net Daily Change: +145 bps (+1.45 index pts)", C_TEXT_MAIN),
        ("Level 2: Corridor Contribution", "DEL-BOM (+42 bps), BLR-DEL (+28 bps), BOM-BLR (+22 bps), Others (+53 bps)", C_BLUE),
        ("Level 3: Carrier Contribution", "IndiGo 6E (+78 bps), Air India AI (+42 bps), Akasa QP (+18 bps), SpiceJet SG (+7 bps)", C_CYAN),
        ("Level 4: Lead-Time Bucket", "L01 Same-Day (+65 bps), L03 (+38 bps), L07 (+24 bps), L14-L60 (+18 bps)", C_PURPLE),
        ("Level 5: Component Breakdown", "Base Fare (+110 bps), ATF Surcharge (+22 bps), Taxes (+13 bps)", C_EMERALD)
    ]
    
    ly = tree_y + 26
    for idx, (lvl_title, lvl_desc, lvl_col) in enumerate(levels):
        page.draw_rect(fitz.Rect(MARGIN_LEFT + 12 + idx * 8, ly, MARGIN_RIGHT - 12, ly + 25), color=C_BORDER_CARD, fill=C_BG_PAGE, width=0.5)
        page.insert_text((MARGIN_LEFT + 20 + idx * 8, ly + 11), lvl_title, fontname="hebo", fontsize=7.0, color=lvl_col)
        page.insert_text((MARGIN_LEFT + 20 + idx * 8, ly + 20), lvl_desc, fontname="menlo", fontsize=6.2, color=C_TEXT_MUTED)
        ly += 28

    # Basis Point Contribution Table
    tbl_y = tree_y + 180
    headers = ["Dimension", "Entity Name", "Weight (W_k)", "Observed Move", "BPS Contribution", "Share of Total Move"]
    cols = [85, 110, 75, 80, 85, 80]
    rows = [
        ["Corridor", "DEL -> BOM (Delhi-Mumbai)", "14.2%", "+2.95 index pts", "+41.89 bps", "28.9% of move"],
        ["Corridor", "BLR -> DEL (Bengaluru-Delhi)", "8.9%", "+3.15 index pts", "+28.04 bps", "19.3% of move"],
        ["Corridor", "BOM -> BLR (Mumbai-Bengaluru)", "9.8%", "+2.24 index pts", "+21.95 bps", "15.1% of move"],
        ["Carrier", "6E (IndiGo Network)", "62.4%", "+1.25 index pts", "+78.00 bps", "53.8% of move"],
        ["Carrier", "AI (Air India Network)", "24.5%", "+1.71 index pts", "+41.90 bps", "28.9% of move"],
        ["Lead Time", "L01 (0-1 Day Walkup)", "8.0%", "+8.12 index pts", "+64.96 bps", "44.8% of move"],
        ["Composite", "Total Reconciled National Index", "100.0%", "+1.45 index pts", "+145.00 bps", "100.0% RECONCILED"]
    ]
    draw_table(page, MARGIN_LEFT, tbl_y, CONTENT_WIDTH, headers, rows, cols, row_height=18, font_size=6.4)

    draw_footer(page, 16)

def render_page_17(doc):
    """PAGE 17 -- ATTRIBUTION MATHEMATICS"""
    page = init_page(doc)
    top_y = draw_header(
        page, 
        part_title="PART IV -- ANALYTICAL INTELLIGENCE",
        page_title="Attribution Mathematics & Reconciled Identities",
        page_subtitle="Exact basis-point decomposition formulas, unrounded precision, and residual reconciliation",
        status="IMPLEMENTED IN ADVANCED ENGINE", status_type="implemented"
    )

    # Narrative
    page.insert_textbox(fitz.Rect(MARGIN_LEFT, top_y, MARGIN_RIGHT, top_y + 35),
        "Attribution in AeroIndex is not a heuristic estimation. It is an exact additive accounting identity. The sum of basis point contributions from every sub-corridor plus mathematical rounding residuals must identically equal the total net index movement.",
        fontsize=7.8, fontname="helv", color=C_TEXT_MAIN
    )

    # Formula Box
    form_y = top_y + 40
    vars_desc = [
        ("Delta I_{total}", "Total national index movement in points: I(t) - I(t-1)"),
        ("BPS_{total}", "Total movement expressed in basis points: Delta I_{total} * 100"),
        ("W_k", "Fixed DGCA weight for sub-component k (e.g. corridor or carrier)"),
        ("Delta I_k", "Movement of sub-component index k: I_k(t) - I_k(t-1)"),
        ("C_k", "Contribution of component k: W_k * Delta I_k * 100 (in basis points)"),
        ("E_{residual}", "Floating-point precision rounding residual (strictly bounded |E| < 0.01 bps)")
    ]
    draw_formula_box(
        page, MARGIN_LEFT, form_y, CONTENT_WIDTH, 120,
        title="Additive Basis Point Attribution & Reconciliation Equations",
        formula="BPS_{total} = SUM_{k in K} C_k + E_{residual}\nC_k = W_k * [ I_k(t) - I_k(t-1) ] * 100",
        variable_lines=vars_desc
    )

    # Fully Worked Illustrative Attribution Reconciliation
    work_y = form_y + 128
    draw_card(page, MARGIN_LEFT, work_y, CONTENT_WIDTH, 185, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=C_PURPLE)
    page.insert_text((MARGIN_LEFT + 12, work_y + 14), "WORKED RECONCILIATION PROOF: +145 BASIS POINTS (+1.45 PTS)", fontname="hebo", fontsize=8.0, color=C_PURPLE)
    draw_badge(page, MARGIN_RIGHT - 110, work_y + 5, 98, 12, "ILLUSTRATIVE EXAMPLE", "simulated")

    # Step by step mathematical audit
    audit_txt = (
        "Baseline Index (t-1): 100.9400000000        Current Index (t): 102.3900000000\n"
        "Net Movement: Delta I = +1.4500000000 pts   --> Target BPS = +145.00000000 bps\n\n"
        "Sub-Component Calculations (Unrounded Float):\n"
        "  1. Corridor DEL-BOM:  Weight = 0.14200000 * Delta = +2.95000000 * 100 = +41.89000000 bps\n"
        "  2. Corridor BLR-DEL:  Weight = 0.08900000 * Delta = +3.15056180 * 100 = +28.04000000 bps\n"
        "  3. Corridor BOM-BLR:  Weight = 0.09800000 * Delta = +2.23979592 * 100 = +21.95000000 bps\n"
        "  4. Corridor CCU-DEL:  Weight = 0.06500000 * Delta = +1.84615385 * 100 = +12.00000000 bps\n"
        "  5. Corridor HYD-DEL:  Weight = 0.05400000 * Delta = +1.98148148 * 100 = +10.70000000 bps\n"
        "  6. Other 37 Corridors:Weight = 0.55200000 * Delta = +0.55108696 * 100 = +30.42000000 bps\n\n"
        "Reconciliation Sum:\n"
        "  Sum(C_k) = 41.89 + 28.04 + 21.95 + 12.00 + 10.70 + 30.42 = +145.00000000 bps\n"
        "  Residual E = Target BPS - Sum(C_k) = +145.00000000 - 145.00000000 = 0.00000000 bps\n"
        "  Status: 100.000% EXACT RECONCILIATION PASSED"
    )
    page.insert_textbox(fitz.Rect(MARGIN_LEFT + 12, work_y + 24, MARGIN_RIGHT - 12, work_y + 178),
        audit_txt, fontsize=6.5, fontname="menlo", color=C_TEXT_MAIN
    )

    # Precision & Rounding Governance (Bottom)
    bot_y = work_y + 192
    draw_card(page, MARGIN_LEFT, bot_y, CONTENT_WIDTH, 52, bg=C_BG_CARD_ALT, border=C_BORDER_CARD)
    page.insert_text((MARGIN_LEFT + 12, bot_y + 14), "FLOATING-POINT INTEGRITY & ROUNDING GOVERNANCE:", fontname="hebo", fontsize=7.2, color=C_TEXT_MAIN)
    page.insert_textbox(fitz.Rect(MARGIN_LEFT + 12, bot_y + 18, MARGIN_RIGHT - 12, bot_y + 48),
        "* All calculations are executed in IEEE 754 64-bit float precision or Python Decimal(28).\n"
        "* Downstream UI representations are formatted to 2 decimal places (+145.00 bps), but the database stores 8 decimal places to eliminate cumulative rounding drift during multi-month time series compounding.",
        fontsize=6.5, fontname="helv", color=C_TEXT_MUTED
    )

    draw_footer(page, 17)

def render_page_18(doc):
    """PAGE 18 -- ROUTE & NETWORK INTELLIGENCE"""
    page = init_page(doc)
    top_y = draw_header(
        page, 
        part_title="PART IV -- ANALYTICAL INTELLIGENCE",
        page_title="Route & Network Intelligence",
        page_subtitle="42 monitored corridors, directional flow asymmetry, hub concentration, and corridor pricing volatility",
        status="IMPLEMENTED IN DRILLDOWN ENGINE", status_type="implemented"
    )

    # Top Narrative
    page.insert_textbox(fitz.Rect(MARGIN_LEFT, top_y, MARGIN_RIGHT, top_y + 35),
        "The Indian domestic civil aviation network is heavily concentrated around six major metropolitan hubs. AeroIndex models 42 distinct origin-destination corridors. Crucially, the platform isolates Route Intelligence (micro price behavior of a city pair) from Index Attribution (macro weighted impact on the national benchmark).",
        fontsize=7.8, fontname="helv", color=C_TEXT_MAIN
    )

    # Network Geography & Hub Matrix (Map + Hub Tiers)
    net_y = top_y + 40
    draw_card(page, MARGIN_LEFT, net_y, CONTENT_WIDTH, 230, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=C_BLUE)
    page.insert_text((MARGIN_LEFT + 12, net_y + 14), "DOMESTIC TRUNK CORRIDORS & AIRPORT HUB TAXONOMY", fontname="hebo", fontsize=8.0, color=C_BLUE)

    # Insert official transparent map
    try:
        m_rect = fitz.Rect(MARGIN_LEFT + 10, net_y + 24, MARGIN_LEFT + 175, net_y + 220)
        page.insert_image(m_rect, filename=ASSET_MAP_TRANSPARENT)
    except Exception:
        pass

    # Top 6 Trunk Corridors Table (Right of map)
    tbl_x = MARGIN_LEFT + 185
    tbl_w = CONTENT_WIDTH - 195
    t_headers = ["Corridor", "Dir", "Daily Dep", "DGCA Weight", "Base Fare", "30D Volatility"]
    t_cols = [75, 30, 55, 60, 55, 60]
    t_rows = [
        ["DEL - BOM", "Bi-dir", "78 flt/d", "14.20%", "INR 5,100", "+/- 18.4%"],
        ["BOM - BLR", "Bi-dir", "54 flt/d", "9.80%", "INR 4,200", "+/- 14.1%"],
        ["DEL - BLR", "Bi-dir", "52 flt/d", "8.90%", "INR 5,800", "+/- 16.2%"],
        ["CCU - DEL", "Bi-dir", "38 flt/d", "6.50%", "INR 5,000", "+/- 19.5%"],
        ["HYD - DEL", "Bi-dir", "36 flt/d", "5.40%", "INR 4,800", "+/- 12.8%"],
        ["MAA - DEL", "Bi-dir", "32 flt/d", "4.80%", "INR 5,300", "+/- 15.0%"],
        ["Other 36 Corridors", "Various", "1,240 flt/d", "50.40%", "Various", "+/- 22.4%"]
    ]
    draw_table(page, tbl_x, net_y + 26, tbl_w, t_headers, t_rows, t_cols, row_height=18, font_size=6.2)

    # Directional Asymmetry Analysis (Middle Strip)
    asym_y = net_y + 238
    draw_card(page, MARGIN_LEFT, asym_y, CONTENT_WIDTH, 120, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=C_PURPLE)
    page.insert_text((MARGIN_LEFT + 12, asym_y + 14), "DIRECTIONAL PRICE ASYMMETRY PHENOMENON", fontname="hebo", fontsize=7.8, color=C_PURPLE)

    page.insert_textbox(fitz.Rect(MARGIN_LEFT + 12, asym_y + 22, MARGIN_RIGHT - 12, asym_y + 115),
        "A common fallacy in consumer pricing is assuming that a round-trip route has symmetric directional pricing. AeroIndex empirical data demonstrates substantial directional divergence:\n\n"
        "* Sunday Evening Asymmetry: BOM -> DEL prices average 28.4% higher than DEL -> BOM on Sunday afternoons due to concentrated corporate executive travel returning to the national capital.\n"
        "* Friday Evening Asymmetry: DEL -> GOI (Goa) experiences an average 45.2% weekend leisure surcharge, while GOI -> DEL northbound operates at substantial discounts.\n"
        "* Aviation Fuel Tax (VAT) Variations: Different Indian states impose widely divergent local VAT on Aviation Turbine Fuel (e.g. 1% to 25%), creating structural cost differentials depending on where an aircraft uplifts fuel.",
        fontsize=6.5, fontname="helv", color=C_TEXT_MUTED
    )

    # Corridor Volatility & Route Tier Taxonomy (Bottom Grid)
    vol_y = asym_y + 128
    draw_card(page, MARGIN_LEFT, vol_y, CONTENT_WIDTH, 140, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=C_EMERALD)
    page.insert_text((MARGIN_LEFT + 12, vol_y + 14), "CORRIDOR VOLATILITY & ROUTE TIER TAXONOMY", fontname="hebo", fontsize=7.8, color=C_EMERALD)

    v_headers = ["Volatility Tier", "Representative Routes", "Competition Index (HHI)", "Daily Frequencies", "30-Day Fare Range", "Primary Yield Driver"]
    v_cols = [85, 110, 85, 75, 80, 88]
    v_rows = [
        ["Metro Trunk (Tier-1)", "DEL-BOM, BOM-BLR, DEL-BLR", "HHI: 3,420 (Oligopoly)", "50 - 80 daily flights", "INR 3,800 - 18,500", "Corporate walkup surge"],
        ["Metro Secondary", "CCU-DEL, HYD-DEL, MAA-DEL", "HHI: 3,890 (Duopoly)", "25 - 40 daily flights", "INR 3,400 - 14,200", "Midday corporate waves"],
        ["Seasonal Leisure", "DEL-GOI, BOM-GOI, DEL-SXR", "HHI: 4,100 (Peak seasonal)", "15 - 30 daily flights", "INR 4,200 - 24,000", "Holiday & weekend spikes"],
        ["Regional / Island", "IXZ-MAA (Port Blair), IXL-DEL", "HHI: 5,200 (Single-carrier)", "4 - 8 daily flights", "INR 6,500 - 16,800", "Inflexible capacity caps"]
    ]
    draw_table(page, MARGIN_LEFT + 6, vol_y + 24, CONTENT_WIDTH - 12, v_headers, v_rows, v_cols, row_height=18, font_size=6.2)

    draw_footer(page, 18)

def render_page_19(doc):
    """PAGE 19 -- CARRIER INTELLIGENCE"""
    page = init_page(doc)
    top_y = draw_header(
        page, 
        part_title="PART IV -- ANALYTICAL INTELLIGENCE",
        page_title="Carrier Intelligence & Market Architecture",
        page_subtitle="Pricing dispersion, airline market share vs. index basket weight, and fleet operating signatures",
        status="IMPLEMENTED IN CARRIER ENGINE", status_type="implemented"
    )

    # Top Narrative
    page.insert_textbox(fitz.Rect(MARGIN_LEFT, top_y, MARGIN_RIGHT, top_y + 35),
        "The Indian domestic aviation market is an oligopoly dominated by low-cost carriers. AeroIndex measures carrier pricing signatures without turning into a marketing leaderboard. Crucially, we separate official DGCA passenger market share from AeroIndex basket weights.",
        fontsize=7.8, fontname="helv", color=C_TEXT_MAIN
    )

    # DGCA Passenger Share vs AeroIndex Basket Weight Table
    tbl_y = top_y + 40
    headers = ["Carrier Code", "Operating Airline", "Business Model", "DGCA Pax Share", "AeroIndex Basket Weight", "Observed Flt Share", "Pricing Signature"]
    cols = [55, 90, 85, 75, 75, 75, 70]
    rows = [
        ["6E", "IndiGo", "Ultra LCC (Point-to-point)", "62.4%", "62.4%", "64.1%", "High Volume, Aggressive L01"],
        ["AI", "Air India", "Full Service (Hub-and-spoke)", "24.5%", "24.5%", "23.8%", "Premium Base, Included Baggage"],
        ["QP", "Akasa Air", "Ultra LCC (Modern 737 MAX)", "5.2%", "5.2%", "5.6%", "Discount Leisure, Metro Point"],
        ["SG", "SpiceJet", "LCC (Regional / Turboprop)", "4.1%", "4.1%", "3.9%", "High Volatility, Cashflow Yield"],
        ["Others", "Regional / Charter", "Commuter / Regional", "3.8%", "3.8%", "2.6%", "Regulated / UDAN Subsidized"]
    ]
    draw_table(page, MARGIN_LEFT, tbl_y, CONTENT_WIDTH, headers, rows, cols, row_height=20, font_size=6.4)

    # Carrier Yield Management Profiles (4 Cards)
    car_y = tbl_y + 140
    cw = (CONTENT_WIDTH - 24) / 4
    ch = 165
    
    profiles = [
        ("IndiGo (6E)", "Dominant Fleet Leader", "Operates >1,450 domestic flights daily. High schedule frequency gives 6E pricing power on late-afternoon corporate waves. Uses sharp L03/L01 price escalation.", C_BLUE),
        ("Air India (AI)", "Full-Service Network", "Consolidated group with Air India Express. Bundles 15kg baggage and meals. Prices average 8-15% higher than LCC competitors, reflecting higher product bundle value.", C_ROSE),
        ("Akasa Air (QP)", "High-Growth Agility", "Young Boeing 737 MAX fleet. Focuses on high-demand metro trunks (BOM, DEL, BLR). Uses aggressive L30/L14 advance purchase discounts to secure base load factors.", C_PURPLE),
        ("SpiceJet (SG)", "Operational Restructuring", "Network curtailed to core profitable routes and regional turboprop operations. Exhibits higher quote dispersion and occasional inventory availability drops.", C_AMBER)
    ]
    
    for idx, (c_name, c_sub, c_desc, c_col) in enumerate(profiles):
        cx = MARGIN_LEFT + idx * (cw + 8)
        draw_card(page, cx, car_y, cw, ch, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=c_col)
        page.insert_text((cx + 8, car_y + 14), c_name, fontname="hebo", fontsize=7.5, color=c_col)
        page.insert_text((cx + 8, car_y + 24), c_sub, fontname="helv", fontsize=6.0, color=C_TEXT_MUTED)
        page.insert_textbox(fitz.Rect(cx + 8, car_y + 32, cx + cw - 8, car_y + 155), c_desc, fontsize=6.2, fontname="helv", color=C_TEXT_MAIN)

    # Scientific Caution Callout
    bot_y = car_y + 175
    draw_card(page, MARGIN_LEFT, bot_y, CONTENT_WIDTH, 48, bg=C_BG_CARD_ALT, border=C_BORDER_CARD)
    page.insert_text((MARGIN_LEFT + 12, bot_y + 14), "NON-COMPARATIVE BENCHMARKING GUARANTEE:", fontname="hebo", fontsize=7.2, color=C_TEXT_MAIN)
    page.insert_textbox(fitz.Rect(MARGIN_LEFT + 12, bot_y + 18, MARGIN_RIGHT - 12, bot_y + 44),
        "AeroIndex does NOT declare an airline 'cheap' or 'expensive'. Price variations are rigorously normalized for ancillary inclusions (free baggage, meals, legroom). The index measures market price evolution, not airline operational efficiency.",
        fontsize=6.5, fontname="helv", color=C_TEXT_MUTED
    )

    draw_footer(page, 19)

def render_page_20(doc):
    """PAGE 20 -- CHANNEL INTELLIGENCE"""
    page = init_page(doc)
    top_y = draw_header(
        page, 
        part_title="PART IV -- ANALYTICAL INTELLIGENCE",
        page_title="Channel Intelligence & Price Parity Spreads",
        page_subtitle="Direct airline booking vs. OTA aggregator pricing, synchronization lag, and promotional spread distortion",
        status="IMPLEMENTED IN CHANNEL ENGINE", status_type="implemented"
    )

    # Narrative
    page.insert_textbox(fitz.Rect(MARGIN_LEFT, top_y, MARGIN_RIGHT, top_y + 35),
        "A flight ticket is sold across multiple competing distribution channels: Airline Direct websites, Online Travel Agencies (OTAs), and Corporate GDS aggregators. AeroIndex continuously tracks cross-channel parity spreads to detect channel-specific price divergence and stale inventory caches.",
        fontsize=7.8, fontname="helv", color=C_TEXT_MAIN
    )

    # Channel Ecosystem Breakdown (3 Cards)
    ch_y = top_y + 40
    cw = (CONTENT_WIDTH - 16) / 3
    ch_h = 135

    c_channels = [
        ("Airline Direct Web", "The Source-of-Truth Price", "* Zero intermediary convenience fees.\n* Direct fare family selection.\n* Lowest L01 cancellation fees.\n* Parity Base: 100.0 (Index Ref)", C_BLUE),
        ("Online Travel Agents (OTA)", "Aggregated Consumer Market", "* Convenience fee: +INR 299 to 450.\n* Coupon discounts: -INR 300 to 800.\n* Frequent cache latency (15-45m).\n* Spread: -4% to +6% vs Direct", C_CYAN),
        ("Corporate GDS Feeds", "Institutional Travel Agents", "* Unbundled business pricing.\n* Corporate cancellation policies.\n* Guaranteed availability seats.\n* Spread: +2% to +8% vs Direct", C_PURPLE)
    ]
    for idx, (ch_title, ch_sub, ch_desc, ch_col) in enumerate(c_channels):
        cx = MARGIN_LEFT + idx * (cw + 8)
        draw_card(page, cx, ch_y, cw, ch_h, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=ch_col)
        page.insert_text((cx + 10, ch_y + 14), ch_title, fontname="hebo", fontsize=7.5, color=ch_col)
        page.insert_text((cx + 10, ch_y + 24), ch_sub, fontname="helv", fontsize=6.0, color=C_TEXT_MUTED)
        page.insert_textbox(fitz.Rect(cx + 10, ch_y + 32, cx + cw - 10, ch_y + 125), ch_desc, fontsize=6.5, fontname="helv", color=C_TEXT_MAIN)

    # Cross-Channel Matching Equivalence Requirement (Middle)
    eq_y = ch_y + 145
    draw_card(page, MARGIN_LEFT, eq_y, CONTENT_WIDTH, 140, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=C_AMBER)
    page.insert_text((MARGIN_LEFT + 12, eq_y + 14), "THE STRICT EQUIVALENCE MATCHING MANDATE", fontname="hebo", fontsize=8.0, color=C_AMBER)

    page.insert_textbox(fitz.Rect(MARGIN_LEFT + 12, eq_y + 24, MARGIN_RIGHT - 12, eq_y + 132),
        "Methodological Imperative:\n"
        "Comparing channel prices is fraudulent unless the comparison evaluates the EXACT SAME physical flight instance, fare family, cabin class, and observation timestamp. For example, comparing an OTA unbundled 'Hand Baggage Only' fare against an Airline Direct 'Standard Saver' fare produces a false spread.\n\n"
        "AeroIndex Parity Spread Formula:\n"
        "  Parity_Spread(F, t) = [ ( Price_OTA(F, t) - Price_Direct(F, t) ) / Price_Direct(F, t) ] * 10,000  (in bps)\n\n"
        "Where F is the exact normalized flight instance tuple (Carrier, Flight#, Date, Cabin, Baggage Allowance).",
        fontsize=6.8, fontname="helv", color=C_TEXT_MUTED
    )

    # Channel Parity Matrix Sample Table (Bottom)
    bot_y = eq_y + 148
    headers = ["Flight Instance", "Direct Web Price", "OTA-A Price", "OTA-B Price", "GDS Price", "Parity Spread", "Audit Status"]
    cols = [85, 75, 70, 70, 65, 80, 80]
    rows = [
        ["6E-205 DEL -> BOM", "INR 5,420", "INR 5,220 (-promo)", "INR 5,420 (par)", "INR 5,580 (+fee)", "-369 bps to +295 bps", "VERIFIED PAR"],
        ["AI-806 BOM -> DEL", "INR 6,100", "INR 6,100 (par)", "INR 6,350 (+conv)", "INR 6,100 (par)", "0 bps to +410 bps", "VERIFIED PAR"],
        ["QP-1102 BLR -> DEL", "INR 5,092", "INR 4,892 (-promo)", "INR 5,092 (par)", "INR 5,200 (+fee)", "-392 bps to +212 bps", "VERIFIED PAR"],
        ["SG-8169 DEL -> BOM", "INR 5,418", "INR 5,418 (par)", "INR 5,800 (stale)", "INR 5,418 (par)", "0 bps to +705 bps", "STALE OTA DETECTED"]
    ]
    draw_table(page, MARGIN_LEFT, bot_y, CONTENT_WIDTH, headers, rows, cols, row_height=18, font_size=6.4)

    draw_footer(page, 20)

print("Part 4 (Pages 15 - 20) module loaded.")
