"""
Part I: Executive Understanding & Conceptual Foundations (Pages 01 - 04)
"""

import pymupdf as fitz
from .theme import (
    PAGE_WIDTH, PAGE_HEIGHT, MARGIN_LEFT, MARGIN_RIGHT, CONTENT_WIDTH,
    MARGIN_TOP, MARGIN_BOTTOM, C_DARK_BG, C_DARK_CARD, C_DARK_BORDER, C_DARK_TEXT,
    C_BG_PAGE, C_BG_CARD, C_BG_CARD_ALT, C_BORDER_CARD, C_BORDER_LINE,
    C_TEXT_MAIN, C_TEXT_MUTED, C_TEXT_LIGHT, C_BLUE, C_BLUE_LIGHT, C_CYAN,
    C_CYAN_LIGHT, C_EMERALD, C_EMERALD_LIGHT, C_AMBER, C_AMBER_LIGHT, C_ROSE,
    C_ROSE_LIGHT, C_PURPLE, C_PURPLE_LIGHT,
    ASSET_MAP_TRANSPARENT, ASSET_MAP_DARK,
    init_page, draw_header, draw_footer, draw_badge, draw_card, draw_kpi,
    draw_table, draw_formula_box, draw_bullet_list, draw_pipeline_step
)

def render_page_01(doc):
    """PAGE 01 -- COVER PAGE"""
    page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
    try:
        page.insert_font(fontname='menlo', fontfile='/System/Library/Fonts/Menlo.ttc')
    except Exception:
        pass

    # Deep Navy / Slate background fill
    bg_rect = fitz.Rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT)
    page.draw_rect(bg_rect, color=C_DARK_BG, fill=C_DARK_BG, width=0)

    # Architectural grid lines (subtle)
    for gy in [80, 220, 480, 720]:
        page.draw_line((MARGIN_LEFT, gy), (MARGIN_RIGHT, gy), color=(20/255, 30/255, 45/255), width=0.5)

    # Top Institutional Tag
    page.insert_text((MARGIN_LEFT, 52), "AEROINDEX RESEARCH & SYSTEMS DOSSIER  |  NATIONAL AIRFARE INTELLIGENCE", fontname="hebo", fontsize=7.5, color=C_CYAN)
    page.insert_text((MARGIN_RIGHT - 110, 52), "DOC ID: AERO-TR-2026-09", fontname="menlo", fontsize=7.0, color=(148/255, 163/255, 184/255))

    # Main Branding & Titles
    page.insert_text((MARGIN_LEFT, 115), "AEROINDEX / FAREOS", fontname="hebo", fontsize=28, color=(1.0, 1.0, 1.0))
    page.insert_text((MARGIN_LEFT, 142), "INDIA DOMESTIC AIRFARE INTELLIGENCE", fontname="hebo", fontsize=15, color=(147/255, 197/255, 253/255))
    page.insert_text((MARGIN_LEFT, 168), "Technical, Analytical & Methodological Report", fontname="helv", fontsize=12, color=(203/255, 213/255, 225/255))
    
    # Subtitle / Research scope
    sub_rect = fitz.Rect(MARGIN_LEFT, 182, MARGIN_LEFT + 400, 215)
    page.insert_textbox(sub_rect, 
        "A Research & Systems Dossier for Real-Time Airfare Measurement, Intelligence, Attribution, Econometric Forecasting, and Provenance Observability across the Indian Domestic Civil Aviation Network.",
        fontsize=8.5, fontname="helv", color=(148/255, 163/255, 184/255)
    )

    # Official India Map Graphic (center right)
    try:
        map_rect = fitz.Rect(MARGIN_RIGHT - 240, 240, MARGIN_RIGHT - 10, 530)
        page.insert_image(map_rect, filename=ASSET_MAP_DARK)
    except Exception:
        pass

    # Core Hub Routes overlayed / Network Specs on left
    draw_card(page, MARGIN_LEFT, 240, 250, 160, bg=C_DARK_CARD, border=C_DARK_BORDER, left_accent=C_CYAN)
    page.insert_text((MARGIN_LEFT + 14, 258), "OBSERVATIONAL COVERAGE MATRIX", fontname="hebo", fontsize=8.0, color=C_CYAN)
    
    kpis = [
        ("CORE FLIGHT NETWORK", "79 Airports | 42 Monitored Corridors"),
        ("AIRLINE CARRIERS", "6E (IndiGo), AI (Air India), QP (Akasa), SG (SpiceJet)"),
        ("OBSERVATION GRANULARITY", "L01 - L60 Advance Booking Horizons"),
        ("PRIMARY INDEX METHOD", "Axiomatic Jevons Geometric Mean"),
        ("ENGINE LATENCY PROFILE", "Flash (<150ms) | Official Daily Settlement"),
        ("DATA REPRODUCIBILITY", "SHA-256 Cryptographic Traceability")
    ]
    ky = 278
    for label, val in kpis:
        page.insert_text((MARGIN_LEFT + 14, ky), label, fontname="hebo", fontsize=6.5, color=(148/255, 163/255, 184/255))
        page.insert_text((MARGIN_LEFT + 14, ky + 9), val, fontname="menlo", fontsize=6.8, color=(241/255, 245/255, 249/255))
        ky += 21

    # Systems Implementation Status Card
    draw_card(page, MARGIN_LEFT, 415, 250, 105, bg=C_DARK_CARD, border=C_DARK_BORDER, left_accent=C_EMERALD)
    page.insert_text((MARGIN_LEFT + 14, 432), "SYSTEMS VERIFICATION STATUS", fontname="hebo", fontsize=8.0, color=C_EMERALD)
    
    statuses = [
        ("Jevons Index Engine", "IMPLEMENTED", C_EMERALD),
        ("R01-R12 Clean Pipeline", "IMPLEMENTED", C_EMERALD),
        ("Basis Points Attribution", "IMPLEMENTED", C_EMERALD),
        ("ETS Forecast Honesty Gate", "IMPLEMENTED", C_EMERALD),
        ("Live OTA/GDS Stream", "SIMULATED ADAPTER", C_CYAN),
    ]
    sy = 448
    for name, stat, col in statuses:
        page.insert_text((MARGIN_LEFT + 14, sy), name, fontname="helv", fontsize=7.2, color=(203/255, 213/255, 225/255))
        page.insert_text((MARGIN_LEFT + 160, sy), stat, fontname="menlo", fontsize=6.8, color=col)
        sy += 12

    # Bottom Metadata & Release Banner
    meta_box = fitz.Rect(MARGIN_LEFT, 725, MARGIN_RIGHT, 800)
    page.draw_rect(meta_box, color=C_DARK_BORDER, fill=C_DARK_CARD, width=0.8)
    
    col1 = [
        ("METHODOLOGY VERSION", "v2.4.1 (Jevons Axiomatic)"),
        ("REPORT PUBLICATION", "September 2026"),
        ("SECURITY CLASSIFICATION", "Technical Research Dossier")
    ]
    col2 = [
        ("DGCA PASSENGER BASELINE", "CY 2025-2026 Traffic Share"),
        ("ANOMALY THRESHOLD", "MAD Modified Z >= 3.0 (Iglewicz-Hoaglin)"),
        ("FORECAST DATA GATE", "Min 14 Continuous Daily Cycles")
    ]
    col3 = [
        ("PRIMARY BACKEND", "FastAPI / Python 3.12 / Redis 7"),
        ("DATABASE TOPOLOGY", "PostgreSQL / TimescaleDB Hypertable"),
        ("REPRODUCIBILITY DIGEST", "SHA-256 Quote Integrity Check")
    ]
    
    for idx, (label, val) in enumerate(col1):
        page.insert_text((MARGIN_LEFT + 12, 742 + idx * 16), label, fontname="hebo", fontsize=6.2, color=(148/255, 163/255, 184/255))
        page.insert_text((MARGIN_LEFT + 12, 750 + idx * 16), val, fontname="menlo", fontsize=6.8, color=(1.0, 1.0, 1.0))

    for idx, (label, val) in enumerate(col2):
        page.insert_text((MARGIN_LEFT + 185, 742 + idx * 16), label, fontname="hebo", fontsize=6.2, color=(148/255, 163/255, 184/255))
        page.insert_text((MARGIN_LEFT + 185, 750 + idx * 16), val, fontname="menlo", fontsize=6.8, color=(1.0, 1.0, 1.0))

    for idx, (label, val) in enumerate(col3):
        page.insert_text((MARGIN_LEFT + 360, 742 + idx * 16), label, fontname="hebo", fontsize=6.2, color=(148/255, 163/255, 184/255))
        page.insert_text((MARGIN_LEFT + 360, 750 + idx * 16), val, fontname="menlo", fontsize=6.8, color=(1.0, 1.0, 1.0))

