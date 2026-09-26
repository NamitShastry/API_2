"""
Theme, constants, styling, and reusable drawing primitives for AeroIndex 30-Page Research Dossier.
"""

import pymupdf as fitz

# Geometry (A4 Portrait)
PAGE_WIDTH = 595.28
PAGE_HEIGHT = 841.89
MARGIN_LEFT = 36.0
MARGIN_RIGHT = PAGE_WIDTH - MARGIN_LEFT  # 559.28
CONTENT_WIDTH = MARGIN_RIGHT - MARGIN_LEFT  # 523.28
MARGIN_TOP = 34.0
MARGIN_BOTTOM = 36.0
CONTENT_HEIGHT = PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM

# Color Palette (Bloomberg Terminal / Institutional Quant Research)
C_DARK_BG = (11/255, 17/255, 26/255)         # #0B111A deep slate/navy
C_DARK_CARD = (17/255, 24/255, 39/255)       # #111827
C_DARK_BORDER = (30/255, 41/255, 59/255)     # #1E293B
C_DARK_TEXT = (241/255, 245/255, 249/255)    # #F1F5F9

C_BG_PAGE = (255/255, 255/255, 255/255)      # Pure White
C_BG_CARD = (248/255, 250/255, 252/255)      # Slate-50
C_BG_CARD_ALT = (241/255, 245/255, 249/255)  # Slate-100
C_BORDER_CARD = (226/255, 232/255, 240/255)  # Slate-200
C_BORDER_LINE = (203/255, 213/255, 225/255)  # Slate-300

C_TEXT_MAIN = (15/255, 23/255, 42/255)       # Slate-900
C_TEXT_MUTED = (71/255, 85/255, 105/255)     # Slate-600
C_TEXT_LIGHT = (148/255, 163/255, 184/255)   # Slate-400

# Semantics
C_BLUE = (37/255, 99/255, 235/255)           # #2563EB Blue-600
C_BLUE_LIGHT = (239/255, 246/255, 255/255)   # Blue-50
C_CYAN = (8/255, 145/255, 178/255)           # #0891B2 Cyan-600
C_CYAN_LIGHT = (236/255, 254/255, 255/255)   # Cyan-50
C_EMERALD = (5/255, 150/255, 105/255)        # #059669 Emerald-600
C_EMERALD_LIGHT = (236/255, 253/255, 245/255)# Emerald-50
C_AMBER = (217/255, 119/255, 6/255)          # #D97706 Amber-600
C_AMBER_LIGHT = (254/255, 243/255, 199/255)  # Amber-100
C_ROSE = (220/255, 38/255, 38/255)           # #DC2626 Rose-600
C_ROSE_LIGHT = (254/255, 242/255, 242/255)   # Rose-50
C_PURPLE = (124/255, 58/255, 237/255)        # #7C3AED Violet-600
C_PURPLE_LIGHT = (245/255, 243/255, 255/255) # Violet-50
C_SLATE_DARK = (30/255, 41/255, 59/255)

ASSET_MAP_TRANSPARENT = "/Users/namitshastry/Desktop/Airfare Index/assets/india-official-transparent.png"
ASSET_MAP_DARK = "/Users/namitshastry/Desktop/Airfare Index/assets/india-official-darkmode.png"

def init_page(doc):
    """Creates a new page and binds standard fonts."""
    page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
    try:
        page.insert_font(fontname='menlo', fontfile='/System/Library/Fonts/Menlo.ttc')
    except Exception:
        pass
    return page

def draw_header(page, part_title, page_title, page_subtitle, status="IMPLEMENTED", status_type="implemented"):
    """Draws standardized institutional header for content pages."""
    y = MARGIN_TOP
    # Part Tracker tag
    page.insert_text((MARGIN_LEFT, y + 8), part_title.upper(), fontname="hebo", fontsize=7.2, color=C_BLUE)
    
    # Status Badge top right with dynamic width
    badge_w = max(85, len(status) * 4.8 + 14)
    draw_badge(page, MARGIN_RIGHT - badge_w, y, badge_w, 14, status, status_type)
    
    # Page Title
    page.insert_text((MARGIN_LEFT, y + 24), page_title, fontname="hebo", fontsize=14, color=C_TEXT_MAIN)
    
    # Subtitle
    if page_subtitle:
        page.insert_text((MARGIN_LEFT, y + 36), page_subtitle, fontname="helv", fontsize=8.0, color=C_TEXT_MUTED)
    
    # Divider rule
    page.draw_line((MARGIN_LEFT, y + 43), (MARGIN_RIGHT, y + 43), color=C_BORDER_CARD, width=0.8)
    return y + 50

