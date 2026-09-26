"""
Parts VI & VII: Quality, Provenance, Governance & Future Extensions (Pages 26 - 30)
"""

import pymupdf as fitz
from .theme import (
    PAGE_WIDTH, PAGE_HEIGHT, MARGIN_LEFT, MARGIN_RIGHT, CONTENT_WIDTH,
    MARGIN_TOP, MARGIN_BOTTOM, C_DARK_BG, C_DARK_CARD, C_DARK_BORDER,
    C_BG_PAGE, C_BG_CARD, C_BG_CARD_ALT, C_BORDER_CARD, C_BORDER_LINE,
    C_TEXT_MAIN, C_TEXT_MUTED, C_TEXT_LIGHT, C_BLUE, C_BLUE_LIGHT, C_CYAN,
    C_CYAN_LIGHT, C_EMERALD, C_EMERALD_LIGHT, C_AMBER, C_AMBER_LIGHT, C_ROSE,
    C_ROSE_LIGHT, C_PURPLE, C_PURPLE_LIGHT, C_SLATE_DARK,
    ASSET_MAP_TRANSPARENT, ASSET_MAP_DARK,
    init_page, draw_header, draw_footer, draw_badge, draw_card, draw_kpi,
    draw_table, draw_formula_box, draw_bullet_list, draw_pipeline_step
)

