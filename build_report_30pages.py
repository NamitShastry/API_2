#!/usr/bin/env python3
"""
Master Builder for AeroIndex / FareOS Technical & Analytical Report
Generates the complete 30-Page Research Dossier PDF:
AeroIndex_FareOS_Technical_Analytical_Report.pdf
"""

import os
import sys
import time
import pymupdf as fitz

# Ensure root workspace is in sys.path
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

from scripts.report.part1 import (
    render_page_01, render_page_02, render_page_03, render_page_04
)
from scripts.report.part2 import (
    render_page_05, render_page_06, render_page_07, render_page_08
)
from scripts.report.part3 import (
    render_page_09, render_page_10, render_page_11, render_page_12,
    render_page_13, render_page_14
)
from scripts.report.part4 import (
    render_page_15, render_page_16, render_page_17, render_page_18,
    render_page_19, render_page_20
)
from scripts.report.part5 import (
    render_page_21, render_page_22, render_page_23, render_page_24,
    render_page_25
)
from scripts.report.part6_7 import (
    render_page_26, render_page_27, render_page_28, render_page_29,
    render_page_30
)

OUTPUT_PDF_PATH = os.path.join(WORKSPACE_DIR, "AeroIndex_FareOS_Technical_Analytical_Report.pdf")

def build_pdf():
    print("=" * 70)
    print("AEROINDEX / FAREOS RESEARCH DOSSIER GENERATOR")
    print("Building 30-Page Institutional Technical & Analytical Report...")
    print("=" * 70)
    
    start_time = time.time()
    doc = fitz.open()

    page_generators = [
        # Part I: Executive Understanding & Foundations
        (1, "Cover Page", render_page_01),
        (2, "Executive Summary", render_page_02),
        (3, "The Problem of Measuring Airfares", render_page_03),
        (4, "AeroIndex Conceptual Model & Taxonomy", render_page_04),
        
        # Part II: Data & Observation System
        (5, "Data Observation Universe", render_page_05),
        (6, "National Observability & Denominators", render_page_06),
        (7, "Data Acquisition & Multi-Source Architecture", render_page_07),
        (8, "Raw Observation to Clean Quote Transformation", render_page_08),
        
        # Part III: Methodology & Index Engine
        (9, "Quality Engine: Rules R01–R12", render_page_09),
        (10, "Robust Outlier Detection (MAD & Modified Z)", render_page_10),
        (11, "Fare Normalization & Component Economics", render_page_11),
        (12, "Fare Family & Cabin Normalization", render_page_12),
        (13, "Lead-Time Intelligence (L01-L60 Dynamics)", render_page_13),
        (14, "Index Construction & Axiomatic Jevons Engine", render_page_14),
        
        # Part IV: Analytical Intelligence & Attribution Engine
        (15, "Dual-State Publication: FLASH vs OFFICIAL", render_page_15),
        (16, "What Moved Today's Index: Attribution Hierarchy", render_page_16),
        (17, "Attribution Mathematics & Reconciled Identities", render_page_17),
        (18, "Route & Network Intelligence", render_page_18),
        (19, "Carrier Intelligence & Market Architecture", render_page_19),
        (20, "Channel Intelligence & Price Parity Spreads", render_page_20),
        
        # Part V: System Architecture & Real-Time Engine
        (21, "Anomaly & Regime-Shift Detection Engine", render_page_21),
        (22, "Nowcast & Econometric Forecasting Engine", render_page_22),
        (23, "Forecast Honesty Gate & Model Diagnostics", render_page_23),
        (24, "Real-Time Streaming System Architecture", render_page_24),
        (25, "Database Schema, API Contracts & System Topology", render_page_25),
        
        # Parts VI & VII: Quality, Provenance, Governance & Future Extensions
        (26, "Cryptographic Provenance & 'Reproduce This Number'", render_page_26),
        (27, "Data Quality States, Revision & Governance", render_page_27),
        (28, "Limitations, Bias & Observability Boundaries", render_page_28),
        (29, "Future Extensions & Strategic Research Roadmap", render_page_29),
        (30, "Final System Closed-Loop Architecture & Conclusion", render_page_30),
    ]

    for p_num, p_title, p_fn in page_generators:
        sys.stdout.write(f"Generating Page {p_num:02d} / 30: {p_title} ... ")
        sys.stdout.flush()
        p_fn(doc)
        print("DONE")

    print("-" * 70)
    print(f"Total pages rendered: {doc.page_count}")
    assert doc.page_count == 30, f"Expected exactly 30 pages, but got {doc.page_count}!"

    # Save PDF
    print(f"Saving compiled PDF to: {OUTPUT_PDF_PATH}")
    doc.save(OUTPUT_PDF_PATH, garbage=4, deflate=True)
    doc.close()

    elapsed = time.time() - start_time
    file_size_mb = os.path.getsize(OUTPUT_PDF_PATH) / (1024 * 1024)
    print("=" * 70)
    print(f"SUCCESS! 30-Page Research Dossier compiled in {elapsed:.2f}s")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Destination: {OUTPUT_PDF_PATH}")
    print("=" * 70)

if __name__ == "__main__":
    build_pdf()
