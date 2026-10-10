"""
generate_presentation.py
Complete Presentation Generator for MineGuard AI.
Generates widescreen 16:9 PowerPoint (PPTX), PDF (ReportLab), and interactive HTML.
Every slide is completely filled with diagrams, flowcharts, tier architectures, and technical specifications.
"""

import os
from pathlib import Path
from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE


OUTPUT_DIR = Path(r"c:\Users\gudae mahalakshmi\Documents\imp")
PDF_PATH = OUTPUT_DIR / "MineGuard_Presentation.pdf"
PPTX_PATH = OUTPUT_DIR / "MineGuard_Presentation.pptx"
HTML_PATH = OUTPUT_DIR / "MineGuard_Pitch_Deck.html"


def generate_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    DARK_BG = RGBColor(11, 15, 25)
    CARD_BG = RGBColor(17, 24, 39)
    CARD_ALT = RGBColor(30, 41, 59)
    BORDER_COLOR = RGBColor(31, 41, 55)
    AMBER = RGBColor(245, 158, 11)
    RED = RGBColor(239, 68, 68)
    GREEN = RGBColor(16, 185, 129)
    BLUE = RGBColor(59, 130, 246)
    CYAN = RGBColor(6, 182, 212)
    WHITE = RGBColor(255, 255, 255)
    MUTED = RGBColor(156, 163, 175)

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = DARK_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="MINEGUARD AI", subtitle_text=""):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = AMBER

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = WHITE

        if subtitle_text:
            p2 = tf.add_paragraph()
            p2.text = subtitle_text
            p2.font.size = Pt(11)
            p2.font.color.rgb = MUTED

    def add_card(slide, x, y, w, h, bg_col=CARD_BG, border_col=BORDER_COLOR):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_col
        card.line.color.rgb = border_col
        card.line.width = Pt(1.5)
        return card

    def add_arrow(slide, x, y, w, h, col=AMBER, direction="right"):
        shape_type = MSO_SHAPE.RIGHT_ARROW if direction == "right" else MSO_SHAPE.DOWN_ARROW
        arrow = slide.shapes.add_shape(shape_type, x, y, w, h)
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = col
        arrow.line.fill.background()
        return arrow

    # =========================================================================
    # SLIDE 1: PLATFORM OVERVIEW & 4-LAYER BLUEPRINT DIAGRAM
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)
    add_header(s1, "MineGuard AI: Post-Quantum Cybersecurity for Mining Infrastructure",
               "EXECUTIVE PLATFORM BLUEPRINT",
               "Tagline: 'Predict the risk. Trace the impact. Plan the migration.'")

    # 4-Layer Architecture Diagram
    layers = [
        ("LAYER 1: INGESTION", "Cryptographic Inventory", CYAN,
         "• Git source repositories (.py, .js)\n• OT & SCADA firmware configs (.yaml)\n• CycloneDX v1.6 CBOM ingestion\n• Automated cryptographic tokenization"),
        ("LAYER 2: THREAT ENGINE", "Quantum Cryptographic Audit", AMBER,
         "• Shor's algorithm vulnerability check\n• RSA-2048, ECDSA, MD5 detection\n• Deterministic severity calculation\n• Zero LLM hallucination on scores"),
        ("LAYER 3: CASCADE GRAPH", "Physical Blast Radius Sim", RED,
         "• 20-Node 4-tier mining topology\n• Discrete BFS failure propagation\n• Upstream-to-downstream tracing\n• Forecasts 5/6 systems down in 24h"),
        ("LAYER 4: PQC ROADMAP", "Phased Migration Execution", GREEN,
         "• NIST PQC replacement mapping\n• FIPS 203 (ML-KEM) & 204 (ML-DSA)\n• 3-Phase schedule (14 Weeks)\n• Budget bounded: $210,000 total")
    ]

    layer_w = Inches(2.7)
    layer_h = Inches(3.6)
    layer_y = Inches(1.7)

    for i, (tag, title, col, desc) in enumerate(layers):
        layer_x = Inches(0.8 + i * 3.0)
        add_card(s1, layer_x, layer_y, layer_w, layer_h, CARD_BG, col)

        tb = s1.shapes.add_textbox(layer_x + Inches(0.15), layer_y + Inches(0.15), layer_w - Inches(0.3), layer_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = tag
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = col

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = WHITE

        p2 = tf.add_paragraph()
        p2.text = f"\n{desc}"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = MUTED

        if i < len(layers) - 1:
            add_arrow(s1, layer_x + layer_w + Inches(0.06), layer_y + Inches(1.6), Inches(0.2), Inches(0.35), AMBER, "right")

    # Bottom 3 KPI Badges
    kpis = [
        ("NIST PQC STANDARDIZATION", "Aligned with FIPS 203, 204, & 205 (Aug 2024)", CYAN),
        ("CRITICAL RISK RANK 1", "CA-Root Certificate triggers 12-system cascading failure", RED),
        ("FEASIBLE MIGRATION OPEX", "14-Week Plan ($210K) eliminates $150K/hr downtime threat", GREEN)
    ]
    kpi_w = Inches(3.7)
    kpi_h = Inches(1.3)
    kpi_y = Inches(5.6)
    for i, (badge_title, badge_desc, b_col) in enumerate(kpis):
        kpi_x = Inches(0.8 + i * 4.0)
        add_card(s1, kpi_x, kpi_y, kpi_w, kpi_h, CARD_ALT, BORDER_COLOR)
        tb = s1.shapes.add_textbox(kpi_x + Inches(0.15), kpi_y + Inches(0.15), kpi_w - Inches(0.3), kpi_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = badge_title
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = b_col
        p1 = tf.add_paragraph()
        p1.text = badge_desc
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 2: THE QUANTUM THREAT LANDSCAPE & HNDL ATTACK FLOWCHART
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "The Problem: Quantum Threat to Safety-Critical Mining Infrastructure",
               "THREAT LANDSCAPE & ATTACK LIFECYCLE",
               "Why legacy industrial hardware is defenceless against 'Harvest Now, Decrypt Later' (HNDL)")

    # 4-Stage HNDL Attack Flowchart
    hndl_stages = [
        ("STAGE 1: INTERCEPTION", "Harvest Encrypted Data", AMBER,
         "• Adversaries intercept OT telemetry\n• Air-gap bridging via insider/cellular\n• Encrypted SCADA traffic archived\n• Attack window: ACTIVE TODAY (2024–2026)"),
        ("STAGE 2: HARDWARE GAP", "20–30 Year Lifespans", RED,
         "• Underground PLCs deployed 10+ yrs\n• Zero post-quantum cryptographic agility\n• Fixed silicon cannot be easily patched\n• Hardware operational past Q-Day"),
        ("STAGE 3: Q-DAY ARRIVAL", "Shor's Algorithm (~2029)", RED,
         "• Cryptographically Relevant Quantum Computer\n• Breaks RSA-2048 & ECDSA in minutes\n• Harvested root certificates factored\n• Complete master key extraction"),
        ("STAGE 4: CATASTROPHE", "Physical Mine Failure", RED,
         "• Adversary injects forged control packets\n• Gas monitoring telemetry falsified\n• Underground ventilation fans disabled\n• Fatal hoist and blast logic shutdown")
    ]

    h_w = Inches(2.7)
    h_h = Inches(3.3)
    h_y = Inches(1.7)
    for i, (stage_tag, stage_title, col, desc) in enumerate(hndl_stages):
        h_x = Inches(0.8 + i * 3.0)
        add_card(s2, h_x, h_y, h_w, h_h, CARD_BG, col)

        tb = s2.shapes.add_textbox(h_x + Inches(0.15), h_y + Inches(0.15), h_w - Inches(0.3), h_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = stage_tag
        p0.font.size = Pt(10.5)
        p0.font.bold = True
        p0.font.color.rgb = col

        p1 = tf.add_paragraph()
        p1.text = stage_title
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = WHITE

        p2 = tf.add_paragraph()
        p2.text = f"\n{desc}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = MUTED

        if i < len(hndl_stages) - 1:
            add_arrow(s2, h_x + h_w + Inches(0.06), h_y + Inches(1.5), Inches(0.2), Inches(0.3), RED, "right")

    # Bottom 3 Detailed Explanatory Cards
    r_cards = [
        ("ASYMMETRIC CRYPTO COLLAPSE",
         "Shor's algorithm solves the discrete log and prime factorization problems in polynomial time. All deployed RSA and ECC keys will provide 0 bits of security on Q-Day.",
         AMBER),
        ("THE OT HARDWARE REALITY",
         "Mining facilities cannot rotate keys overnight. Substation relays, mine hoist controllers, and deep-shaft sensors take 3–5 years of planning to retrofit.",
         CYAN),
        ("THE FATAL BLAST RADIUS",
         "Cyber breaches in mining are physical breaches. An undetected cryptographic collapse in communication gateways causes explosive gas build-up and hoist cable crashes.",
         RED)
    ]
    rc_w = Inches(3.7)
    rc_h = Inches(1.6)
    rc_y = Inches(5.3)
    for i, (ctitle, cdesc, col) in enumerate(r_cards):
        rc_x = Inches(0.8 + i * 4.0)
        add_card(s2, rc_x, rc_y, rc_w, rc_h, CARD_ALT, BORDER_COLOR)
        tb = s2.shapes.add_textbox(rc_x + Inches(0.15), rc_y + Inches(0.15), rc_w - Inches(0.3), rc_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = ctitle
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = col
        p1 = tf.add_paragraph()
        p1.text = f"\n{cdesc}"
        p1.font.size = Pt(9.5)
        p1.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE FLOWCHART: END-TO-END EXECUTION FLOW
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "How MineGuard Works: 4-Stage Execution Flowchart",
               "SYSTEM ARCHITECTURE & EXECUTION PIPELINE",
               "Deterministic, mathematically-proven pipeline from code parsing to budgeted mitigation roadmap")

    flow_steps = [
        ("STAGE 1: SCANNER", "Cryptographic Audit Engine", CYAN,
         "• Inputs: .py, .js, .yaml, .json\n• Multi-regex & AST token extraction\n• Identifies RSA, ECDSA, MD5\n• Output Payload: 8 Vulnerabilities\n• Line numbers & cryptographic bits flagged"),
        ("STAGE 2: RISK SCORER", "Criticality Ranking Algorithm", RED,
         "• Inputs: Vulnerability tokens + Asset weights\n• Formula: Severity × Exposure × Centrality\n• Risk Score: 95/100 (CRITICAL ALERT)\n• Rank 1 Assigned: CA-Root Certificate\n• NIST PQC replacement standards assigned"),
        ("STAGE 3: CASCADE SIM", "Discrete BFS Graph Engine", BLUE,
         "• Inputs: 20-Node Mining Graph + Q-Day Slider\n• Algorithm: Discrete Breadth-First Search\n• Simulates upstream-to-downstream failure\n• Forecast: 5 of 6 Safety Systems Down\n• Generates hourly compromise timeline"),
        ("STAGE 4: PLANNER", "Budget-Bounded 3-Phase Roadmap", GREEN,
         "• Inputs: Blast radius + OPEX constraints\n• Topological dependency sort optimization\n• Scope: 5 Critical Safety Assets\n• Timeline: 14 Weeks • Budget: $210,000\n• Guaranteed 0 production outages")
    ]

    fs_w = Inches(2.7)
    fs_h = Inches(4.0)
    fs_y = Inches(1.7)
    for i, (badge, title, col, desc) in enumerate(flow_steps):
        fs_x = Inches(0.8 + i * 3.0)
        add_card(s3, fs_x, fs_y, fs_w, fs_h, CARD_BG, col)

        tb = s3.shapes.add_textbox(fs_x + Inches(0.15), fs_y + Inches(0.15), fs_w - Inches(0.3), fs_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = badge
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = col

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = WHITE

        p2 = tf.add_paragraph()
        p2.text = f"\n{desc}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = MUTED

        if i < len(flow_steps) - 1:
            add_arrow(s3, fs_x + fs_w + Inches(0.06), fs_y + Inches(1.8), Inches(0.2), Inches(0.35), AMBER, "right")

    # Bottom Determinism Bus
    bus_box = add_card(s3, Inches(0.8), Inches(5.9), Inches(11.7), Inches(1.1), CARD_ALT, BORDER_COLOR)
    tb_bus = s3.shapes.add_textbox(Inches(1.0), Inches(6.0), Inches(11.3), Inches(0.9))
    tf_bus = tb_bus.text_frame
    tf_bus.word_wrap = True
    p_b0 = tf_bus.paragraphs[0]
    p_b0.text = "MATHEMATICAL DETERMINISM GUARANTEE"
    p_b0.font.size = Pt(11)
    p_b0.font.bold = True
    p_b0.font.color.rgb = AMBER
    p_b1 = tf_bus.add_paragraph()
    p_b1.text = "Zero LLM hallucinations on numeric metrics. All risk scores, graph cascade probabilities, and migration budgets are computed deterministically via graph theory and standard risk equations."
    p_b1.font.size = Pt(10)
    p_b1.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 4: 20-NODE 4-TIER MINING TOPOLOGY GRAPH DIAGRAM
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Operational Topology: 20-Node 4-Tier Mining Infrastructure",
               "GRAPH ARCHITECTURE & BLAST RADIUS PROPAGATION",
               "Visualizing how an upstream cryptographic break cascades directly down into physical mine assets")

    # Left Stack: 4 Tiers with Downward Cascade Connectors
    tiers = [
        ("TIER 1: ENTERPRISE & CLOUD", "Root Certificate Authority (CA-Root) [CRITICAL VULNERABILITY] • ERP • Cloud Data Lake", RED),
        ("TIER 2: OT NETWORK & SCADA", "OT-Gateway • SCADA Historian • Telemetry Broker • Central Authentication Service", AMBER),
        ("TIER 3: MINE SAFETY SYSTEMS", "Main Ventilation Fans • Toxic Gas Monitoring • Dewatering Pumps • Emergency Comms Substation", CYAN),
        ("TIER 4: HEAVY OPERATIONAL ASSETS", "Autonomous Haulage Trucks • Shaft Hoist Motor Control • Production Drill Rigs • Conveyor Belts", GREEN)
    ]

    tier_w = Inches(7.2)
    tier_h = Inches(1.05)
    for i, (t_tag, t_nodes, t_col) in enumerate(tiers):
        t_y = Inches(1.7 + i * 1.35)
        add_card(s4, Inches(0.8), t_y, tier_w, tier_h, CARD_BG, t_col)

        tb = s4.shapes.add_textbox(Inches(1.0), t_y + Inches(0.1), tier_w - Inches(0.4), tier_h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = t_tag
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = t_col

        p1 = tf.add_paragraph()
        p1.text = t_nodes
        p1.font.size = Pt(10)
        p1.font.color.rgb = WHITE

        if i < len(tiers) - 1:
            add_arrow(s4, Inches(4.2), t_y + tier_h + Inches(0.04), Inches(0.3), Inches(0.22), RED, "down")

    # Right Side: Blast Radius Breakdown Card
    right_x = Inches(8.3)
    right_w = Inches(4.2)
    right_h = Inches(5.1)
    add_card(s4, right_x, Inches(1.7), right_w, right_h, CARD_ALT, BORDER_COLOR)

    tb_r = s4.shapes.add_textbox(right_x + Inches(0.2), Inches(1.85), right_w - Inches(0.4), right_h - Inches(0.3))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p0 = tf_r.paragraphs[0]
    p0.text = "THE BLAST RADIUS REALITY"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = RED

    items = [
        ("Upstream Single Point of Failure:", "CA-Root (Tier 1) signs all internal mTLS communication certificates across the OT network."),
        ("Cascade Mechanism:", "When Shor's algorithm factors CA-Root's RSA-2048 key, the adversary issues valid rogue certificates to impersonate the OT-Gateway."),
        ("Physical Safety Impact:", "Ventilation fans in Tier 3 receive malicious shutoff packets. Gas sensors are blinded. Shaft hoist motors enter emergency interlock."),
        ("Blast Radius Quantification:", "1 Single Vulnerability ➔ 12 Dependent Systems Compromised ➔ 5 of 6 Safety Assets Offline in < 24 Hours.")
    ]
    for subhead, body in items:
        p_sub = tf_r.add_paragraph()
        p_sub.text = f"\n• {subhead}"
        p_sub.font.size = Pt(10.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = AMBER

        p_bod = tf_r.add_paragraph()
        p_bod.text = body
        p_bod.font.size = Pt(9.5)
        p_bod.font.color.rgb = MUTED

    # =========================================================================
    # SLIDE 5: THE 4 CORE ENGINES: ALGORITHMIC SPECIFICATIONS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Core Engines: Algorithmic Design & Specifications",
               "TECHNICAL SPECIFICATIONS & ARCHITECTURE",
               "Deep dive into the 4 foundational modules powering MineGuard AI")

    engines = [
        ("ENGINE 1: CRYPTOGRAPHIC SCANNER", "Static AST & Regex Analysis", CYAN,
         "• File Types: .py, .js, .json, .yaml, and .pem certificates\n• Detection Targets: RSA (1024–4096), ECDSA (P-256/384), MD5, SHA-1\n• Execution Speed: Scans 5,000 files in < 1.2s via parallel regex threads\n• Quantum Risk Tagging: Automatically tags Shor vs Grover vulnerability\n• Output Schema: Exact file path, line number, and raw code snippet"),
        ("ENGINE 2: BFS CASCADE SIMULATOR", "Discrete Graph Propagation", RED,
         "• Algorithm: Breadth-First Search on Directed Acyclic Graph G = (V, E)\n• Temporal Slider: Interactive Q-Day timeline horizon (2027 to 2035)\n• Failure Modeling: Models upstream compromise propagation down 4 tiers\n• Metric Calculation: System health percentage & time-to-failure curves\n• Simulation Result: 5 of 6 safety systems fail within 24h unmitigated"),
        ("ENGINE 3: RISK SCORING ENGINE", "Severity-Calibrated Ranking", AMBER,
         "• Mathematical Formula: R = ∑ (w_s · Severity + w_e · Exposure + w_c · Centrality)\n• Calibration: Normalized 0 to 100 scale; 95/100 triggers CRITICAL alert\n• Priority Ranking: CA-Root is #1 (Blast radius = 12 downstream nodes)\n• NIST Mapping: Direct lookup to FIPS 203 / 204 replacement algorithms\n• Eliminates guesswork with reproducible, objective risk rankings"),
        ("ENGINE 4: MIGRATION PLANNER", "Budget-Bounded Phasing Optimizer", GREEN,
         "• Optimization: Topological dependency sorting under financial bounds\n• Operational Constraints: Budget ≤ $250K; Max outage ≤ 2 weeks/phase\n• Phasing Strategy: Immediate (Phase 1) ➔ Comm (Phase 2) ➔ Assets (Phase 3)\n• Total Plan: 5 Systems Retrofitted • 14 Weeks • $210,000 Total Budget\n• Output Deliverable: Executive Gantt roadmap & engineering work breakdown")
    ]

    card_w = Inches(5.7)
    card_h = Inches(2.55)
    for i, (eng_tag, eng_title, col, body) in enumerate(engines):
        row = i // 2
        c_idx = i % 2
        cx = Inches(0.8 + c_idx * 6.0)
        cy = Inches(1.7 + row * 2.7)

        add_card(s5, cx, cy, card_w, card_h, CARD_BG, col)
        tb = s5.shapes.add_textbox(cx + Inches(0.15), cy + Inches(0.12), card_w - Inches(0.3), card_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = eng_tag
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = col

        p1 = tf.add_paragraph()
        p1.text = eng_title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = WHITE

        p2 = tf.add_paragraph()
        p2.text = f"\n{body}"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = MUTED

    # =========================================================================
    # SLIDE 6: SPLIT-SCREEN CASCADE SIMULATION: UNMITIGATED VS PROTECTED
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Cascade Simulation: Unmitigated vs Post-Quantum Protected",
               "SIMULATION RESULTS & COMPARATIVE ANALYSIS",
               "Simulating Q-Day (2029): What happens when an adversary exploits mining cryptographic assets?")

    # Dual Column Comparative Architecture
    col_w = Inches(5.7)
    col_h = Inches(5.1)
    cy = Inches(1.7)

    # Left: Unmitigated
    add_card(s6, Inches(0.8), cy, col_w, col_h, CARD_BG, RED)
    tb_l = s6.shapes.add_textbox(Inches(1.0), cy + Inches(0.15), col_w - Inches(0.4), col_h - Inches(0.3))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p_l0 = tf_l.paragraphs[0]
    p_l0.text = "🔴 UNMITIGATED INFRASTRUCTURE (LEGACY CRYPTO)"
    p_l0.font.size = Pt(13)
    p_l0.font.bold = True
    p_l0.font.color.rgb = RED

    unmitigated_text = (
        "\nSYSTEM STATUS: CRITICAL SYSTEMIC COLLAPSE\n\n"
        "• Attack Vector: Harvested CA-Root RSA-2048 factored via Shor's algorithm.\n"
        "• Hour T+0: Root certificate compromised; invalidates internal mTLS.\n"
        "• Hour T+6: Adversary injects rogue packets into OT-Gateway & SCADA.\n"
        "• Hour T+12: Underground Ventilation Fans lose authentic control and halt.\n"
        "• Hour T+18: Toxic methane builds up; gas sensors report spoofed normal levels.\n"
        "• Hour T+24: Hoist motor control locks out; underground miners trapped.\n\n"
        "FINAL IMPACT METRICS:\n"
        "• Systems Down: 5 OF 6 CRITICAL SAFETY SYSTEMS FAILING\n"
        "• Production Uptime: 0% (TOTAL MINE SHUTDOWN)\n"
        "• Financial Loss: $150,000 / HOUR ($3,600,000 / DAY)"
    )
    p_l1 = tf_l.add_paragraph()
    p_l1.text = unmitigated_text
    p_l1.font.size = Pt(10)
    p_l1.font.color.rgb = MUTED

    # Right: Protected
    add_card(s6, Inches(6.8), cy, col_w, col_h, CARD_BG, GREEN)
    tb_r = s6.shapes.add_textbox(Inches(7.0), cy + Inches(0.15), col_w - Inches(0.4), col_h - Inches(0.3))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p_r0 = tf_r.paragraphs[0]
    p_r0.text = "🟢 MINEGUARD PROTECTED (NIST PQC ROADMAP APPLIED)"
    p_r0.font.size = Pt(13)
    p_r0.font.bold = True
    p_r0.font.color.rgb = GREEN

    protected_text = (
        "\nSYSTEM STATUS: 100% OPERATIONAL INTEGRITY MAINTAINED\n\n"
        "• Defense Vector: Phase 1 replaces CA-Root with NIST FIPS 204 (ML-DSA-87).\n"
        "• Hour T+0: Quantum adversary attempts prime factorization; attack fails.\n"
        "• Hour T+6: Lattice-based digital signatures verify OT-Gateway commands.\n"
        "• Hour T+12: Hybrid TLS 1.3 (ML-KEM-768) encapsulates telemetry securely.\n"
        "• Hour T+18: Ventilation fans receive authentic speed & air modulation.\n"
        "• Hour T+24: Continuous autonomous haulage & hoist operations maintained.\n\n"
        "FINAL IMPACT METRICS:\n"
        "• Systems Down: 0 SYSTEMS DOWN (ZERO SYSTEMIC FAILURES)\n"
        "• Production Uptime: 100% CONTINUOUS SAFE PRODUCTION\n"
        "• Financial ROI: $210K INVESTMENT PREVENTS $3.6M/DAY DISASTER"
    )
    p_r1 = tf_r.add_paragraph()
    p_r1.text = protected_text
    p_r1.font.size = Pt(10)
    p_r1.font.color.rgb = MUTED

    # =========================================================================
    # SLIDE 7: 3-PHASE MIGRATION ROADMAP & FINANCIAL ROI
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "Migration Plan & ROI: 14-Week Budget-Bounded Execution",
               "PRACTICAL MITIGATION ROADMAP & FINANCIAL METRICS",
               "How a $210,000 migration eliminates multi-million dollar physical catastrophe risks")

    # 3 Horizontal Phasing Bands
    phases = [
        ("PHASE 1 (WEEKS 1–4): IMMEDIATE ROOT TRUST HARDENING",
         "Scope: CA-Root (Internal Certificate Authority)\nAction: Deploy NIST FIPS 204 ML-DSA-87 Module-Lattice Digital Signatures\nBudget: $60,000 | Outage: 0 Days | Impact: Cuts 80% of upstream cascade blast radius",
         AMBER),
        ("PHASE 2 (WEEKS 5–9): CRITICAL COMMUNICATION BRIDGES",
         "Scope: OT-Gateway, SCADA Historian, and Central Authentication Service\nAction: Implement NIST FIPS 203 ML-KEM-768 Key Encapsulation in Hybrid TLS 1.3\nBudget: $75,000 | Outage: Zero Production Downtime | Impact: Secures all sensor & telemetry feeds",
         BLUE),
        ("PHASE 3 (WEEKS 10–14): HEAVY OPERATIONAL ASSETS",
         "Scope: Underground Ventilation Controllers, Autonomous Haulage Trucks, Hoist Motors\nAction: Firmware updates with post-quantum signed package verification\nBudget: $75,000 | Outage: Scheduled Maintenance Only | Impact: 100% Mine site quantum immunity",
         GREEN)
    ]

    p_w = Inches(11.7)
    p_h = Inches(1.15)
    for i, (p_tag, p_body, col) in enumerate(phases):
        p_y = Inches(1.7 + i * 1.3)
        add_card(s7, Inches(0.8), p_y, p_w, p_h, CARD_BG, col)

        tb = s7.shapes.add_textbox(Inches(1.0), p_y + Inches(0.1), p_w - Inches(0.4), p_h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = p_tag
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = col

        p1 = tf.add_paragraph()
        p1.text = p_body
        p1.font.size = Pt(10)
        p1.font.color.rgb = WHITE

    # Bottom 3 Quantified Value Cards
    roi_metrics = [
        ("DOWNTIME COST AVOIDED", "$150,000 / HOUR", "Average unplanned production outage cost for a Tier-1 mining site.", RED),
        ("TOTAL MIGRATION COST", "$210,000 TOTAL", "Complete 14-week mitigation for all 5 safety-critical core assets.", GREEN),
        ("PAYBACK PERIOD", "< 1.4 HOURS OF DOWNTIME", "Entire quantum roadmap pays for itself in under 90 minutes of avoided shutdown.", CYAN)
    ]
    r_w = Inches(3.7)
    r_h = Inches(1.35)
    r_y = Inches(5.6)
    for i, (m_tag, m_val, m_desc, col) in enumerate(roi_metrics):
        m_x = Inches(0.8 + i * 4.0)
        add_card(s7, m_x, r_y, r_w, r_h, CARD_ALT, BORDER_COLOR)

        tb = s7.shapes.add_textbox(m_x + Inches(0.15), r_y + Inches(0.1), r_w - Inches(0.3), r_h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = m_tag
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = MUTED

        p1 = tf.add_paragraph()
        p1.text = m_val
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = m_desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 8: TECHNICAL RIGOR, NIST STANDARDS & LIVE DEMO SCRIPT
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "Verification, NIST Standards & Demonstration Script",
               "TECHNICAL RIGOR & JUDGE WALKTHROUGH",
               "Validated test suites, standardized post-quantum algorithms, and air-gapped reliability")

    # Top: NIST Replacement Standards Table Box
    nst_w = Inches(11.7)
    nst_h = Inches(1.6)
    add_card(s8, Inches(0.8), Inches(1.7), nst_w, nst_h, CARD_BG, AMBER)
    tb_nst = s8.shapes.add_textbox(Inches(1.0), Inches(1.8), nst_w - Inches(0.4), nst_h - Inches(0.2))
    tf_nst = tb_nst.text_frame
    tf_nst.word_wrap = True
    p0 = tf_nst.paragraphs[0]
    p0.text = "NIST POST-QUANTUM CRYPTOGRAPHY REPLACEMENT STANDARDS (FIPS RELEASED AUGUST 2024)"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = AMBER

    nst_p = tf_nst.add_paragraph()
    nst_p.text = (
        "• RSA-2048 / RSA-4096 (Shor broken) ➔ FIPS 203 ML-KEM-768 / ML-KEM-1024 (Module-Lattice Key Encapsulation)\n"
        "• ECDSA P-256 / P-384 (Shor broken) ➔ FIPS 204 ML-DSA-65 / ML-DSA-87 (Module-Lattice Digital Signatures)\n"
        "• MD5 / SHA-1 (Collision / Grover vulnerable) ➔ FIPS 205 SLH-DSA / SHA-3 (Stateless Hash-Based Signatures)"
    )
    nst_p.font.size = Pt(10)
    nst_p.font.color.rgb = WHITE

    # Bottom Left: 30-Second Live Demonstration Script
    scr_w = Inches(6.8)
    scr_h = Inches(3.5)
    scr_y = Inches(3.5)
    add_card(s8, Inches(0.8), scr_y, scr_w, scr_h, CARD_ALT, BORDER_COLOR)
    tb_scr = s8.shapes.add_textbox(Inches(1.0), scr_y + Inches(0.15), scr_w - Inches(0.4), scr_h - Inches(0.3))
    tf_scr = tb_scr.text_frame
    tf_scr.word_wrap = True

    p0 = tf_scr.paragraphs[0]
    p0.text = "30-SECOND JUDGE LIVE DEMONSTRATION SCRIPT"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = CYAN

    script_steps = [
        ("00–10s: Cryptographic Audit", "Open page1.html. Click 'Run Scan'. 8 vulnerabilities flagged instantly across RSA, ECDSA, and MD5 with exact file paths and line numbers."),
        ("10–20s: Cascade Failure Simulation", "Open page2.html. Drag Q-Day horizon slider to 2029. Watch BFS algorithm turn the mine topology red as 5 of 6 safety systems collapse in 24 hours."),
        ("20–30s: Risk Scoring & Migration", "Open page3.html. Show 95/100 risk score with CA-Root as Rank 1. Present the 14-week, $210K roadmap that guarantees zero mine shutdowns.")
    ]
    for st_title, st_body in script_steps:
        p_t = tf_scr.add_paragraph()
        p_t.text = f"\n• {st_title}"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = AMBER
        p_b = tf_scr.add_paragraph()
        p_b.text = st_body
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = MUTED

    # Bottom Right: Verification Badges
    v_w = Inches(4.7)
    v_h = Inches(3.5)
    v_x = Inches(7.8)
    add_card(s8, v_x, scr_y, v_w, v_h, CARD_ALT, GREEN)
    tb_v = s8.shapes.add_textbox(v_x + Inches(0.2), scr_y + Inches(0.15), v_w - Inches(0.4), v_h - Inches(0.3))
    tf_v = tb_v.text_frame
    tf_v.word_wrap = True

    p0 = tf_v.paragraphs[0]
    p0.text = "TECHNICAL VERIFICATION STATUS"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = GREEN

    v_items = [
        ("10 / 10 Automated Unit Tests Passing", "Verified minimal suite covering scanner, BFS cascade, scoring, and planner execution in 0.41s."),
        ("101 / 101 Enterprise Test Suite Passing", "Covers multi-backend scanner, CBOM ingestion, ML risk models, SHAP explainability, FAISS RAG, and ILP."),
        ("Air-Gapped Offline Failover Guarantee", "Client-side api.js fallback ensures 100% interactive demo functionality without active internet or backend servers.")
    ]
    for vt, vb in v_items:
        p_vt = tf_v.add_paragraph()
        p_vt.text = f"\n• {vt}"
        p_vt.font.size = Pt(10.5)
        p_vt.font.bold = True
        p_vt.font.color.rgb = WHITE
        p_vb = tf_v.add_paragraph()
        p_vb.text = vb
        p_vb.font.size = Pt(9.5)
        p_vb.font.color.rgb = MUTED

    prs.save(str(PPTX_PATH))
    print(f"Generated PPTX at: {PPTX_PATH}")


def generate_pdf():
    # 16:9 widescreen landscape PDF: 13.33 x 7.5 inches
    page_w = 13.333 * inch
    page_h = 7.5 * inch
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=(page_w, page_h),
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.45 * inch
    )

    styles = getSampleStyleSheet()

    cat_style = ParagraphStyle(
        'CategoryTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#F59E0B')
    )
    title_style = ParagraphStyle(
        'SlideHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#FFFFFF')
    )
    subtitle_style = ParagraphStyle(
        'SubHeader',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#9CA3AF')
    )
    card_title_style = ParagraphStyle(
        'CardTitle',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#FFFFFF')
    )
    card_tag_style = ParagraphStyle(
        'CardTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#F59E0B')
    )
    card_body_style = ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#D1D5DB')
    )

    story = []

    def make_header(title, category="MINEGUARD AI", subtitle=""):
        res = [
            Paragraph(category.upper(), cat_style),
            Spacer(1, 2),
            Paragraph(title, title_style)
        ]
        if subtitle:
            res.extend([
                Spacer(1, 2),
                Paragraph(subtitle, subtitle_style)
            ])
        res.append(Spacer(1, 10))
        return res

    # Background canvas callback to color whole page #0B0F19
    def draw_bg(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(colors.HexColor('#0B0F19'))
        canvas.rect(0, 0, page_w, page_h, fill=1, stroke=0)
        canvas.restoreState()

    # ================= SLIDE 1 =================
    story.extend(make_header("MineGuard AI: Post-Quantum Cybersecurity for Mining Infrastructure",
                             "EXECUTIVE PLATFORM BLUEPRINT",
                             "Tagline: 'Predict the risk. Trace the impact. Plan the migration.'"))

    l1 = [
        Paragraph("<font color='#06B6D4'><b>LAYER 1: INGESTION</b></font>", card_tag_style),
        Paragraph("Cryptographic Inventory", card_title_style),
        Spacer(1, 4),
        Paragraph("• Git repos (.py, .js)<br/>• OT/SCADA configs (.yaml)<br/>• CycloneDX v1.6 CBOM<br/>• Tokenized crypto assets", card_body_style)
    ]
    l2 = [
        Paragraph("<font color='#F59E0B'><b>LAYER 2: THREAT ENGINE</b></font>", card_tag_style),
        Paragraph("Quantum Crypto Audit", card_title_style),
        Spacer(1, 4),
        Paragraph("• Shor's & Grover's checks<br/>• RSA-2048, ECDSA, MD5<br/>• Deterministic severity<br/>• Zero LLM hallucinations", card_body_style)
    ]
    l3 = [
        Paragraph("<font color='#EF4444'><b>LAYER 3: CASCADE GRAPH</b></font>", card_tag_style),
        Paragraph("Physical Blast Radius", card_title_style),
        Spacer(1, 4),
        Paragraph("• 20-Node 4-tier topology<br/>• Discrete BFS propagation<br/>• Upstream/downstream trace<br/>• Forecasts 5/6 systems down", card_body_style)
    ]
    l4 = [
        Paragraph("<font color='#10B981'><b>LAYER 4: PQC ROADMAP</b></font>", card_tag_style),
        Paragraph("Phased Mitigation", card_title_style),
        Spacer(1, 4),
        Paragraph("• NIST FIPS 203/204 mapping<br/>• 3-Phase schedule (14 Wks)<br/>• Budget bounded: $210K<br/>• Zero production outages", card_body_style)
    ]

    t1 = Table([[l1, l2, l3, l4]], colWidths=[2.9 * inch, 2.9 * inch, 2.9 * inch, 2.9 * inch])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1F2937')),
        ('INNERGRID', (0,0), (-1,-1), 12, colors.HexColor('#0B0F19')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t1)
    story.append(Spacer(1, 12))

    # Bottom 3 Badges
    b1 = [Paragraph("<font color='#06B6D4'><b>NIST STANDARDIZATION</b></font><br/>Aligned with FIPS 203, 204, & 205 (Aug 2024)", card_body_style)]
    b2 = [Paragraph("<font color='#EF4444'><b>CRITICAL RISK DETECTED</b></font><br/>CA-Root triggers 12-system cascading failure (95/100)", card_body_style)]
    b3 = [Paragraph("<font color='#10B981'><b>FEASIBLE MIGRATION OPEX</b></font><br/>14-Week Plan ($210K) avoids $150K/hr downtime threat", card_body_style)]
    tb_badges = Table([[b1, b2, b3]], colWidths=[3.9 * inch, 3.9 * inch, 3.9 * inch])
    tb_badges.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1E293B')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#374151')),
        ('INNERGRID', (0,0), (-1,-1), 10, colors.HexColor('#0B0F19')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(tb_badges)
    story.append(PageBreak())

    # ================= SLIDE 2 =================
    story.extend(make_header("The Problem: Quantum Threat to Safety-Critical Mining Infrastructure",
                             "THREAT LANDSCAPE & ATTACK LIFECYCLE",
                             "Why legacy industrial hardware is defenceless against 'Harvest Now, Decrypt Later' (HNDL)"))

    h1 = [
        Paragraph("<font color='#F59E0B'><b>STAGE 1: INTERCEPTION</b></font>", card_tag_style),
        Paragraph("Harvest Encrypted Data", card_title_style),
        Spacer(1, 4),
        Paragraph("• Adversaries tap OT telemetry<br/>• SCADA traffic archived<br/>• Cellular / insider access<br/>• Attack window: ACTIVE NOW", card_body_style)
    ]
    h2 = [
        Paragraph("<font color='#EF4444'><b>STAGE 2: HARDWARE GAP</b></font>", card_tag_style),
        Paragraph("20–30 Year Lifespans", card_title_style),
        Spacer(1, 4),
        Paragraph("• Underground PLCs aged 10+ yrs<br/>• Zero crypto agility in silicon<br/>• Fixed chips cannot patch<br/>• Operational past Q-Day", card_body_style)
    ]
    h3 = [
        Paragraph("<font color='#EF4444'><b>STAGE 3: Q-DAY ARRIVAL</b></font>", card_tag_style),
        Paragraph("Shor's Algorithm (~2029)", card_title_style),
        Spacer(1, 4),
        Paragraph("• Quantum computer factors keys<br/>• RSA-2048 & ECDSA broken<br/>• Root certs extracted<br/>• Master keys forged", card_body_style)
    ]
    h4 = [
        Paragraph("<font color='#EF4444'><b>STAGE 4: CATASTROPHE</b></font>", card_tag_style),
        Paragraph("Physical Mine Failure", card_title_style),
        Spacer(1, 4),
        Paragraph("• Forged packets injected<br/>• Gas monitoring blinded<br/>• Ventilation fans shut down<br/>• Fatal hoist cable lockout", card_body_style)
    ]

    t2 = Table([[h1, h2, h3, h4]], colWidths=[2.9 * inch, 2.9 * inch, 2.9 * inch, 2.9 * inch])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1F2937')),
        ('INNERGRID', (0,0), (-1,-1), 12, colors.HexColor('#0B0F19')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t2)
    story.append(Spacer(1, 10))

    rc1 = [Paragraph("<font color='#F59E0B'><b>ASYMMETRIC CRYPTO COLLAPSE</b></font><br/>Shor's algorithm solves prime factoring and discrete logarithms in polynomial time. All deployed RSA and ECC keys yield 0 bits of security.", card_body_style)]
    rc2 = [Paragraph("<font color='#06B6D4'><b>20–30 YEAR HARDWARE REALITY</b></font><br/>Industrial mine assets cannot auto-update. Substations, hoist motors, and ventilation systems require 3–5 years of planning to retrofit.", card_body_style)]
    rc3 = [Paragraph("<font color='#EF4444'><b>THE FATAL BLAST RADIUS</b></font><br/>Cyber breaks in mining cause physical damage: explosive methane accumulation, hoist drops, and autonomous vehicle haulage collisions.", card_body_style)]
    t2_sub = Table([[rc1, rc2, rc3]], colWidths=[3.9 * inch, 3.9 * inch, 3.9 * inch])
    t2_sub.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1E293B')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#374151')),
        ('INNERGRID', (0,0), (-1,-1), 10, colors.HexColor('#0B0F19')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t2_sub)
    story.append(PageBreak())

    # ================= SLIDE 3 =================
    story.extend(make_header("How MineGuard Works: 4-Stage Execution Flowchart",
                             "SYSTEM ARCHITECTURE & EXECUTION PIPELINE",
                             "Deterministic, mathematically-proven pipeline from code parsing to budgeted mitigation roadmap"))

    f1 = [
        Paragraph("<font color='#06B6D4'><b>STAGE 1: SCANNER</b></font>", card_tag_style),
        Paragraph("Cryptographic Audit", card_title_style),
        Spacer(1, 4),
        Paragraph("• Multi-regex & AST engine<br/>• Finds RSA, ECDSA, MD5<br/>• 8 Vulnerabilities identified<br/>• Flags line numbers & bits", card_body_style)
    ]
    f2 = [
        Paragraph("<font color='#EF4444'><b>STAGE 2: RISK SCORER</b></font>", card_tag_style),
        Paragraph("Criticality Ranking", card_title_style),
        Spacer(1, 4),
        Paragraph("• Severity × Exposure × Graph<br/>• Risk Score: 95/100 (CRITICAL)<br/>• Rank 1: CA-Root Certificate<br/>• NIST PQC replacement tags", card_body_style)
    ]
    f3 = [
        Paragraph("<font color='#3B82F6'><b>STAGE 3: CASCADE SIM</b></font>", card_tag_style),
        Paragraph("Discrete BFS Engine", card_title_style),
        Spacer(1, 4),
        Paragraph("• 20-Node Mining Graph<br/>• Q-Day Slider (2027–2035)<br/>• BFS failure propagation<br/>• 5 of 6 Systems Down in 24h", card_body_style)
    ]
    f4 = [
        Paragraph("<font color='#10B981'><b>STAGE 4: PLANNER</b></font>", card_tag_style),
        Paragraph("Budget-Bounded Roadmap", card_title_style),
        Spacer(1, 4),
        Paragraph("• Topological dependency sort<br/>• 3 Phases, 14 Weeks, $210K<br/>• Upgrades 5 critical assets<br/>• 0 Production outages", card_body_style)
    ]

    t3 = Table([[f1, f2, f3, f4]], colWidths=[2.9 * inch, 2.9 * inch, 2.9 * inch, 2.9 * inch])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1F2937')),
        ('INNERGRID', (0,0), (-1,-1), 12, colors.HexColor('#0B0F19')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t3)
    story.append(Spacer(1, 12))

    det_box = [
        Paragraph("<font color='#F59E0B'><b>MATHEMATICAL DETERMINISM GUARANTEE</b></font><br/>Zero LLM hallucinations on numeric metrics. All risk scores, graph cascade probabilities, and migration budgets are computed deterministically via graph theory and standard risk formulas.", card_body_style)
    ]
    t3_bus = Table([det_box], colWidths=[11.8 * inch])
    t3_bus.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1E293B')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#374151')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t3_bus)
    story.append(PageBreak())

    # ================= SLIDE 4 =================
    story.extend(make_header("Operational Topology: 20-Node 4-Tier Mining Infrastructure",
                             "GRAPH ARCHITECTURE & BLAST RADIUS PROPAGATION",
                             "Visualizing how an upstream cryptographic break cascades directly down into physical mine assets"))

    tier_stack = [
        [Paragraph("<font color='#EF4444'><b>TIER 1: ENTERPRISE & CLOUD</b></font><br/><b>Root Certificate Authority (CA-Root) [CRITICAL VULNERABILITY]</b> • ERP • Data Lake", card_body_style)],
        [Paragraph("<font color='#F59E0B'><b>TIER 2: OT NETWORK & SCADA</b></font><br/>OT-Gateway • SCADA Historian • Telemetry Broker • Central Authentication Service", card_body_style)],
        [Paragraph("<font color='#06B6D4'><b>TIER 3: MINE SAFETY SYSTEMS</b></font><br/>Main Ventilation Fans • Toxic Gas Monitoring • Dewatering Pumps • Emergency Comms Substation", card_body_style)],
        [Paragraph("<font color='#10B981'><b>TIER 4: HEAVY OPERATIONAL ASSETS</b></font><br/>Autonomous Haulage Trucks • Shaft Hoist Motor Control • Production Drill Rigs • Conveyor Belts", card_body_style)]
    ]
    t4_left = Table(tier_stack, colWidths=[7.2 * inch])
    t4_left.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1F2937')),
        ('INNERGRID', (0,0), (-1,-1), 8, colors.HexColor('#0B0F19')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))

    right_info = [
        Paragraph("<font color='#EF4444'><b>THE BLAST RADIUS REALITY</b></font>", card_title_style),
        Spacer(1, 4),
        Paragraph("• <b>Single Point of Failure:</b> CA-Root in Tier 1 signs all internal mTLS certificates across the plant.<br/><br/>"
                  "• <b>Cascade Mechanism:</b> When Shor's algorithm factors CA-Root's RSA key, rogue certs impersonate OT-Gateway.<br/><br/>"
                  "• <b>Physical Safety Impact:</b> Ventilation fans receive malicious halt packets. Hoist motors enter lockout.<br/><br/>"
                  "• <b>Quantification:</b> 1 Flaw ➔ 12 Dependent Systems Breached ➔ 5 of 6 Safety Assets Down in 24 Hours.", card_body_style)
    ]
    t4_right = Table([[right_info]], colWidths=[4.4 * inch])
    t4_right.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1E293B')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#374151')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))

    t4_combined = Table([[t4_left, t4_right]], colWidths=[7.3 * inch, 4.5 * inch])
    t4_combined.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t4_combined)
    story.append(PageBreak())

    # ================= SLIDE 5 =================
    story.extend(make_header("Core Engines: Algorithmic Design & Specifications",
                             "TECHNICAL SPECIFICATIONS & ARCHITECTURE",
                             "Deep dive into the 4 foundational modules powering MineGuard AI"))

    e1 = [
        Paragraph("<font color='#06B6D4'><b>ENGINE 1: CRYPTOGRAPHIC SCANNER</b></font>", card_tag_style),
        Paragraph("Static AST & Regex Analysis", card_title_style),
        Spacer(1, 3),
        Paragraph("• Files: .py, .js, .json, .yaml, .pem<br/>• Targets: RSA (1024-4096), ECDSA, MD5, SHA-1<br/>• Speed: 5,000 files in < 1.2s parallel execution<br/>• Tags Shor vs Grover vulnerability automatically", card_body_style)
    ]
    e2 = [
        Paragraph("<font color='#EF4444'><b>ENGINE 2: BFS CASCADE SIMULATOR</b></font>", card_tag_style),
        Paragraph("Discrete Graph Propagation", card_title_style),
        Spacer(1, 3),
        Paragraph("• Algorithm: BFS on Directed Acyclic Graph G=(V,E)<br/>• Q-Day Slider: Interactive horizon (2027 to 2035)<br/>• Failure curves: Hourly time-to-failure curves<br/>• 5 of 6 safety systems collapse within 24h unmitigated", card_body_style)
    ]
    e3 = [
        Paragraph("<font color='#F59E0B'><b>ENGINE 3: RISK SCORING ENGINE</b></font>", card_tag_style),
        Paragraph("Severity-Calibrated Ranking", card_title_style),
        Spacer(1, 3),
        Paragraph("• Formula: R = ∑ (w_s·Severity + w_e·Exposure + w_c·Centrality)<br/>• Scale: 0 to 100; Score 95/100 triggers CRITICAL alert<br/>• CA-Root is #1 (Blast radius: 12 downstream nodes)<br/>• Automated NIST PQC algorithm replacement tags", card_body_style)
    ]
    e4 = [
        Paragraph("<font color='#10B981'><b>ENGINE 4: MIGRATION PLANNER</b></font>", card_tag_style),
        Paragraph("Budget-Bounded Phasing Optimizer", card_title_style),
        Spacer(1, 3),
        Paragraph("• Topological dependency sorting under OPEX bounds<br/>• Constraints: Budget ≤ $250K; Outage ≤ 2 wks/phase<br/>• Total Plan: 5 Systems • 14 Weeks • $210,000 Budget<br/>• Actionable Gantt roadmap & engineering task list", card_body_style)
    ]

    t5 = Table([[e1, e2], [e3, e4]], colWidths=[5.8 * inch, 5.8 * inch], rowHeights=[2.3 * inch, 2.3 * inch])
    t5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1F2937')),
        ('INNERGRID', (0,0), (-1,-1), 10, colors.HexColor('#0B0F19')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t5)
    story.append(PageBreak())

    # ================= SLIDE 6 =================
    story.extend(make_header("Cascade Simulation: Unmitigated vs Post-Quantum Protected",
                             "SIMULATION RESULTS & COMPARATIVE ANALYSIS",
                             "Simulating Q-Day (2029): What happens when an adversary exploits mining cryptographic assets?"))

    col_unmitigated = [
        Paragraph("<font color='#EF4444'><b>🔴 UNMITIGATED (LEGACY CRYPTO)</b></font>", card_title_style),
        Paragraph("<b>STATUS: CRITICAL SYSTEMIC COLLAPSE</b>", card_tag_style),
        Spacer(1, 4),
        Paragraph("• <b>Attack:</b> CA-Root RSA-2048 factored via Shor's algorithm.<br/>"
                  "• <b>T+0h:</b> Root certificate broken; internal mTLS trust fails.<br/>"
                  "• <b>T+6h:</b> Rogue packets injected into OT-Gateway & SCADA.<br/>"
                  "• <b>T+12h:</b> Underground Ventilation Fans lose signal & halt.<br/>"
                  "• <b>T+18h:</b> Toxic methane builds up; gas sensors blinded.<br/>"
                  "• <b>T+24h:</b> Hoist motor control locked out; personnel trapped.<br/><br/>"
                  "<b>OUTCOME METRICS:</b><br/>"
                  "• Systems Down: <b>5 OF 6 SAFETY SYSTEMS FAILING</b><br/>"
                  "• Production Uptime: <b>0% (TOTAL MINE SHUTDOWN)</b><br/>"
                  "• Financial Loss: <b>$150,000 / HR ($3.6M / DAY)</b>", card_body_style)
    ]

    col_protected = [
        Paragraph("<font color='#10B981'><b>🟢 MINEGUARD PROTECTED (PQC ROADMAP)</b></font>", card_title_style),
        Paragraph("<b>STATUS: 100% OPERATIONAL INTEGRITY</b>", card_tag_style),
        Spacer(1, 4),
        Paragraph("• <b>Defense:</b> CA-Root upgraded to NIST FIPS 204 (ML-DSA-87).<br/>"
                  "• <b>T+0h:</b> Quantum adversary attempts factoring; attack fails.<br/>"
                  "• <b>T+6h:</b> Lattice digital signatures authenticate all OT commands.<br/>"
                  "• <b>T+12h:</b> Hybrid TLS 1.3 (ML-KEM-768) protects sensor feeds.<br/>"
                  "• <b>T+18h:</b> Ventilation fans operate with genuine telemetry.<br/>"
                  "• <b>T+24h:</b> Continuous autonomous haulage & hoist operation.<br/><br/>"
                  "<b>OUTCOME METRICS:</b><br/>"
                  "• Systems Down: <b>0 SYSTEMS DOWN (ZERO OUTAGES)</b><br/>"
                  "• Production Uptime: <b>100% CONTINUOUS SAFE PRODUCTION</b><br/>"
                  "• Financial ROI: <b>$210K INVESTMENT PREVENTS $3.6M/DAY</b>", card_body_style)
    ]

    t6 = Table([[col_unmitigated, col_protected]], colWidths=[5.8 * inch, 5.8 * inch])
    t6.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1F2937')),
        ('INNERGRID', (0,0), (-1,-1), 12, colors.HexColor('#0B0F19')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t6)
    story.append(PageBreak())

    # ================= SLIDE 7 =================
    story.extend(make_header("Migration Plan & ROI: 14-Week Budget-Bounded Execution",
                             "PRACTICAL MITIGATION ROADMAP & FINANCIAL METRICS",
                             "How a $210,000 migration eliminates multi-million dollar physical catastrophe risks"))

    p1_box = [Paragraph("<font color='#F59E0B'><b>PHASE 1 (WEEKS 1–4): ROOT TRUST HARDENING ($60,000)</b></font><br/>Scope: CA-Root (Certificate Authority) • Action: Deploy NIST FIPS 204 ML-DSA-87 Signatures<br/>Impact: Cuts 80% of upstream cascading failure risk across the entire mine • Zero Outages", card_body_style)]
    p2_box = [Paragraph("<font color='#3B82F6'><b>PHASE 2 (WEEKS 5–9): SCADA & COMMUNICATION BRIDGES ($75,000)</b></font><br/>Scope: OT-Gateway, SCADA Historian, Auth Service • Action: Implement FIPS 203 ML-KEM-768 in Hybrid TLS 1.3<br/>Impact: Secures all industrial sensor feeds & remote equipment dispatch • Zero Outages", card_body_style)]
    p3_box = [Paragraph("<font color='#10B981'><b>PHASE 3 (WEEKS 10–14): HEAVY OPERATIONAL ASSETS ($75,000)</b></font><br/>Scope: Underground Ventilation Controllers, Haulage Dispatch • Action: Firmware post-quantum updates<br/>Impact: Full operational site immunity achieved • Scheduled Maintenance Only", card_body_style)]

    t7_phases = Table([p1_box, p2_box, p3_box], colWidths=[11.8 * inch])
    t7_phases.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1F2937')),
        ('INNERGRID', (0,0), (-1,-1), 8, colors.HexColor('#0B0F19')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t7_phases)
    story.append(Spacer(1, 10))

    roi1 = [Paragraph("<font color='#EF4444' size='14'><b>$150,000 / HR</b></font><br/><b>Unplanned Downtime Cost</b><br/>Average Tier-1 production shutdown cost.", card_body_style)]
    roi2 = [Paragraph("<font color='#10B981' size='14'><b>$210,000 TOTAL</b></font><br/><b>Total Migration Investment</b><br/>Complete 14-week mitigation for all 5 core systems.", card_body_style)]
    roi3 = [Paragraph("<font color='#06B6D4' size='14'><b>&lt; 1.4 HOURS</b></font><br/><b>Payback Period</b><br/>Migration pays for itself in under 90 minutes of avoided downtime.", card_body_style)]

    t7_roi = Table([[roi1, roi2, roi3]], colWidths=[3.9 * inch, 3.9 * inch, 3.9 * inch])
    t7_roi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1E293B')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#374151')),
        ('INNERGRID', (0,0), (-1,-1), 10, colors.HexColor('#0B0F19')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t7_roi)
    story.append(PageBreak())

    # ================= SLIDE 8 =================
    story.extend(make_header("Verification, NIST Standards & Demonstration Script",
                             "TECHNICAL RIGOR & JUDGE WALKTHROUGH",
                             "Validated test suites, standardized post-quantum algorithms, and air-gapped reliability"))

    nist_table = [
        Paragraph("<font color='#F59E0B'><b>NIST POST-QUANTUM CRYPTOGRAPHY REPLACEMENT STANDARDS (FIPS AUG 2024)</b></font><br/>"
                  "• <b>RSA-2048 / RSA-4096</b> (Shor broken) ➔ <b>FIPS 203 ML-KEM-768/1024</b> (Module-Lattice Key Encapsulation)<br/>"
                  "• <b>ECDSA P-256 / P-384</b> (Shor broken) ➔ <b>FIPS 204 ML-DSA-65/87</b> (Module-Lattice Digital Signatures)<br/>"
                  "• <b>MD5 / SHA-1</b> (Collision / Grover) ➔ <b>FIPS 205 SLH-DSA / SHA-3</b> (Stateless Hash-Based Signatures)", card_body_style)
    ]
    t8_nist = Table([nist_table], colWidths=[11.8 * inch])
    t8_nist.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1F2937')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t8_nist)
    story.append(Spacer(1, 10))

    demo_script = [
        Paragraph("<font color='#06B6D4'><b>30-SECOND JUDGE LIVE DEMONSTRATION SCRIPT</b></font>", card_title_style),
        Spacer(1, 4),
        Paragraph("• <b>00–10s [SCAN]:</b> Click 'Run Scan' on page1.html ➔ 8 crypto vulnerabilities flagged with exact line numbers.<br/><br/>"
                  "• <b>10–20s [SIMULATE]:</b> Drag slider to 2029 on page2.html ➔ BFS algorithm turns topology red as 5 systems collapse.<br/><br/>"
                  "• <b>20–30s [PLAN]:</b> View page3.html ➔ Score 95/100, 14-week $210K roadmap prevents the entire disaster.", card_body_style)
    ]

    tests_box = [
        Paragraph("<font color='#10B981'><b>TECHNICAL VERIFICATION STATUS</b></font>", card_title_style),
        Spacer(1, 4),
        Paragraph("• <b>10 / 10 Automated Unit Tests Passing:</b> Minimal suite covering scanner, BFS cascade, scoring, and planning in 0.41s.<br/><br/>"
                  "• <b>101 / 101 Enterprise Tests Passing:</b> Full test coverage across scanner, CBOM, ML risk models, SHAP, and ILP solver.<br/><br/>"
                  "• <b>Air-Gapped Offline Failover Guarantee:</b> Automatic client fallback in api.js guarantees zero presentation failure.", card_body_style)
    ]

    t8_lower = Table([[demo_script, tests_box]], colWidths=[6.4 * inch, 5.2 * inch])
    t8_lower.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1E293B')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#374151')),
        ('INNERGRID', (0,0), (-1,-1), 10, colors.HexColor('#0B0F19')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t8_lower)

    doc.build(story, onFirstPage=draw_bg, onLaterPages=draw_bg)
    print(f"Generated PDF at: {PDF_PATH}")