def render_page_26(doc):
    """PAGE 26 -- PROVENANCE & REPRODUCIBILITY"""
    page = init_page(doc)
    top_y = draw_header(
        page, 
        part_title="PART VI -- QUALITY, PROVENANCE & REPRODUCIBILITY",
        page_title="Cryptographic Provenance & 'Reproduce This Number'",
        page_subtitle="Forensic data lineage, immutable SHA-256 input digests, methodology versioning, and calculation replay",
        status="IMPLEMENTED IN SCHEMAS", status_type="implemented"
    )

    # Narrative
    page.insert_textbox(fitz.Rect(MARGIN_LEFT, top_y, MARGIN_RIGHT, top_y + 35),
        "In institutional finance and economic research, a number without provenance is an unverified assertion. AeroIndex treats reproducibility as a core engineering invariant. Every published index point is cryptographically anchored to its constituent raw inputs, quality rules, and weights.",
        fontsize=7.8, fontname="helv", color=C_TEXT_MAIN
    )

    # Lineage Reproduction Flow (Horizontal Step Stack)
    rep_y = top_y + 40
    draw_card(page, MARGIN_LEFT, rep_y, CONTENT_WIDTH, 140, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=C_PURPLE)
    page.insert_text((MARGIN_LEFT + 12, rep_y + 14), "THE 'REPRODUCE THIS NUMBER' SEVEN-STAGE FORENSIC CHAIN", fontname="hebo", fontsize=8.0, color=C_PURPLE)

    stages = [
        ("1. Index Value", "Published benchmark (e.g. 102.39 at 23:59 IST)."),
        ("2. Method Tag", "Methodology version v2.4.1 (Axiomatic Jevons)."),
        ("3. Input Baskets", "Exact set of 520 clean quotes matching corridor basket."),
        ("4. Clean Rules", "R01-R12 ruleset hash at time of calculation execution."),
        ("5. Weight Matrix", "DGCA corridor weights (W_r) & lead weights (w_b)."),
        ("6. Calculation", "Deterministic Python script executing Jevons engine."),
        ("7. Verification", "Re-run produces identical 102.39000000 with 0.00 drift.")
    ]
    sw = (CONTENT_WIDTH - 24 - 18) / 7
    for idx, (s_title, s_desc) in enumerate(stages):
        sx = MARGIN_LEFT + 12 + idx * (sw + 3)
        s_rect = fitz.Rect(sx, rep_y + 26, sx + sw, rep_y + 125)
        page.draw_rect(s_rect, color=C_BORDER_CARD, fill=C_BG_PAGE, width=0.5)
        page.insert_text((sx + 4, rep_y + 40), s_title, fontname="hebo", fontsize=6.2, color=C_PURPLE)
        page.insert_textbox(fitz.Rect(sx + 4, rep_y + 46, sx + sw - 4, rep_y + 120), s_desc, fontsize=5.6, fontname="helv", color=C_TEXT_MUTED)

    # Provenance Drawer Inspection Card (Middle)
    prov_y = rep_y + 148
    draw_card(page, MARGIN_LEFT, prov_y, CONTENT_WIDTH, 185, bg=C_DARK_CARD, border=C_DARK_BORDER, left_accent=C_CYAN)
    page.insert_text((MARGIN_LEFT + 12, prov_y + 14), "FORENSIC PROVENANCE DRAWER PAYLOAD (INSPECTED VIA UI / API)", fontname="hebo", fontsize=8.0, color=C_CYAN)
    draw_badge(page, MARGIN_RIGHT - 110, prov_y + 5, 98, 12, "SHA-256 VERIFIED", "implemented")

    json_provenance = (
        "{\n"
        '  "calculation_id": "calc_20260926_eod_001",\n'
        '  "published_index": 102.39000000,\n'
        '  "as_of_timestamp": "2026-09-26T23:59:59.000+05:30",\n'
        '  "methodology": "JEVONS_AXIOMATIC_TWO_TIER_v2.4.1",\n'
        '  "weights_snapshot_id": "weights_dgca_cy2025_v3",\n'
        '  "input_quote_count": 520,\n'
        '  "quarantined_quote_count": 18,\n'
        '  "input_quotes_sha256": "8f3b6c2d4a1e9750cf39b41829e1d8035a72091fc5e6b12a89047c3e41b892da",\n'
        '  "weights_matrix_sha256": "d41d8cd98f00b204e9800998ecf8427e02b0c3f58a7e4b9c1d2e3f4a5b6c7d8e",\n'
        '  "execution_environment": "Python 3.12.4 (FastAPI ASGI / Alpine 3.20)",\n'
        '  "reproducibility_status": "DETERMINISTIC_REPLAY_CERTIFIED"\n'
        "}"
    )
    page.insert_textbox(fitz.Rect(MARGIN_LEFT + 12, prov_y + 24, MARGIN_RIGHT - 12, prov_y + 175),
        json_provenance, fontsize=6.5, fontname="menlo", color=(203/255, 213/255, 225/255)
    )

    # Provenance Audit Protocol (Middle)
    cmd_y = prov_y + 190
    draw_card(page, MARGIN_LEFT, cmd_y, CONTENT_WIDTH, 42, bg=C_BG_CARD_ALT, border=C_BORDER_CARD)
    page.insert_text((MARGIN_LEFT + 12, cmd_y + 13), "AUDITOR REPLAY COMMAND & CLI EXECUTION:", fontname="hebo", fontsize=7.2, color=C_TEXT_MAIN)
    page.insert_textbox(fitz.Rect(MARGIN_LEFT + 12, cmd_y + 17, MARGIN_RIGHT - 12, cmd_y + 38),
        "Third-party auditors can execute `python -m services.api.app.engine.replay --calc-id calc_20260926_eod_001`. The CLI pulls the raw MinIO input slice, validates the SHA-256 hash, re-executes the calculation, and confirms zero numerical drift.",
        fontsize=6.5, fontname="helv", color=C_TEXT_MUTED
    )

    # Forensic Provenance Attributes Table (Bottom)
    bot_y = cmd_y + 50
    draw_card(page, MARGIN_LEFT, bot_y, CONTENT_WIDTH, 140, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=C_EMERALD)
    page.insert_text((MARGIN_LEFT + 12, bot_y + 14), "CRYPTOGRAPHIC PROVENANCE ATTRIBUTES & VERIFICATION AUDIT MATRIX", fontname="hebo", fontsize=7.8, color=C_EMERALD)

    p_headers = ["Lineage Layer", "Entity Checked", "Cryptographic Anchor", "Storage Subsystem", "Audit SLA"]
    p_cols = [95, 110, 135, 105, 78]
    p_rows = [
        ["Layer 1: Raw Stream", "520 raw API payloads", "SHA-256 input slice digest", "MinIO S3 (WORM)", "Immutable (7 Years)"],
        ["Layer 2: Clean Quotes", "R01-R12 filter passes", "Bitmask pass/quarantine hash", "TimescaleDB Hypertable", "Deterministic match"],
        ["Layer 3: Weights Matrix", "42 DGCA route weights", "Cryptographic matrix checksum", "PostgreSQL Config Table", "Annual audit cycle"],
        ["Layer 4: Engine Code", "Jevons python module", "Git Commit SHA (v2.4.1)", "Container Build Tag", "Zero runtime mutation"],
        ["Layer 5: Benchmark Seal", "National Index 102.39", "HMAC signed settlement token", "Public Ledger / API", "Permanent record"]
    ]
    draw_table(page, MARGIN_LEFT + 6, bot_y + 24, CONTENT_WIDTH - 12, p_headers, p_rows, p_cols, row_height=18, font_size=6.2)

    draw_footer(page, 26)