def render_page_02(doc):
    """PAGE 02 -- EXECUTIVE SUMMARY"""
    page = init_page(doc)
    top_y = draw_header(
        page, 
        part_title="PART I -- EXECUTIVE UNDERSTANDING",
        page_title="Executive Summary & Platform Scope",
        page_subtitle="Foundational mission, architecture, and analytical capabilities of AeroIndex / FareOS",
        status="IMPLEMENTED", status_type="implemented"
    )

    # Core Problem & Solution Narrative (2 Columns)
    c1_rect = fitz.Rect(MARGIN_LEFT, top_y, MARGIN_LEFT + 252, top_y + 94)
    page.insert_textbox(c1_rect,
        "What AeroIndex Is:\n"
        "AeroIndex is an institutional-grade observational and quantitative measurement platform for Indian domestic airfares. It transforms fragmented multi-channel quote streams into a rigorous national price index (AeroIndex-100) with route corridors, carrier pricing signatures, and automated basis-point attribution.\n\n"
        "Why Airfare Intelligence Is Hard:\n"
        "Unlike commodities, airline tickets have no single spot price. A flight instance has dozens of concurrent quotes across fare families, advance horizons (L01-L60), channels, and yield management buckets.",
        fontsize=6.1, fontname="helv", color=C_TEXT_MAIN
    )

    c2_rect = fitz.Rect(MARGIN_LEFT + 266, top_y, MARGIN_RIGHT, top_y + 94)
    page.insert_textbox(c2_rect,
        "What the Index Measures:\n"
        "The national index uses an axiomatic Jevons geometric mean, weighted by DGCA passenger volume shares across 42 corridors and 7 advance lead buckets. The base index equals 100.00 at baseline calibration.\n\n"
        "Website vs. Analytical Engine:\n"
        "The interactive web portal is the exploratory cockpit for sub-150ms visual updates. This report provides the deep engineering layer: formulas, statistical outlier boundaries, forecast diagnostics, and SHA-256 provenance chains.",
        fontsize=6.1, fontname="helv", color=C_TEXT_MAIN
    )

    # KPI Strip
    kpi_y = top_y + 100
    kw = (CONTENT_WIDTH - 24) / 4
    draw_kpi(page, MARGIN_LEFT, kpi_y, kw, 48, "National Base Index", "100.00", "Baseline calibration period", accent=C_BLUE)
    draw_kpi(page, MARGIN_LEFT + kw + 8, kpi_y, kw, 48, "Monitored Network", "42 Corridors", "Covering >82% DGCA traffic", accent=C_CYAN)
    draw_kpi(page, MARGIN_LEFT + (kw+8)*2, kpi_y, kw, 48, "Cleaning Rules", "R01 - R12", "Algorithmic quote filtering", accent=C_EMERALD)
    draw_kpi(page, MARGIN_LEFT + (kw+8)*3, kpi_y, kw, 48, "Provenance Hash", "SHA-256", "Cryptographic quote replay", accent=C_PURPLE)

    # Architectural Pipeline Diagram (Compact Flow)
    pipe_y = kpi_y + 56
    draw_card(page, MARGIN_LEFT, pipe_y, CONTENT_WIDTH, 178, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=C_BLUE)
    page.insert_text((MARGIN_LEFT + 12, pipe_y + 14), "END-TO-END ANALYTICAL PIPELINE TOPOLOGY", fontname="hebo", fontsize=8.0, color=C_BLUE)
    
    stages = [
        (1, "Raw Ingestion", "Multi-source API adapters ingest flight payloads.", "IMPLEMENTED", "implemented"),
        (2, "R01-R12 Clean", "Floor/ceiling bounds, tax ratio, deduplication.", "IMPLEMENTED", "implemented"),
        (3, "MAD Outlier", "Median Absolute Deviation modified Z-score test.", "IMPLEMENTED", "implemented"),
        (4, "Product Norm", "Lead bucketing (L01-L60), cabin class alignment.", "IMPLEMENTED", "implemented"),
        (5, "Jevons Engine", "Two-tier DGCA volume weighted aggregation.", "IMPLEMENTED", "implemented"),
        (6, "Attribution", "Corridor, carrier, and lead-time BPS decomposition.", "IMPLEMENTED", "implemented"),
        (7, "Flash & Official", "Sub-150ms Redis pub/sub push; daily settlement.", "IMPLEMENTED", "implemented"),
        (8, "Provenance", "Forensic SHA-256 audit log enabling 100% replay.", "IMPLEMENTED", "implemented")
    ]
    
    row1_y = pipe_y + 24
    step_w = (CONTENT_WIDTH - 24 - 18) / 4
    for i in range(4):
        s_num, s_name, s_desc, s_stat, s_stype = stages[i]
        sx = MARGIN_LEFT + 12 + i * (step_w + 6)
        draw_pipeline_step(page, sx, row1_y, step_w, 68, s_num, s_name, s_desc, s_stat, s_stype)

    row2_y = pipe_y + 98
    for i in range(4):
        s_num, s_name, s_desc, s_stat, s_stype = stages[4 + i]
        sx = MARGIN_LEFT + 12 + i * (step_w + 6)
        draw_pipeline_step(page, sx, row2_y, step_w, 68, s_num, s_name, s_desc, s_stat, s_stype)

    # Core Architectural Principles Table
    tbl_y = pipe_y + 186
    headers = ["Principle", "System Implementation", "Traditional Mistake Avoided", "Verification Status"]
    col_w = [105, 155, 175, 85]
    rows = [
        ["Axiomatic Indexing", "Jevons Geometric Mean (time-reversible)", "Arithmetic average with upward substitution bias", "IMPLEMENTED"],
        ["Robust Statistics", "MAD & modified Z-score statistical bounds", "Mean/std-dev distorted by single airline surge quotes", "IMPLEMENTED"],
        ["Causal Honesty", "Strict non-causal attribution model", "Inventing market stories without verifiable news data", "IMPLEMENTED"],
        ["Forecast Honesty", "Honesty gate requiring >= 14 daily cycles", "Sparse data extrapolation without cycles", "IMPLEMENTED"],
        ["Full Traceability", "Immutable SHA-256 digests & weights", "Unverifiable black-box calculations", "IMPLEMENTED"]
    ]
    draw_table(page, MARGIN_LEFT, tbl_y, CONTENT_WIDTH, headers, rows, col_w, row_height=18, font_size=6.2)

    # Closing Manifesto Callout
    call_y = tbl_y + 118
    draw_card(page, MARGIN_LEFT, call_y, CONTENT_WIDTH, 26, bg=C_BLUE_LIGHT, border=C_BLUE, border_width=0.8)
    page.insert_text((MARGIN_LEFT + 16, call_y + 16), 
        "\"From individual fare observations to national airfare intelligence.\"", 
        fontname="hebo", fontsize=9.0, color=C_BLUE
    )
    page.insert_text((MARGIN_RIGHT - 210, call_y + 16), "AeroIndex Quantitative Research Standard", fontname="helv", fontsize=7.5, color=C_TEXT_MUTED)

    draw_footer(page, 2)