def draw_footer(page, page_num, total_pages=30):
    """Draws standardized institutional footer with non-overlapping zones."""
    y = PAGE_HEIGHT - MARGIN_BOTTOM + 8
    # Divider rule
    page.draw_line((MARGIN_LEFT, y - 6), (MARGIN_RIGHT, y - 6), color=C_BORDER_CARD, width=0.6)
    
    # Left text (max width ~180pt)
    page.insert_text((MARGIN_LEFT, y + 6), "AEROINDEX / FAREOS  *  RESEARCH DOSSIER", fontname="hebo", fontsize=6.8, color=C_TEXT_LIGHT)
    
    # Center text
    center_text = "METHODOLOGY SPECIFICATION v2.4.1"
    page.insert_text((225, y + 6), center_text, fontname="menlo", fontsize=6.2, color=C_TEXT_LIGHT)
    
    # Right text
    right_text = f"PAGE {page_num:02d} / {total_pages:02d}"
    page.insert_text((MARGIN_RIGHT - 54, y + 6), right_text, fontname="menlo", fontsize=7.5, color=C_TEXT_MAIN)

def draw_badge(page, x, y, w, h, text, status_type="implemented"):
    """Draws clean status badge."""
    colors = {
        "implemented": (C_EMERALD_LIGHT, C_EMERALD),
        "partial": (C_AMBER_LIGHT, C_AMBER),
        "simulated": (C_CYAN_LIGHT, C_CYAN),
        "planned": (C_PURPLE_LIGHT, C_PURPLE),
        "conceptual": (C_BG_CARD_ALT, C_TEXT_MUTED),
        "unavailable": (C_BG_CARD_ALT, C_TEXT_LIGHT),
        "official": (C_BLUE_LIGHT, C_BLUE),
        "flash": (C_AMBER_LIGHT, C_AMBER),
    }
    bg, fg = colors.get(status_type.lower(), (C_BG_CARD_ALT, C_TEXT_MUTED))
    rect = fitz.Rect(x, y, x + w, y + h)
    page.draw_rect(rect, color=fg, fill=bg, width=0.6)
    # Center text roughly
    font_sz = 6.2
    text_w = len(text) * 4.0
    tx = max(x + 4, x + (w - text_w)/2)
    ty = y + h - 4.0
    page.insert_text((tx, ty), text.upper(), fontname="hebo", fontsize=font_sz, color=fg)

def draw_card(page, x, y, w, h, bg=C_BG_CARD, border=C_BORDER_CARD, border_width=0.7, left_accent=None):
    """Draws clean container card with optional left accent border."""
    rect = fitz.Rect(x, y, x + w, y + h)
    page.draw_rect(rect, color=border, fill=bg, width=border_width)
    if left_accent:
        accent_rect = fitz.Rect(x, y, x + 3.5, y + h)
        page.draw_rect(accent_rect, color=left_accent, fill=left_accent, width=0)

def draw_kpi(page, x, y, w, h, label, value, subtext="", status_badge=None, accent=C_BLUE):
    """Draws KPI metric card."""
    draw_card(page, x, y, w, h, bg=C_BG_CARD, border=C_BORDER_CARD, left_accent=accent)
    # Label
    page.insert_text((x + 8, y + 12), label.upper(), fontname="hebo", fontsize=6.8, color=C_TEXT_MUTED)
    # Status badge if any
    if status_badge:
        draw_badge(page, x + w - 75, y + 5, 68, 11, status_badge[0], status_badge[1])
    # Big Value
    page.insert_text((x + 8, y + 28), str(value), fontname="hebo", fontsize=14, color=C_TEXT_MAIN)
    # Subtext
    if subtext:
        page.insert_text((x + 8, y + 39), subtext, fontname="helv", fontsize=7.2, color=C_TEXT_MUTED)