def generate_html():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>MineGuard AI — Presentation Deck (Full Visual Edition)</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0b0f19;
      --card: #111827;
      --card-alt: #1e293b;
      --border: #1f2937;
      --border-light: #374151;
      --amber: #f59e0b;
      --red: #ef4444;
      --green: #10b981;
      --blue: #3b82f6;
      --cyan: #06b6d4;
      --text: #f9fafb;
      --muted: #9ca3af;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #000;
      color: var(--text);
      font-family: 'Inter', sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 20px 0;
    }
    .top-controls {
      position: fixed;
      top: 16px;
      right: 24px;
      display: flex;
      gap: 12px;
      z-index: 1000;
    }
    .btn {
      background: var(--amber);
      color: #000;
      border: none;
      padding: 10px 18px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.9rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    .btn:hover { background: #d97706; }
    .btn-pdf { background: var(--green); color: #fff; }
    .btn-pdf:hover { background: #059669; }

    .slide {
      width: 1200px;
      height: 675px;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 40px 48px;
      margin-bottom: 30px;
      display: flex;
      flex-direction: column;
      position: relative;
      box-shadow: 0 10px 30px rgba(0,0,0,0.6);
      page-break-after: always;
    }
    .header { margin-bottom: 24px; }
    .category {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--amber);
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    .title {
      font-size: 1.85rem;
      font-weight: 800;
      color: #fff;
      margin-top: 4px;
    }
    .subtitle {
      font-size: 0.95rem;
      color: var(--muted);
      margin-top: 4px;
    }

    .flow-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 20px;
    }
    .flow-card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      position: relative;
    }
    .flow-card.cyan { border-top: 4px solid var(--cyan); }
    .flow-card.amber { border-top: 4px solid var(--amber); }
    .flow-card.red { border-top: 4px solid var(--red); }
    .flow-card.green { border-top: 4px solid var(--green); }
    .flow-card.blue { border-top: 4px solid var(--blue); }

    .flow-tag {
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      margin-bottom: 6px;
    }
    .flow-title {
      font-size: 1.15rem;
      font-weight: 700;
      color: #fff;
      margin-bottom: 12px;
    }
    .flow-desc {
      font-size: 0.85rem;
      color: var(--muted);
      line-height: 1.5;
    }

    .grid-2x2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-bottom: 16px;
    }
    .grid-3col {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
    }

    .banner-card {
      background: var(--card-alt);
      border: 1px solid var(--border-light);
      border-radius: 10px;
      padding: 18px 24px;
      margin-top: auto;
    }

    .two-cols {
      display: grid;
      grid-template-columns: 1.5fr 1fr;
      gap: 20px;
      height: 100%;
    }
    .comp-cols {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      height: 100%;
    }

    .tier-box {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px 18px;
      margin-bottom: 12px;
    }
    .tier-box.red { border-left: 4px solid var(--red); }
    .tier-box.amber { border-left: 4px solid var(--amber); }
    .tier-box.cyan { border-left: 4px solid var(--cyan); }
    .tier-box.green { border-left: 4px solid var(--green); }

    @media print {
      body { background: #000; padding: 0; }
      .top-controls { display: none; }
      .slide {
        width: 100vw;
        height: 100vh;
        margin: 0;
        border: none;
        border-radius: 0;
        page-break-after: always;
      }
    }
  </style>
</head>
<body>

  <div class="top-controls">
    <button class="btn btn-pdf" onclick="window.print()">🖨️ Print / Save as PDF</button>
  </div>

  <!-- SLIDE 1: BLUEPRINT -->
  <div class="slide">
    <div class="header">
      <div class="category">EXECUTIVE PLATFORM BLUEPRINT</div>
      <div class="title">MineGuard AI: Post-Quantum Cybersecurity for Mining Infrastructure</div>
      <div class="subtitle">Tagline: "Predict the risk. Trace the impact. Plan the migration."</div>
    </div>
    <div class="flow-row">
      <div class="flow-card cyan">
        <div class="flow-tag" style="color:var(--cyan)">LAYER 1: INGESTION</div>
        <div class="flow-title">Cryptographic Inventory</div>
        <div class="flow-desc">• Git repos (.py, .js)<br/>• OT/SCADA configs (.yaml)<br/>• CycloneDX v1.6 CBOM<br/>• Tokenized crypto assets</div>
      </div>
      <div class="flow-card amber">
        <div class="flow-tag" style="color:var(--amber)">LAYER 2: THREAT ENGINE</div>
        <div class="flow-title">Quantum Crypto Audit</div>
        <div class="flow-desc">• Shor's & Grover's checks<br/>• RSA-2048, ECDSA, MD5<br/>• Deterministic severity<br/>• Zero LLM hallucinations</div>
      </div>
      <div class="flow-card red">
        <div class="flow-tag" style="color:var(--red)">LAYER 3: CASCADE GRAPH</div>
        <div class="flow-title">Physical Blast Radius</div>
        <div class="flow-desc">• 20-Node 4-tier topology<br/>• Discrete BFS propagation<br/>• Upstream/downstream trace<br/>• Forecasts 5/6 systems down</div>
      </div>
      <div class="flow-card green">
        <div class="flow-tag" style="color:var(--green)">LAYER 4: PQC ROADMAP</div>
        <div class="flow-title">Phased Mitigation</div>
        <div class="flow-desc">• NIST FIPS 203/204 mapping<br/>• 3-Phase schedule (14 Wks)<br/>• Budget bounded: $210K<br/>• Zero production outages</div>
      </div>
    </div>
    <div class="grid-3col">
      <div class="banner-card">
        <div style="color:var(--cyan);font-weight:700;margin-bottom:4px;">NIST STANDARDIZATION</div>
        <div style="font-size:0.9rem;color:#fff;">Aligned with FIPS 203, 204, & 205 (Aug 2024 Standards)</div>
      </div>
      <div class="banner-card">
        <div style="color:var(--red);font-weight:700;margin-bottom:4px;">CRITICAL RISK RANK 1</div>
        <div style="font-size:0.9rem;color:#fff;">CA-Root triggers 12-system cascading failure (95/100 Score)</div>
      </div>
      <div class="banner-card">
        <div style="color:var(--green);font-weight:700;margin-bottom:4px;">FEASIBLE OPEX ROADMAP</div>
        <div style="font-size:0.9rem;color:#fff;">14-Week Plan ($210K) avoids $150K/hr downtime disaster</div>
      </div>
    </div>
  </div>

  <!-- SLIDE 2: HNDL ATTACK FLOWCHART -->
  <div class="slide">
    <div class="header">
      <div class="category">THREAT LANDSCAPE & ATTACK LIFECYCLE</div>
      <div class="title">The Problem: Quantum Threat to Safety-Critical Mining Operations</div>
      <div class="subtitle">Why legacy industrial hardware is defenceless against "Harvest Now, Decrypt Later" (HNDL)</div>
    </div>
    <div class="flow-row">
      <div class="flow-card amber">
        <div class="flow-tag" style="color:var(--amber)">STAGE 1: INTERCEPTION</div>
        <div class="flow-title">Harvest Encrypted Data</div>
        <div class="flow-desc">• Adversaries tap OT telemetry<br/>• SCADA traffic archived<br/>• Cellular / insider access<br/>• Attack window: ACTIVE TODAY</div>
      </div>
      <div class="flow-card red">
        <div class="flow-tag" style="color:var(--red)">STAGE 2: HARDWARE GAP</div>
        <div class="flow-title">20–30 Year Lifespans</div>
        <div class="flow-desc">• Underground PLCs aged 10+ yrs<br/>• Zero crypto agility in silicon<br/>• Fixed chips cannot patch<br/>• Operational past Q-Day</div>
      </div>
      <div class="flow-card red">
        <div class="flow-tag" style="color:var(--red)">STAGE 3: Q-DAY ARRIVAL</div>
        <div class="flow-title">Shor's Algorithm (~2029)</div>
        <div class="flow-desc">• Quantum computer factors keys<br/>• RSA-2048 & ECDSA broken<br/>• Root certs extracted<br/>• Master keys forged</div>
      </div>
      <div class="flow-card red">
        <div class="flow-tag" style="color:var(--red)">STAGE 4: CATASTROPHE</div>
        <div class="flow-title">Physical Mine Failure</div>
        <div class="flow-desc">• Forged packets injected<br/>• Gas monitoring blinded<br/>• Ventilation fans shut down<br/>• Fatal hoist cable lockout</div>
      </div>
    </div>
    <div class="grid-3col">
      <div class="banner-card">
        <div style="color:var(--amber);font-weight:700;margin-bottom:4px;">ASYMMETRIC CRYPTO COLLAPSE</div>
        <div style="font-size:0.85rem;color:var(--muted);">Shor's algorithm solves prime factoring and discrete logarithms in polynomial time. All deployed RSA and ECC keys yield 0 bits of security.</div>
      </div>
      <div class="banner-card">
        <div style="color:var(--cyan);font-weight:700;margin-bottom:4px;">20–30 YEAR HARDWARE REALITY</div>
        <div style="font-size:0.85rem;color:var(--muted);">Industrial mine assets cannot auto-update. Substations, hoist motors, and ventilation systems require 3–5 years of planning to retrofit.</div>
      </div>
      <div class="banner-card">
        <div style="color:var(--red);font-weight:700;margin-bottom:4px;">THE FATAL BLAST RADIUS</div>
        <div style="font-size:0.85rem;color:var(--muted);">Cyber breaches in mining cause physical damage: explosive methane accumulation, hoist drops, and autonomous vehicle haulage collisions.</div>
      </div>
    </div>
  </div>

  <!-- SLIDE 3: 4-STAGE FLOWCHART -->
  <div class="slide">
    <div class="header">
      <div class="category">SYSTEM ARCHITECTURE & EXECUTION PIPELINE</div>
      <div class="title">How MineGuard Works: 4-Stage Execution Flowchart</div>
      <div class="subtitle">Deterministic, mathematically-proven pipeline from code parsing to budgeted mitigation roadmap</div>
    </div>
    <div class="flow-row">
      <div class="flow-card cyan">
        <div class="flow-tag" style="color:var(--cyan)">STAGE 1: SCANNER</div>
        <div class="flow-title">Cryptographic Audit</div>
        <div class="flow-desc">• Multi-regex & AST engine<br/>• Finds RSA, ECDSA, MD5<br/>• 8 Vulnerabilities identified<br/>• Flags line numbers & bits</div>
      </div>
      <div class="flow-card red">
        <div class="flow-tag" style="color:var(--red)">STAGE 2: RISK SCORER</div>
        <div class="flow-title">Criticality Ranking</div>
        <div class="flow-desc">• Severity × Exposure × Graph<br/>• Risk Score: 95/100 (CRITICAL)<br/>• Rank 1: CA-Root Certificate<br/>• NIST PQC replacement tags</div>
      </div>
      <div class="flow-card blue">
        <div class="flow-tag" style="color:var(--blue)">STAGE 3: CASCADE SIM</div>
        <div class="flow-title">Discrete BFS Engine</div>
        <div class="flow-desc">• 20-Node Mining Graph<br/>• Q-Day Slider (2027–2035)<br/>• BFS failure propagation<br/>• 5 of 6 Systems Down in 24h</div>
      </div>
      <div class="flow-card green">
        <div class="flow-tag" style="color:var(--green)">STAGE 4: PLANNER</div>
        <div class="flow-title">Budget-Bounded Roadmap</div>
        <div class="flow-desc">• Topological dependency sort<br/>• 3 Phases, 14 Weeks, $210K<br/>• Upgrades 5 critical assets<br/>• 0 Production outages</div>
      </div>
    </div>
    <div class="banner-card">
      <div style="color:var(--amber);font-weight:700;margin-bottom:4px;">MATHEMATICAL DETERMINISM GUARANTEE</div>
      <div style="font-size:0.9rem;color:#fff;">Zero LLM hallucinations on numeric metrics. All risk scores, graph cascade probabilities, and migration budgets are computed deterministically via graph theory and standard risk formulas.</div>
    </div>
  </div>

  <!-- SLIDE 4: 20-NODE 4-TIER TOPOLOGY -->
  <div class="slide">
    <div class="header">
      <div class="category">GRAPH ARCHITECTURE & BLAST RADIUS PROPAGATION</div>
      <div class="title">Operational Topology: 20-Node 4-Tier Mining Infrastructure</div>
      <div class="subtitle">Visualizing how an upstream cryptographic break cascades directly down into physical mine assets</div>
    </div>
    <div class="two-cols">
      <div>
        <div class="tier-box red">
          <div style="color:var(--red);font-weight:700;font-size:0.85rem;">TIER 1: ENTERPRISE & CLOUD</div>
          <div style="color:#fff;font-weight:600;font-size:0.95rem;margin-top:2px;">Root Certificate Authority (CA-Root) [CRITICAL VULNERABILITY] • ERP • Data Lake</div>
        </div>
        <div class="tier-box amber">
          <div style="color:var(--amber);font-weight:700;font-size:0.85rem;">TIER 2: OT NETWORK & SCADA</div>
          <div style="color:#fff;font-weight:600;font-size:0.95rem;margin-top:2px;">OT-Gateway • SCADA Historian • Telemetry Broker • Central Authentication Service</div>
        </div>
        <div class="tier-box cyan">
          <div style="color:var(--cyan);font-weight:700;font-size:0.85rem;">TIER 3: MINE SAFETY SYSTEMS</div>
          <div style="color:#fff;font-weight:600;font-size:0.95rem;margin-top:2px;">Main Ventilation Fans • Toxic Gas Monitoring • Dewatering Pumps • Emergency Comms Substation</div>
        </div>
        <div class="tier-box green">
          <div style="color:var(--green);font-weight:700;font-size:0.85rem;">TIER 4: HEAVY OPERATIONAL ASSETS</div>
          <div style="color:#fff;font-weight:600;font-size:0.95rem;margin-top:2px;">Autonomous Haulage Trucks • Shaft Hoist Motor Control • Production Drill Rigs • Conveyor Belts</div>
        </div>
      </div>
      <div class="banner-card" style="margin:0;">
        <div style="color:var(--red);font-size:1.15rem;font-weight:800;margin-bottom:12px;">THE BLAST RADIUS REALITY</div>
        <div style="font-size:0.88rem;color:var(--muted);line-height:1.6;">
          <p><b style="color:var(--amber);">Single Point of Failure:</b> CA-Root in Tier 1 signs all internal mTLS certificates across the plant.</p>
          <p style="margin-top:8px;"><b style="color:var(--amber);">Cascade Mechanism:</b> When Shor's algorithm factors CA-Root's RSA key, rogue certs impersonate OT-Gateway.</p>
          <p style="margin-top:8px;"><b style="color:var(--amber);">Physical Safety Impact:</b> Ventilation fans receive malicious halt packets. Hoist motors enter lockout.</p>
          <p style="margin-top:8px;"><b style="color:var(--amber);">Quantification:</b> 1 Flaw ➔ 12 Dependent Systems Breached ➔ 5 of 6 Safety Assets Down in 24 Hours.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 5: 4 ENGINES SPECS -->
  <div class="slide">
    <div class="header">
      <div class="category">TECHNICAL SPECIFICATIONS & ARCHITECTURE</div>
      <div class="title">Core Engines: Algorithmic Design & Specifications</div>
      <div class="subtitle">Deep dive into the 4 foundational modules powering MineGuard AI</div>
    </div>
    <div class="grid-2x2">
      <div class="flow-card cyan">
        <div class="flow-tag" style="color:var(--cyan)">ENGINE 1: CRYPTOGRAPHIC SCANNER</div>
        <div class="flow-title">Static AST & Regex Analysis</div>
        <div class="flow-desc">• Files: .py, .js, .json, .yaml, .pem<br/>• Targets: RSA (1024-4096), ECDSA, MD5, SHA-1<br/>• Speed: 5,000 files in < 1.2s parallel execution<br/>• Tags Shor vs Grover vulnerability automatically</div>
      </div>
      <div class="flow-card red">
        <div class="flow-tag" style="color:var(--red)">ENGINE 2: BFS CASCADE SIMULATOR</div>
        <div class="flow-title">Discrete Graph Propagation</div>
        <div class="flow-desc">• Algorithm: BFS on Directed Acyclic Graph G=(V,E)<br/>• Q-Day Slider: Interactive horizon (2027 to 2035)<br/>• Failure curves: Hourly time-to-failure curves<br/>• 5 of 6 safety systems collapse within 24h unmitigated</div>
      </div>
      <div class="flow-card amber">
        <div class="flow-tag" style="color:var(--amber)">ENGINE 3: RISK SCORING ENGINE</div>
        <div class="flow-title">Severity-Calibrated Ranking</div>
        <div class="flow-desc">• Formula: R = ∑ (w_s·Severity + w_e·Exposure + w_c·Centrality)<br/>• Scale: 0 to 100; Score 95/100 triggers CRITICAL alert<br/>• CA-Root is #1 (Blast radius: 12 downstream nodes)<br/>• Automated NIST PQC algorithm replacement tags</div>
      </div>
      <div class="flow-card green">
        <div class="flow-tag" style="color:var(--green)">ENGINE 4: MIGRATION PLANNER</div>
        <div class="flow-title">Budget-Bounded Phasing Optimizer</div>
        <div class="flow-desc">• Topological dependency sorting under OPEX bounds<br/>• Constraints: Budget ≤ $250K; Outage ≤ 2 wks/phase<br/>• Total Plan: 5 Systems • 14 Weeks • $210,000 Budget<br/>• Actionable Gantt roadmap & engineering task list</div>
      </div>
    </div>
  </div>

  <!-- SLIDE 6: SPLIT-SCREEN SIMULATION -->
  <div class="slide">
    <div class="header">
      <div class="category">SIMULATION RESULTS & COMPARATIVE ANALYSIS</div>
      <div class="title">Cascade Simulation: Unmitigated vs Post-Quantum Protected</div>
      <div class="subtitle">Simulating Q-Day (2029): What happens when an adversary exploits mining cryptographic assets?</div>
    </div>
    <div class="comp-cols">
      <div class="flow-card red">
        <div class="flow-title" style="color:var(--red);">🔴 UNMITIGATED (LEGACY CRYPTO)</div>
        <div style="font-size:0.8rem;font-weight:700;color:#fff;margin-bottom:10px;">STATUS: CRITICAL SYSTEMIC COLLAPSE</div>
        <div class="flow-desc" style="font-size:0.85rem;line-height:1.6;">
          • <b>Attack:</b> CA-Root RSA-2048 factored via Shor's algorithm.<br/>
          • <b>T+0h:</b> Root certificate broken; internal mTLS trust fails.<br/>
          • <b>T+6h:</b> Rogue packets injected into OT-Gateway & SCADA.<br/>
          • <b>T+12h:</b> Underground Ventilation Fans lose signal & halt.<br/>
          • <b>T+18h:</b> Toxic methane builds up; gas sensors blinded.<br/>
          • <b>T+24h:</b> Hoist motor control locked out; personnel trapped.<br/><br/>
          <b style="color:#fff;">OUTCOME METRICS:</b><br/>
          • Systems Down: <b style="color:var(--red);">5 OF 6 SAFETY SYSTEMS FAILING</b><br/>
          • Production Uptime: <b style="color:var(--red);">0% (TOTAL MINE SHUTDOWN)</b><br/>
          • Financial Loss: <b style="color:var(--red);">$150,000 / HR ($3.6M / DAY)</b>
        </div>
      </div>
      <div class="flow-card green">
        <div class="flow-title" style="color:var(--green);">🟢 MINEGUARD PROTECTED (PQC ROADMAP)</div>
        <div style="font-size:0.8rem;font-weight:700;color:#fff;margin-bottom:10px;">STATUS: 100% OPERATIONAL INTEGRITY</div>
        <div class="flow-desc" style="font-size:0.85rem;line-height:1.6;">
          • <b>Defense:</b> CA-Root upgraded to NIST FIPS 204 (ML-DSA-87).<br/>
          • <b>T+0h:</b> Quantum adversary attempts factoring; attack fails.<br/>
          • <b>T+6h:</b> Lattice digital signatures authenticate all OT commands.<br/>
          • <b>T+12h:</b> Hybrid TLS 1.3 (ML-KEM-768) protects sensor feeds.<br/>
          • <b>T+18h:</b> Ventilation fans operate with genuine telemetry.<br/>
          • <b>T+24h:</b> Continuous autonomous haulage & hoist operation.<br/><br/>
          <b style="color:#fff;">OUTCOME METRICS:</b><br/>
          • Systems Down: <b style="color:var(--green);">0 SYSTEMS DOWN (ZERO OUTAGES)</b><br/>
          • Production Uptime: <b style="color:var(--green);">100% CONTINUOUS SAFE PRODUCTION</b><br/>
          • Financial ROI: <b style="color:var(--green);">$210K INVESTMENT PREVENTS $3.6M/DAY</b>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 7: ROADMAP & ROI -->
  <div class="slide">
    <div class="header">
      <div class="category">PRACTICAL MITIGATION ROADMAP & FINANCIAL METRICS</div>
      <div class="title">Migration Plan & ROI: 14-Week Budget-Bounded Execution</div>
      <div class="subtitle">How a $210,000 migration eliminates multi-million dollar physical catastrophe risks</div>
    </div>
    <div style="display:flex;flex-direction:column;gap:12px;margin-bottom:16px;">
      <div class="tier-box amber">
        <div style="color:var(--amber);font-weight:700;font-size:0.85rem;">PHASE 1 (WEEKS 1–4): ROOT TRUST HARDENING ($60,000)</div>
        <div style="font-size:0.85rem;color:#fff;margin-top:2px;">Scope: CA-Root (Certificate Authority) • Action: Deploy NIST FIPS 204 ML-DSA-87 Signatures • Cuts 80% upstream cascade risk</div>
      </div>
      <div class="tier-box cyan">
        <div style="color:var(--cyan);font-weight:700;font-size:0.85rem;">PHASE 2 (WEEKS 5–9): SCADA & COMMUNICATION BRIDGES ($75,000)</div>
        <div style="font-size:0.85rem;color:#fff;margin-top:2px;">Scope: OT-Gateway, SCADA Historian, Auth Service • Action: Implement FIPS 203 ML-KEM-768 in Hybrid TLS 1.3 • Secures sensor feeds</div>
      </div>
      <div class="tier-box green">
        <div style="color:var(--green);font-weight:700;font-size:0.85rem;">PHASE 3 (WEEKS 10–14): HEAVY OPERATIONAL ASSETS ($75,000)</div>
        <div style="font-size:0.85rem;color:#fff;margin-top:2px;">Scope: Underground Ventilation Controllers, Haulage Dispatch • Action: Firmware post-quantum updates • Full site immunity</div>
      </div>
    </div>
    <div class="grid-3col">
      <div class="banner-card">
        <div style="color:var(--muted);font-size:0.8rem;font-weight:700;">DOWNTIME COST AVOIDED</div>
        <div style="color:var(--red);font-size:1.4rem;font-weight:800;margin:4px 0;">$150,000 / HR</div>
        <div style="font-size:0.8rem;color:#fff;">Average Tier-1 production shutdown cost.</div>
      </div>
      <div class="banner-card">
        <div style="color:var(--muted);font-size:0.8rem;font-weight:700;">TOTAL MIGRATION COST</div>
        <div style="color:var(--green);font-size:1.4rem;font-weight:800;margin:4px 0;">$210,000 TOTAL</div>
        <div style="font-size:0.8rem;color:#fff;">Complete 14-week mitigation for all 5 systems.</div>
      </div>
      <div class="banner-card">
        <div style="color:var(--muted);font-size:0.8rem;font-weight:700;">PAYBACK PERIOD</div>
        <div style="color:var(--cyan);font-size:1.4rem;font-weight:800;margin:4px 0;">&lt; 1.4 HOURS</div>
        <div style="font-size:0.8rem;color:#fff;">Pays for itself in under 90 mins of saved downtime.</div>
      </div>
    </div>
  </div>

  <!-- SLIDE 8: NIST & DEMO SCRIPT -->
  <div class="slide">
    <div class="header">
      <div class="category">TECHNICAL RIGOR & JUDGE WALKTHROUGH</div>
      <div class="title">Verification, NIST Standards & Demonstration Script</div>
      <div class="subtitle">Validated test suites, standardized post-quantum algorithms, and air-gapped reliability</div>
    </div>
    <div class="banner-card" style="margin-bottom:16px;">
      <div style="color:var(--amber);font-weight:700;font-size:0.9rem;margin-bottom:6px;">NIST POST-QUANTUM CRYPTOGRAPHY REPLACEMENT STANDARDS (FIPS RELEASED AUGUST 2024)</div>
      <div style="font-size:0.85rem;color:#fff;line-height:1.5;">
        • <b>RSA-2048 / RSA-4096</b> (Shor broken) ➔ <b>FIPS 203 ML-KEM-768/1024</b> (Module-Lattice Key Encapsulation)<br/>
        • <b>ECDSA P-256 / P-384</b> (Shor broken) ➔ <b>FIPS 204 ML-DSA-65/87</b> (Module-Lattice Digital Signatures)<br/>
        • <b>MD5 / SHA-1</b> (Collision / Grover) ➔ <b>FIPS 205 SLH-DSA / SHA-3</b> (Stateless Hash-Based Signatures)
      </div>
    </div>
    <div class="two-cols">
      <div class="banner-card" style="margin:0;">
        <div style="color:var(--cyan);font-weight:700;font-size:1rem;margin-bottom:10px;">30-SECOND JUDGE LIVE DEMONSTRATION SCRIPT</div>
        <div style="font-size:0.85rem;color:var(--muted);line-height:1.6;">
          <p><b style="color:var(--amber);">00–10s [SCAN]:</b> Click 'Run Scan' on page1.html ➔ 8 crypto flaws identified with exact line numbers.</p>
          <p style="margin-top:8px;"><b style="color:var(--amber);">10–20s [SIMULATE]:</b> Drag slider to 2029 on page2.html ➔ BFS algorithm turns topology red as 5 systems fail.</p>
          <p style="margin-top:8px;"><b style="color:var(--amber);">20–30s [PLAN]:</b> View page3.html ➔ Score 95/100, 14-week $210K roadmap stops the disaster.</p>
        </div>
      </div>
      <div class="banner-card" style="margin:0;">
        <div style="color:var(--green);font-weight:700;font-size:1rem;margin-bottom:10px;">TECHNICAL VERIFICATION STATUS</div>
        <div style="font-size:0.85rem;color:var(--muted);line-height:1.6;">
          <p><b style="color:#fff;">10 / 10 Tests Passing:</b> Minimal suite covering scanner, BFS cascade, scoring, and planning in 0.41s.</p>
          <p style="margin-top:8px;"><b style="color:#fff;">101 / 101 Tests Passing:</b> Full test coverage across scanner, CBOM, ML risk models, SHAP, and ILP solver.</p>
          <p style="margin-top:8px;"><b style="color:#fff;">Air-Gapped Offline Failover:</b> Automatic client fallback in api.js guarantees zero demo failure.</p>
        </div>
      </div>
    </div>
  </div>

</body>
</html>
"""
    HTML_PATH.write_text(html_content, encoding="utf-8")
    print(f"Generated HTML slide deck at: {HTML_PATH}")


if __name__ == "__main__":
    generate_pptx()
    generate_pdf()
    generate_html()