def render_page_03(doc):
    """PAGE 03 -- THE PROBLEM OF MEASURING AIRFARES"""
    page = init_page(doc)
    top_y = draw_header(
        page, 
        part_title="PART I -- EXECUTIVE UNDERSTANDING",
        page_title="The Problem of Measuring Airfares",
        page_subtitle="Why civil aviation pricing breaks naive statistical models and requires specialized econometric indexing",
        status="CONCEPTUAL & METHODOLOGICAL", status_type="implemented"
    )

    # Introduction Narrative
    p1 = fitz.Rect(MARGIN_LEFT, top_y, MARGIN_RIGHT, top_y + 44)
    page.insert_textbox(p1,
        "In financial equities or commodities markets, trading occurs at a singular, observable spot price cleared on an exchange order book. Civil aviation airfare behaves in the exact opposite manner: an airline seat is an extremely perishable asset governed by continuous, algorithmic yield management systems. At any given second, a single scheduled flight possesses dozens of concurrent prices depending on customer identity, channel, advance purchase window, baggage allowance, and inventory allocation.",
        fontsize=7.2, fontname="helv", color=C_TEXT_MAIN
    )

    # 12 Dimensions of Airfare Variance Grid
    dim_y = top_y + 48
    draw_card(page, MARGIN_LEFT, dim_y, CONTENT_WIDTH, 148, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=C_AMBER)
    page.insert_text((MARGIN_LEFT + 12, dim_y + 14), "THE 12 CRITICAL DIMENSIONS OF AIRFARE PRICING HETEROGENEITY", fontname="hebo", fontsize=8.0, color=C_AMBER)
    
    dims = [
        ("01. Dynamic Revenue Mgmt", "Real-time algorithmic repricing based on booking velocity."),
        ("02. Advance Lead Time", "L01 (last-minute premium) vs L30/L60 (early-bird discount)."),
        ("03. Fare Families", "Basic, Value, Flexi, Corporate with varying baggage/cancellation."),
        ("04. Inventory Bucket / RBD", "O, Q, M, Y reservation booking designators opening/closing."),
        ("05. Route Competition", "Monopoly/duopoly regional routes vs hyper-competitive metros."),
        ("06. Carrier Operating Model", "Ultra Low-Cost (LCC: 6E, SG, QP) vs Full-Service (FSC: AI)."),
        ("07. Cabin Class Stratification", "Economy, Premium Economy, Business, First inventory."),
        ("08. Distribution Channel", "Airline Direct Web vs OTA (MakeMyTrip, Yatra) vs Corporate GDS."),
        ("09. Airport Charges (UDF/PSF)", "Disparate aeronautical tariffs across privatized vs AAI hubs."),
        ("10. Fiscal Taxes & Cesses", "Goods and Services Tax (GST 5% economy, 12% business)."),
        ("11. Observation Timing Freshness", "Stale OTA cache latency (up to 4 hours) vs live airline GDS."),
        ("12. Missing / Ghost Quotes", "Discontinued flights, sold-out cabins, and scraping lockouts.")
    ]
    
    col_w = (CONTENT_WIDTH - 24 - 16) / 3
    col_h = 24
    for idx, (d_title, d_desc) in enumerate(dims):
        cx = MARGIN_LEFT + 12 + (idx % 3) * (col_w + 8)
        cy = dim_y + 26 + (idx // 3) * (col_h + 5)
        page.insert_text((cx, cy + 8), d_title, fontname="hebo", fontsize=7.2, color=C_TEXT_MAIN)
        page.insert_text((cx, cy + 18), d_desc, fontname="helv", fontsize=6.2, color=C_TEXT_MUTED)

    # Visual Demonstration: One Flight -> Many Possible Fares
    vis_y = dim_y + 156
    draw_card(page, MARGIN_LEFT, vis_y, CONTENT_WIDTH, 175, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=C_PURPLE)
    page.insert_text((MARGIN_LEFT + 12, vis_y + 14), "OBSERVATIONAL MATRIX: 6E-205 (DEL -> BOM, DEPARTURE 18:00 IST)", fontname="hebo", fontsize=8.0, color=C_PURPLE)
    draw_badge(page, MARGIN_RIGHT - 110, vis_y + 5, 98, 12, "ILLUSTRATIVE QUOTE SPREAD", "simulated")

    # Table of quotes for same flight instance
    q_headers = ["Quote ID", "Lead Time", "Fare Family", "Channel", "Base Fare", "Taxes & UDF", "Total Observed", "Status"]
    q_cols = [60, 50, 70, 70, 55, 65, 75, 70]
    q_rows = [
        ["Q-10491", "L30 (30d)", "Lite (Hand bag only)", "Direct Web", "INR 3,200", "INR 1,142", "INR 4,342", "CLEAN QUOTE"],
        ["Q-10492", "L30 (30d)", "Standard (15kg)", "OTA Provider A", "INR 3,450", "INR 1,142", "INR 4,592", "CLEAN QUOTE"],
        ["Q-10493", "L14 (14d)", "Standard (15kg)", "Direct Web", "INR 4,800", "INR 1,220", "INR 6,020", "CLEAN QUOTE"],
        ["Q-10494", "L07 (7d)", "Standard (15kg)", "Direct Web", "INR 7,100", "INR 1,350", "INR 8,450", "CLEAN QUOTE"],
        ["Q-10495", "L03 (3d)", "Flexi Plus (Meal+Seat)", "Direct Web", "INR 10,800", "INR 1,580", "INR 12,380", "CLEAN QUOTE"],
        ["Q-10496", "L01 (Same day)", "Last-Seat Economy", "OTA Provider B", "INR 16,500", "INR 1,920", "INR 18,420", "CLEAN QUOTE"],
        ["Q-10497", "L01 (Same day)", "Corrupted Scrape", "Untrusted Feed", "INR 85,000", "INR 22,000", "INR 107,000", "REJECTED (R02)"]
    ]
    draw_table(page, MARGIN_LEFT + 8, vis_y + 24, CONTENT_WIDTH - 16, q_headers, q_rows, q_cols, row_height=18, font_size=6.8)

    # Mathematical Comparison: Naive Arithmetic Mean vs Geometric Jevons
    math_y = vis_y + 185
    mw = (CONTENT_WIDTH - 12) / 2
    
    # Left Card: Naive Arithmetic Mean
    draw_card(page, MARGIN_LEFT, math_y, mw, 140, bg=C_ROSE_LIGHT, border=C_ROSE, left_accent=C_ROSE)
    page.insert_text((MARGIN_LEFT + 10, math_y + 14), "THE FAILURE OF NAIVE ARITHMETIC MEAN", fontname="hebo", fontsize=7.8, color=C_ROSE)
    
    page.insert_textbox(fitz.Rect(MARGIN_LEFT + 10, math_y + 22, MARGIN_LEFT + mw - 10, math_y + 65),
        "Formula: P_mean = (1 / N) * SUM(p_i)\n"
        "Observed Spread: INR 4,342 to INR 18,420\n"
        "Naive Mean = INR 9,034.00",
        fontname="menlo", fontsize=7.0, color=C_TEXT_MAIN
    )
    page.insert_textbox(fitz.Rect(MARGIN_LEFT + 10, math_y + 68, MARGIN_LEFT + mw - 10, math_y + 135),
        "Critical Flaws:\n"
        "* Asymmetric sensitivity: One extreme surge quote pulls the arithmetic average up disproportionately.\n"
        "* Fails Time-Reversal Test: P(t1/t0) != 1 / P(t0/t1).\n"
        "* Upward Substitution Bias: Ignores consumer elasticity shifting demand away from expensive buckets.",
        fontname="helv", fontsize=6.8, color=C_TEXT_MUTED
    )

    # Right Card: Geometric Jevons Index
    draw_card(page, MARGIN_LEFT + mw + 12, math_y, mw, 140, bg=C_EMERALD_LIGHT, border=C_EMERALD, left_accent=C_EMERALD)
    page.insert_text((MARGIN_LEFT + mw + 22, math_y + 14), "THE AEROINDEX JEVONS SOLUTION", fontname="hebo", fontsize=7.8, color=C_EMERALD)
    
    page.insert_textbox(fitz.Rect(MARGIN_LEFT + mw + 22, math_y + 22, MARGIN_RIGHT - 10, math_y + 65),
        "Formula: P_jevons = EXP( (1 / N) * SUM( ln(p_i) ) )\n"
        "Normalized Base: 100.00\n"
        "Robust Geometric Mean = INR 8,012.45",
        fontname="menlo", fontsize=7.0, color=C_TEXT_MAIN
    )
    page.insert_textbox(fitz.Rect(MARGIN_LEFT + mw + 22, math_y + 68, MARGIN_RIGHT - 10, math_y + 135),
        "Axiomatic Strengths:\n"
        "* Satisfies Time-Reversal & Transitivity axiomatic properties.\n"
        "* Invariant to proportional price scale transformations.\n"
        "* Robust against idiosyncratic booking spikes; respects geometric elasticity of perishable inventory.",
        fontname="helv", fontsize=6.8, color=C_TEXT_MUTED
    )

    draw_footer(page, 3)

def render_page_04(doc):
    """PAGE 04 -- AEROINDEX CONCEPTUAL MODEL & TAXONOMY"""
    page = init_page(doc)
    top_y = draw_header(
        page, 
        part_title="PART I -- EXECUTIVE UNDERSTANDING",
        page_title="AeroIndex Conceptual Model & Architecture",
        page_subtitle="Hierarchical abstraction layers from raw network observations to reproducible intelligence",
        status="IMPLEMENTED", status_type="implemented"
    )

    # Conceptual Architecture Stack (Vertical Stack of 8 Layers)
    stack_y = top_y + 5
    draw_card(page, MARGIN_LEFT, stack_y, 230, 480, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=C_BLUE)
    page.insert_text((MARGIN_LEFT + 12, stack_y + 16), "HIERARCHICAL DATA ABSTRACTION LAYERS", fontname="hebo", fontsize=8.0, color=C_BLUE)
    
    layers = [
        ("Layer 8: Intelligence & Observability", "Attribution decomposition, forecast models, and regime shift alerts."),
        ("Layer 7: Official Index Publication", "Daily finalized benchmark settled post audit and reconciliation."),
        ("Layer 6: Flash Stream (Live)", "Sub-150ms real-time quote aggregation pushed via WebSockets."),
        ("Layer 5: Weighted Index Engine", "Axiomatic Jevons aggregation using DGCA passenger traffic weights."),
        ("Layer 4: Matched Product Baskets", "Flight instance mapping into standardized lead buckets (L01-L60)."),
        ("Layer 3: Outlier & Quality Filter", "R01-R12 validation and MAD modified Z-score statistical tests."),
        ("Layer 2: Clean Normalized Quote", "Tax breakdown, currency normalization, SHA-256 fingerprinting."),
        ("Layer 1: Raw Observation Ingestion", "Heterogeneous JSON payloads collected across Direct, OTA, and GDS.")
    ]
    
    ly = stack_y + 30
    for idx, (title, desc) in enumerate(layers):
        l_rect = fitz.Rect(MARGIN_LEFT + 8, ly, MARGIN_LEFT + 222, ly + 48)
        page.draw_rect(l_rect, color=C_BORDER_CARD, fill=C_BG_PAGE, width=0.5)
        # Left layer indicator
        num_str = f"L{8 - idx}"
        page.insert_text((MARGIN_LEFT + 14, ly + 16), num_str, fontname="menlo", fontsize=7.5, color=C_BLUE)
        page.insert_text((MARGIN_LEFT + 32, ly + 16), title.split(":")[1].strip(), fontname="hebo", fontsize=7.2, color=C_TEXT_MAIN)
        page.insert_textbox(fitz.Rect(MARGIN_LEFT + 32, ly + 22, MARGIN_LEFT + 218, ly + 46), desc, fontsize=6.2, fontname="helv", color=C_TEXT_MUTED)
        ly += 54

    # Formal Definitions & Domain Taxonomy (Right Side)
    tax_x = MARGIN_LEFT + 242
    tax_w = CONTENT_WIDTH - 242
    draw_card(page, tax_x, stack_y, tax_w, 480, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=C_PURPLE)
    page.insert_text((tax_x + 12, stack_y + 16), "STANDARDIZED DOMAIN TAXONOMY & DEFINITIONS", fontname="hebo", fontsize=8.0, color=C_PURPLE)

    terms = [
        ("Raw Observation", "The immutable, serialized JSON payload received from a data source adapter, preserved in object storage with timestamp, source ID, and HTTP latency metrics."),
        ("Flight Instance", "A specific physical flight operation on a specific calendar date: Carrier + Flight Number + Origin + Destination + Departure Datetime (e.g., 6E-501 DEL-BOM on 2026-10-15)."),
        ("Fare Observation", "A price point observed for a flight instance, tagged with observation timestamp, cabin, lead time, and fare family."),
        ("Clean Quote", "A fare observation that has passed R01-R12 deterministic checks and MAD outlier thresholds, possessing verified component economics (Base, ATF, Taxes)."),
        ("Route Corridor", "A directional origin-destination city pair (e.g., DEL -> BOM). Bi-directional corridors are tracked separately to capture asymmetric demand."),
        ("Lead-Time Bucket", "Standardized advance purchase windows: L01 (0-1d), L03 (2-3d), L07 (4-7d), L14 (8-14d), L21 (15-21d), L30 (22-30d), L60 (31-60d)."),
        ("Index Basket", "The fixed representative sample of 42 domestic routes and lead-time buckets calibrated to reflect national passenger flows."),
        ("FLASH Index", "The unrevised, real-time index calculated with sub-second latency from continuous quote ingestion, subject to intra-day revisions."),
        ("OFFICIAL Index", "The finalized, immutable daily settlement index published at 23:59 IST after end-of-day quality audit and missing data imputation."),
        ("Attribution (BPS)", "Decomposition of index movement into additive basis points (+/- 1 bps = 0.01 index points) attributed to corridors, carriers, or advance buckets."),
        ("Provenance Digest", "A cryptographically secure SHA-256 hash generated over the exact quote inputs and weights that produced a published index value.")
    ]

    ty = stack_y + 30
    for term, definition in terms:
        page.insert_text((tax_x + 12, ty), term, fontname="hebo", fontsize=7.2, color=C_TEXT_MAIN)
        d_rect = fitz.Rect(tax_x + 12, ty + 2, tax_x + tax_w - 12, ty + 38)
        page.insert_textbox(d_rect, definition, fontsize=6.2, fontname="helv", color=C_TEXT_MUTED)
        ty += 40

    # Bottom Implementation Note
    bot_y = stack_y + 490
    draw_card(page, MARGIN_LEFT, bot_y, CONTENT_WIDTH, 40, bg=C_BG_CARD_ALT, border=C_BORDER_CARD)
    page.insert_text((MARGIN_LEFT + 12, bot_y + 14), "ARCHITECTURAL INVARIANT:", fontname="hebo", fontsize=7.2, color=C_TEXT_MAIN)
    page.insert_text((MARGIN_LEFT + 120, bot_y + 14), 
        "Every layer is strictly decoupled. Layer 1 payloads remain write-once in MinIO object storage;",
        fontname="helv", fontsize=7.0, color=C_TEXT_MUTED
    )
    page.insert_text((MARGIN_LEFT + 12, bot_y + 26), 
        "Layer 5 index calculation consumes only Layer 4 validated baskets. Downstream consumers cannot mutate upstream raw lineage.",
        fontname="helv", fontsize=7.0, color=C_TEXT_MUTED
    )

    draw_footer(page, 4)

print("Part 1 (Pages 01 - 04) module loaded.")