def draw_table(page, x, y, w, headers, rows, col_widths, row_height=18, font_size=7.2, header_bg=C_SLATE_DARK, header_fg=C_BG_PAGE):
    """Draws structured tabular data with clean lines and cell alignment."""
    cur_y = y
    # Header Row
    header_rect = fitz.Rect(x, cur_y, x + w, cur_y + row_height)
    page.draw_rect(header_rect, color=header_bg, fill=header_bg, width=0)
    col_x = x + 6
    for i, h in enumerate(headers):
        page.insert_text((col_x, cur_y + row_height - 5.5), h.upper(), fontname="hebo", fontsize=font_size, color=header_fg)
        col_x += col_widths[i]
    cur_y += row_height
    
    # Rows
    for r_idx, row in enumerate(rows):
        bg = C_BG_CARD if (r_idx % 2 == 0) else C_BG_PAGE
        r_rect = fitz.Rect(x, cur_y, x + w, cur_y + row_height)
        page.draw_rect(r_rect, color=C_BORDER_CARD, fill=bg, width=0.5)
        col_x = x + 6
        for c_idx, cell in enumerate(row):
            txt = str(cell)
            # check if cell is numeric or status
            fg = C_TEXT_MAIN
            font = "helv"
            if txt in ["IMPLEMENTED", "VERIFIED", "ACTIVE"]:
                fg = C_EMERALD
                font = "hebo"
            elif txt in ["SIMULATED", "SYNTHETIC"]:
                fg = C_CYAN
                font = "hebo"
            elif txt in ["PLANNED", "CONCEPTUAL"]:
                fg = C_PURPLE
                font = "hebo"
            elif txt in ["STALE", "WARNING", "DEGRADED"]:
                fg = C_AMBER
                font = "hebo"
            elif txt.startswith("R") and len(txt) <= 4:
                font = "menlo"
                fg = C_BLUE
            elif txt.startswith("INR") or txt.startswith("+") or txt.startswith("-") or "%" in txt or txt.replace('.', '', 1).isdigit():
                font = "menlo"
                
            page.insert_text((col_x, cur_y + row_height - 5.5), txt, fontname=font, fontsize=font_size, color=fg)
            col_x += col_widths[c_idx]
        cur_y += row_height
    return cur_y

def draw_formula_box(page, x, y, w, h, title, formula, variable_lines):
    """Draws high-rigor mathematical formula card."""
    draw_card(page, x, y, w, h, bg=(248/255, 250/255, 252/255), border=C_BORDER_CARD, left_accent=C_PURPLE)
    # Title
    page.insert_text((x + 10, y + 14), title.upper(), fontname="hebo", fontsize=8.0, color=C_PURPLE)
    
    # Formula Box in Menlo
    f_bg = fitz.Rect(x + 10, y + 20, x + w - 10, y + 42)
    page.draw_rect(f_bg, color=C_BORDER_CARD, fill=(1.0, 1.0, 1.0), width=0.5)
    page.insert_text((x + 16, y + 34), formula, fontname="menlo", fontsize=9.2, color=C_TEXT_MAIN)
    
    # Variable explanation
    vy = y + 53
    for var, desc in variable_lines:
        page.insert_text((x + 12, vy), var, fontname="menlo", fontsize=7.2, color=C_TEXT_MAIN)
        page.insert_text((x + 75, vy), f": {desc}", fontname="helv", fontsize=7.2, color=C_TEXT_MUTED)
        vy += 11.5
    return y + h

def draw_bullet_list(page, x, y, items, bullet_color=C_BLUE, font_size=7.5, line_spacing=12):
    """Draws compact bulleted explanation."""
    cy = y
    for title, desc in items:
        # bullet dot
        page.draw_circle((x + 4, cy - 2.5), 1.8, color=bullet_color, fill=bullet_color, width=0)
        page.insert_text((x + 12, cy), title, fontname="hebo", fontsize=font_size, color=C_TEXT_MAIN)
        title_len = len(title) * 4.4
        page.insert_text((x + 14 + title_len, cy), f"-- {desc}", fontname="helv", fontsize=font_size, color=C_TEXT_MUTED)
        cy += line_spacing
    return cy

def draw_pipeline_step(page, x, y, w, h, step_num, name, desc, badge_txt="IMPLEMENTED", badge_type="implemented"):
    """Draws a pipeline stage card with clean vertical hierarchy."""
    draw_card(page, x, y, w, h, bg=C_BG_CARD, border=C_BORDER_CARD)
    # Circle step number top left
    page.draw_circle((x + 12, y + 12), 7.5, color=C_BLUE, fill=C_BLUE_LIGHT, width=0.8)
    page.insert_text((x + 10.0, y + 14.5), str(step_num), fontname="hebo", fontsize=6.8, color=C_BLUE)
    
    # Step name top left next to circle
    page.insert_text((x + 24, y + 14.5), name.upper()[:16], fontname="hebo", fontsize=6.5, color=C_TEXT_MAIN)
    
    # Mini badge below name
    draw_badge(page, x + 6, y + 23, 62, 10, badge_txt[:12], badge_type)
    
    # Description box below badge
    page.insert_textbox(fitz.Rect(x + 6, y + 35, x + w - 6, y + h - 4), desc, fontsize=5.8, fontname="helv", color=C_TEXT_MUTED)

print("Report Theme and Canvas primitives loaded.")