def render_page_27(doc):
    """PAGE 27 -- DATA QUALITY, REVISION & GOVERNANCE"""
    page = init_page(doc)
    top_y = draw_header(
        page, 
        part_title="PART VI -- QUALITY, PROVENANCE & REPRODUCIBILITY",
        page_title="Data Quality States, Revision & Governance",
        page_subtitle="Six explicit operational quality states, revision immutability, and auditable data lifecycle",
        status="IMPLEMENTED", status_type="implemented"
    )

    # Narrative
    page.insert_textbox(fitz.Rect(MARGIN_LEFT, top_y, MARGIN_RIGHT, top_y + 35),
        "AeroIndex rejects the oversimplified 'green = good' indicator common in superficial dashboards. Aviation data feeds continuously fluctuate between healthy, stale, degraded, and synthetic recovery modes. Explicit state labeling is an ethical prerequisite for quantitative research.",
        fontsize=7.8, fontname="helv", color=C_TEXT_MAIN
    )

    # Six Formal Data Quality States Grid
    state_y = top_y + 40
    sw = (CONTENT_WIDTH - 12) / 2
    sh = 78

    states = [
        ("VERIFIED / FRESH", "Latency < 20 min; 100% R01-R12 rules passed. Normal index computation active.", C_EMERALD, C_EMERALD_LIGHT),
        ("STALE OBSERVED", "Quote age 20 min to 4 hours. Eligible for Flash with warning; flagged for refresh.", C_AMBER, C_AMBER_LIGHT),
        ("DEGRADED / THROTTLED", "Source error rate 1-5% or latency > 2s. Scraper throttled; synthetic fill standby.", C_AMBER, C_AMBER_LIGHT),
        ("OFFLINE / BLACKOUT", "Source unreachable > 15 min. Automatic failover to secondary source or GDS.", C_ROSE, C_ROSE_LIGHT),
        ("SIMULATED / ILLUSTRATIVE", "Synthetic flight quotes generated by simulator adapter. Explicitly tagged.", C_CYAN, C_CYAN_LIGHT),
        ("QUARANTINED", "Failed deterministic R01-R12 rules or MAD outlier. Isolated in quarantine hypertable.", C_PURPLE, C_PURPLE_LIGHT)
    ]
    for idx, (st_name, st_desc, st_c, st_bg) in enumerate(states):
        sx = MARGIN_LEFT + (idx % 2) * (sw + 12)
        sy = state_y + (idx // 2) * (sh + 8)
        draw_card(page, sx, sy, sw, sh, bg=st_bg, border=st_c, left_accent=st_c)
        page.insert_text((sx + 10, sy + 14), st_name, fontname="hebo", fontsize=7.2, color=st_c)
        page.insert_textbox(fitz.Rect(sx + 10, sy + 22, sx + sw - 10, sy + sh - 6), st_desc, fontsize=6.2, fontname="helv", color=C_TEXT_MAIN)

    # Revision Governance Protocol (Middle)
    rev_y = state_y + (sh + 8) * 3 + 10
    draw_card(page, MARGIN_LEFT, rev_y, CONTENT_WIDTH, 140, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=C_BLUE)
    page.insert_text((MARGIN_LEFT + 12, rev_y + 14), "REVISION POLICY & IMMUTABILITY CONTRACTS", fontname="hebo", fontsize=8.0, color=C_BLUE)

    page.insert_textbox(fitz.Rect(MARGIN_LEFT + 12, rev_y + 24, MARGIN_RIGHT - 12, rev_y + 132),
        "Immutable Settlement Protocol:\n\n"
        "* FLASH Revisions: The Flash stream recalculates continuously. Flash values from 14:00 may differ from 16:00 as newer quotes arrive. This is normal price discovery.\n\n"
        "* OFFICIAL Seal: Once the daily settlement benchmark is sealed at 23:59:59 IST, it becomes read-only and immutable. It cannot be altered retroactively without a formal, version-controlled revision release (e.g. `OFFICIAL_v2.0`).\n\n"
        "* As-Of Query Semantics: The API supports `as_of: <timestamp>` queries. Re-querying an index value with the same `as_of` parameter always returns the exact state of knowledge available at that moment in history.",
        fontsize=6.8, fontname="helv", color=C_TEXT_MUTED
    )

    draw_footer(page, 27)

def render_page_28(doc):
    """PAGE 28 -- LIMITATIONS, BIAS & OBSERVABILITY BOUNDARIES"""
    page = init_page(doc)
    top_y = draw_header(
        page, 
        part_title="PART VII -- LIMITATIONS, GOVERNANCE & FUTURE EXTENSIONS",
        page_title="Limitations, Bias & Observability Boundaries",
        page_subtitle="What AeroIndex knows, what AeroIndex cannot know, and structural sampling boundaries",
        status="ACADEMIC & METHODOLOGICAL HONESTY", status_type="implemented"
    )

    # Top Narrative
    page.insert_textbox(fitz.Rect(MARGIN_LEFT, top_y, MARGIN_RIGHT, top_y + 35),
        "Scientific integrity requires declaring the exact boundaries of observational capability. AeroIndex is an airfare intelligence platform, not an omniscient oracle. Below is the explicit declaration of known biases, technical limitations, and unobserved variables.",
        fontsize=7.8, fontname="helv", color=C_TEXT_MAIN
    )

    # Side-by-Side: What AeroIndex Knows vs What It Cannot Know
    comp_y = top_y + 40
    cw = (CONTENT_WIDTH - 12) / 2
    ch = 220

    # Left: What AeroIndex Knows
    draw_card(page, MARGIN_LEFT, comp_y, cw, ch, bg=C_EMERALD_LIGHT, border=C_EMERALD, left_accent=C_EMERALD)
    page.insert_text((MARGIN_LEFT + 10, comp_y + 14), "WHAT AEROINDEX RIGOROUSLY MEASURES", fontname="hebo", fontsize=7.5, color=C_EMERALD)

    knows = [
        ("Public Retail Fares", "Published web, OTA, and GDS ticket quotes available to domestic retail passengers."),
        ("Lead-Time Yield Curves", "Dynamic price escalation across L01-L60 advance purchase windows."),
        ("Component Fee Splits", "Decomposition into base fare, fuel surcharge, UDF, PSF, and statutory GST."),
        ("Macro Movement Attribution", "Exact mathematical contribution of corridors, carriers, and lead buckets to index changes."),
        ("Statistical Price Outliers", "Modified Z-score anomalies confirmed by multi-quote corroboration.")
    ]
    ky = comp_y + 26
    for k_title, k_desc in knows:
        page.insert_text((MARGIN_LEFT + 10, ky), k_title, fontname="hebo", fontsize=6.8, color=C_TEXT_MAIN)
        page.insert_textbox(fitz.Rect(MARGIN_LEFT + 10, ky + 2, MARGIN_LEFT + cw - 10, ky + 34), k_desc, fontsize=6.0, fontname="helv", color=C_TEXT_MUTED)
        ky += 36

    # Right: What AeroIndex Cannot Know
    draw_card(page, MARGIN_LEFT + cw + 12, comp_y, cw, ch, bg=C_ROSE_LIGHT, border=C_ROSE, left_accent=C_ROSE)
    page.insert_text((MARGIN_LEFT + cw + 20, comp_y + 14), "WHAT AEROINDEX CANNOT CURRENTLY KNOW", fontname="hebo", fontsize=7.5, color=C_ROSE)

    unknowns = [
        ("Private Corporate Discounts", "Bespoke contracted corporate rates negotiated offline by large enterprise enterprises."),
        ("Actual Load Factor & Pax Counts", "Real-time seat occupancy prior to official DGCA monthly retrospective reports."),
        ("Airline Cost Structures", "Aircraft lease rates, physical fuel hedging contracts, crew salary structures."),
        ("Underlying Market Causality", "Whether a price spike was caused by weather, crew shortages, or commercial greed."),
        ("Flash Frequent Flyer Redemptions", "Award seat inventory and frequent flyer loyalty program redemptions.")
    ]
    uy = comp_y + 26
    for u_title, u_desc in unknowns:
        page.insert_text((MARGIN_LEFT + cw + 20, uy), u_title, fontname="hebo", fontsize=6.8, color=C_TEXT_MAIN)
        page.insert_textbox(fitz.Rect(MARGIN_LEFT + cw + 20, uy + 2, MARGIN_RIGHT - 10, uy + 34), u_desc, fontsize=6.0, fontname="helv", color=C_TEXT_MUTED)
        uy += 36

    # Structural Biases & Mitigations Table (Bottom)
    bot_y = comp_y + ch + 12
    headers = ["Known Sampling Bias", "Structural Cause in Aviation", "AeroIndex Methodological Mitigation", "Residual Risk"]
    cols = [110, 135, 155, 100]
    rows = [
        ["Metro Trunk Over-Representation", "High schedule frequency on 6 major metros", "DGCA passenger volume weighting balances Tier-1/2", "Low (Volume calibrated)"],
        ["Scraper Anti-Bot Throttling", "Carrier web defenses block high-frequency IP requests", "Distributed rotated adapters & GDS secondary feed", "Moderate (Requires SLAs)"],
        ["Promotional Coupon Masking", "OTAs show discounted totals via proprietary promos", "Fares matched to Direct carrier unbundled base", "Low (Direct baseline)"],
        ["Sold-Out Phantom Flights", "Scrapers report sold-out flights as 'missing data'", "Status explicitly tagged as 'Zero Inventory' vs error", "Low (Separated state)"]
    ]
    draw_table(page, MARGIN_LEFT, bot_y, CONTENT_WIDTH, headers, rows, cols, row_height=20, font_size=6.2)

    draw_footer(page, 28)

def render_page_29(doc):
    """PAGE 29 -- FUTURE EXTENSIONS ROADMAP"""
    page = init_page(doc)
    top_y = draw_header(
        page, 
        part_title="PART VII -- LIMITATIONS, GOVERNANCE & FUTURE EXTENSIONS",
        page_title="Future Extensions & Strategic Research Roadmap",
        page_subtitle="Planned analytical capabilities, machine learning models, and planned architectural extensions",
        status="PLANNED CAPABILITIES", status_type="planned"
    )

    # Narrative
    page.insert_textbox(fitz.Rect(MARGIN_LEFT, top_y, MARGIN_RIGHT, top_y + 35),
        "The following extensions represent planned research initiatives currently in algorithmic prototyping. They are strictly segregated from the operational production codebase and are labeled as PLANNED to preserve evidentiary integrity.",
        fontsize=7.8, fontname="helv", color=C_TEXT_MAIN
    )

    # Roadmap Grid (6 Research Projects)
    road_y = top_y + 40
    rw = (CONTENT_WIDTH - 12) / 2
    rh = 95

    projects = [
        ("1. SARIMAX Festival Regressors", "PLANNED", "Incorporates Hindu/Islamic festival calendars (Diwali, Holi, Eid, Puja) as exogenous regressors into time-series forecasting, capturing demand surges.", C_PURPLE),
        ("2. Real-Time Meteorological Coupling", "CONCEPTUAL", "Ingests IMD (India Meteorological Department) radar and fog advisories to detect weather-induced schedule cancellations and consequent walkup fare spikes.", C_BLUE),
        ("3. Agentic Research Copilot (LLM)", "PLANNED", "An enterprise conversational analyst powered by AGY SDK, providing natural language provenance queries and automated executive briefings.", C_EMERALD),
        ("4. Probabilistic Seat Availability (RBD)", "CONCEPTUAL", "Bayesian inference estimating probability distribution of remaining seats in specific reservation booking designators based on price velocity.", C_CYAN),
        ("5. International Cross-Border Expansion", "PLANNED", "Extending AeroIndex architecture to high-volume Indian international corridors (India to UAE/Gulf, Singapore, Thailand, UK, Europe).", C_AMBER),
        ("6. Historical Scenario Simulator & Replay", "PLANNED", "Interactive historical replay engine allowing risk managers to simulate ATF fuel tax cuts, airline bankruptcies, or airspace closures.", C_ROSE)
    ]
    for idx, (p_title, p_tag, p_desc, p_col) in enumerate(projects):
        px = MARGIN_LEFT + (idx % 2) * (rw + 12)
        py = road_y + (idx // 2) * (rh + 10)
        draw_card(page, px, py, rw, rh, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=p_col)
        page.insert_text((px + 10, py + 14), p_title, fontname="hebo", fontsize=7.2, color=p_col)
        draw_badge(page, px + rw - 75, py + 5, 68, 12, p_tag, "planned")
        page.insert_textbox(fitz.Rect(px + 10, py + 22, px + rw - 10, py + rh - 6), p_desc, fontsize=6.2, fontname="helv", color=C_TEXT_MAIN)

    # Strategic Milestone Timeline (Bottom)
    time_y = road_y + (rh + 10) * 3 + 10
    draw_card(page, MARGIN_LEFT, time_y, CONTENT_WIDTH, 120, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=C_PURPLE)
    page.insert_text((MARGIN_LEFT + 12, time_y + 14), "ESTIMATED RESEARCH & ENGINEERING TIMELINE", fontname="hebo", fontsize=8.0, color=C_PURPLE)

    milestones = [
        ("Q4 2026", "SARIMAX & Event Calendar Integration", "Calibrate festival regression coefficients across 42 domestic corridors."),
        ("Q1 2027", "Direct NDC Carrier Partnerships", "Transition from web scraping to bilateral airline NDC API agreements."),
        ("Q2 2027", "Agentic Natural Language Interface", "Deploy AGY SDK conversational assistant inside AeroIndex web workspace."),
        ("Q3 2027", "South Asia & Gulf International Expansion", "Launch AeroIndex-INTL covering Gulf (DXB, DOH) and ASEAN (SIN, BKK).")
    ]
    mw = (CONTENT_WIDTH - 24 - 18) / 4
    for idx, (m_date, m_title, m_desc) in enumerate(milestones):
        mx = MARGIN_LEFT + 12 + idx * (mw + 6)
        m_rect = fitz.Rect(mx, time_y + 24, mx + mw, time_y + 110)
        page.draw_rect(m_rect, color=C_BORDER_CARD, fill=C_BG_PAGE, width=0.5)
        page.insert_text((mx + 6, time_y + 38), m_date, fontname="menlo", fontsize=6.8, color=C_PURPLE)
        page.insert_text((mx + 6, time_y + 48), m_title, fontname="hebo", fontsize=6.0, color=C_TEXT_MAIN)
        page.insert_textbox(fitz.Rect(mx + 6, time_y + 54, mx + mw - 6, time_y + 105), m_desc, fontsize=5.6, fontname="helv", color=C_TEXT_MUTED)

    draw_footer(page, 29)

def render_page_30(doc):
    """PAGE 30 -- FINAL SYSTEM MAP & RESEARCH CONCLUSION"""
    page = init_page(doc)
    top_y = draw_header(
        page, 
        part_title="PART VII -- LIMITATIONS, GOVERNANCE & FUTURE EXTENSIONS",
        page_title="Final System Closed-Loop Architecture & Conclusion",
        page_subtitle="The end-to-end observational closed loop and foundational research conclusion",
        status="PRODUCTION SPECIFICATION", status_type="implemented"
    )

    # Complete End-to-End Closed Loop Map (Visual Stack)
    loop_y = top_y + 5
    draw_card(page, MARGIN_LEFT, loop_y, CONTENT_WIDTH, 260, bg=C_DARK_CARD, border=C_DARK_BORDER, left_accent=C_CYAN)
    page.insert_text((MARGIN_LEFT + 14, loop_y + 16), "THE AEROINDEX COMPLETE CLOSED-LOOP INTELLIGENCE TOPOLOGY", fontname="hebo", fontsize=8.0, color=C_CYAN)

    # 11-step pipeline chain
    pipe_steps = [
        ("01. INDIAN AVIATION MARKET", "2,790 scheduled commercial daily services across 79 operational airports.", C_TEXT_LIGHT),
        ("02. MULTI-SOURCE INGESTION", "Direct NDC APIs, OTA scrapers, GDS EDIFACT, and DGCA timetable registries.", C_BLUE),
        ("03. R01-R12 QUALITY ENGINE", "Deterministic floor/ceiling bounds, tax ratios, currency, and deduplication.", C_EMERALD),
        ("04. ROBUST MAD OUTLIER FILTER", "Iglewicz & Hoaglin modified Z-score test (|M| <= 3.5) shielding against flash spikes.", C_AMBER),
        ("05. PRODUCT BASKET MATCHING", "Lead-time bucketing (L01-L60) and fare family standardization (Hand-bag vs Saver).", C_PURPLE),
        ("06. AXIOMATIC JEVONS ENGINE", "Geometric mean price aggregation with two-tier DGCA volume route weighting.", C_CYAN),
        ("07. REAL-TIME FLASH & OFFICIAL", "Sub-150ms WebSocket streaming for live telemetry; audited 23:59 IST daily settlement.", C_BLUE),
        ("08. ATTRIBUTION DECOMPOSITION", "Exact additive basis points decomposition across corridors, carriers, and lead times.", C_EMERALD),
        ("09. ANOMALY & REGIME-SHIFT DETECTOR", "Multi-quote confirmed surge detection (|Z| >= 3.0) with non-causal reporting.", C_ROSE),
        ("10. ECONOMETRIC FORECAST & NOWCAST", "ETS Exponential Smoothing with Holt-Winters day-of-week cycles and Honesty Gate.", C_PURPLE),
        ("11. SHA-256 PROVENANCE AUDIT", "Cryptographic fingerprinting enabling 100% deterministic calculation replay.", C_CYAN)
    ]
    
    py = loop_y + 28
    for p_num, p_desc, p_col in pipe_steps:
        page.draw_rect(fitz.Rect(MARGIN_LEFT + 12, py, MARGIN_RIGHT - 12, py + 18), color=C_DARK_BORDER, fill=C_DARK_BG, width=0.5)
        page.insert_text((MARGIN_LEFT + 18, py + 12), p_num, fontname="menlo", fontsize=6.2, color=p_col)
        page.insert_text((MARGIN_LEFT + 195, py + 12), p_desc, fontname="helv", fontsize=5.8, color=(203/255, 213/255, 225/255))
        py += 20.5

    # Research Conclusion & Philosophy Box
    concl_y = loop_y + 270
    draw_card(page, MARGIN_LEFT, concl_y, CONTENT_WIDTH, 175, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=C_BLUE)
    page.insert_text((MARGIN_LEFT + 14, concl_y + 16), "FOUNDATIONAL RESEARCH CONCLUSION", fontname="hebo", fontsize=8.0, color=C_BLUE)

    page.insert_textbox(fitz.Rect(MARGIN_LEFT + 14, concl_y + 26, MARGIN_RIGHT - 14, concl_y + 165),
        "AeroIndex does not merely display airfares; it creates a traceable, mathematically rigorous analytical layer between fragmented civil aviation observations and interpretable market intelligence.\n\n"
        "By enforcing axiomatic index formulas, robust non-Gaussian outlier boundaries, strict denominator discipline, non-causal attribution honesty, and cryptographic input provenance, AeroIndex transforms chaotic booking screens into an institutional measurement instrument suitable for macroeconomists, aviation executives, and enterprise decision-makers.\n\n"
        "Where traditional interfaces offer transient search results, AeroIndex delivers a permanent, auditable historical record of Indian domestic airfare pricing dynamics.",
        fontsize=7.2, fontname="helv", color=C_TEXT_MAIN
    )

    # Concluding Manifesto Banner
    man_y = concl_y + 185
    man_rect = fitz.Rect(MARGIN_LEFT, man_y, MARGIN_RIGHT, man_y + 34)
    page.draw_rect(man_rect, color=C_DARK_BORDER, fill=C_DARK_BG, width=0.8)
    
    motto = "OBSERVE.   NORMALIZE.   MEASURE.   EXPLAIN.   REPRODUCE."
    m_len = len(motto) * 5.2
    page.insert_text(((PAGE_WIDTH - m_len)/2, man_y + 21), motto, fontname="hebo", fontsize=9.5, color=C_CYAN)

    # Institutional Sign-Off Card
    sign_y = man_y + 42
    draw_card(page, MARGIN_LEFT, sign_y, CONTENT_WIDTH, 65, bg=C_BG_CARD_ALT, border=C_BORDER_CARD)
    page.insert_text((MARGIN_LEFT + 12, sign_y + 13), "INSTITUTIONAL METHODOLOGY SPECIFICATION SIGN-OFF", fontname="hebo", fontsize=7.2, color=C_TEXT_MAIN)
    
    col_w = (CONTENT_WIDTH - 24) / 3
    c1 = [("RESEARCH LEAD", "Principal Data Scientist"), ("SYSTEM ARCHITECT", "Senior Quantitative Systems Lead")]
    c2 = [("METHODOLOGY VERSION", "v2.4.1 (Axiomatic Jevons)"), ("VERIFICATION STATUS", "REPLAY CERTIFIED (SHA-256)")]
    c3 = [("DEPLOYMENT STATUS", "PRODUCTION READY (AEROINDEX)"), ("DATA JURISDICTION", "Republic of India Civil Aviation")]
    
    for idx, (label, val) in enumerate(c1):
        page.insert_text((MARGIN_LEFT + 12, sign_y + 25 + idx*17), label, fontname="hebo", fontsize=5.8, color=C_TEXT_LIGHT)
        page.insert_text((MARGIN_LEFT + 12, sign_y + 34 + idx*17), val, fontname="menlo", fontsize=6.2, color=C_TEXT_MAIN)
    for idx, (label, val) in enumerate(c2):
        page.insert_text((MARGIN_LEFT + 12 + col_w, sign_y + 25 + idx*17), label, fontname="hebo", fontsize=5.8, color=C_TEXT_LIGHT)
        page.insert_text((MARGIN_LEFT + 12 + col_w, sign_y + 34 + idx*17), val, fontname="menlo", fontsize=6.2, color=C_BLUE)
    for idx, (label, val) in enumerate(c3):
        page.insert_text((MARGIN_LEFT + 12 + col_w*2, sign_y + 25 + idx*17), label, fontname="hebo", fontsize=5.8, color=C_TEXT_LIGHT)
        page.insert_text((MARGIN_LEFT + 12 + col_w*2, sign_y + 34 + idx*17), val, fontname="menlo", fontsize=6.2, color=C_EMERALD)

    draw_footer(page, 30)

print("Parts 6 & 7 (Pages 26 - 30) module loaded.")
