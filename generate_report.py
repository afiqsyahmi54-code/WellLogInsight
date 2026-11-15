"""
generate_report.py
Run this script to generate a PDF interview preparation report:
    python generate_report.py
"""

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
import os

OUTPUT = "WellLog_Insight_Project_Report.pdf"

BLUE   = "#003366"
LBLUE  = "#0066CC"
GREY   = "#F5F5F5"
DKGREY = "#333333"
ACCENT = "#FF6B35"
WHITE  = "#FFFFFF"


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def new_page(pdf, title=None):
    fig = plt.figure(figsize=(8.27, 11.69))   # A4 portrait
    fig.patch.set_facecolor(WHITE)
    if title:
        # Header bar
        bar = fig.add_axes([0, 0.94, 1, 0.06])
        bar.set_facecolor(BLUE)
        bar.axis("off")
        bar.text(0.5, 0.5, title, color=WHITE, fontsize=14,
                 fontweight="bold", ha="center", va="center", transform=bar.transAxes)
        # Footer
        foot = fig.add_axes([0, 0, 1, 0.025])
        foot.set_facecolor(BLUE)
        foot.axis("off")
        foot.text(0.5, 0.5,
                  f"WellLog Insight  |  FYP II  |  {datetime.now().strftime('%B %Y')}",
                  color=WHITE, fontsize=8, ha="center", va="center",
                  transform=foot.transAxes)
    return fig


def txt(fig, x, y, s, size=10, color=DKGREY, bold=False, italic=False, ha="left"):
    style = "italic" if italic else "normal"
    weight = "bold" if bold else "normal"
    fig.text(x, y, s, fontsize=size, color=color,
             fontstyle=style, fontweight=weight, ha=ha, wrap=True)


def section(fig, y, label):
    fig.text(0.07, y, label, fontsize=11, color=BLUE,
             fontweight="bold")
    ax = fig.add_axes([0.07, y - 0.005, 0.86, 0.003])
    ax.set_facecolor(LBLUE)
    ax.axis("off")


def bullet(fig, x, y, text, size=9.5, color=DKGREY):
    fig.text(x, y, "•  " + text, fontsize=size, color=color, wrap=True)


def box(fig, x, y, w, h, fc=GREY, ec=LBLUE, lw=1):
    ax = fig.add_axes([x, y, w, h])
    ax.set_facecolor(fc)
    for sp in ax.spines.values():
        sp.set_color(ec)
        sp.set_linewidth(lw)
    ax.set_xticks([])
    ax.set_yticks([])
    return ax


def save(fig, pdf):
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 — COVER
# ─────────────────────────────────────────────────────────────────────────────

def page_cover(pdf):
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.patch.set_facecolor(BLUE)

    # Title block
    fig.text(0.5, 0.72, "WellLog Insight",
             fontsize=36, color=WHITE, fontweight="bold", ha="center")
    fig.text(0.5, 0.65, "Petrophysical Well Log Analysis Application",
             fontsize=16, color="#AAD4FF", ha="center")

    # Divider
    ax_line = fig.add_axes([0.15, 0.62, 0.70, 0.003])
    ax_line.set_facecolor(ACCENT)
    ax_line.axis("off")

    fig.text(0.5, 0.56, "Final Year Project II  (FYP II)",
             fontsize=13, color="#CCDDFF", ha="center", style="italic")
    fig.text(0.5, 0.52, "Interview Preparation Report",
             fontsize=13, color="#CCDDFF", ha="center", style="italic")

    fig.text(0.5, 0.42, "Prepared by:",
             fontsize=11, color="#AABBCC", ha="center")
    fig.text(0.5, 0.38, "Afiq Syahmi",
             fontsize=18, color=WHITE, fontweight="bold", ha="center")

    fig.text(0.5, 0.30, datetime.now().strftime("%B %Y"),
             fontsize=12, color="#AABBCC", ha="center")

    # Tech stack badges
    techs = ["Python", "Kivy / KivyMD", "Matplotlib", "NumPy / Pandas", "LAS / lasio"]
    for i, t in enumerate(techs):
        bx = 0.08 + i * 0.168
        bax = fig.add_axes([bx, 0.17, 0.14, 0.04])
        bax.set_facecolor("#004488")
        for sp in bax.spines.values():
            sp.set_color(ACCENT)
            sp.set_linewidth(1.5)
        bax.axis("off")
        bax.text(0.5, 0.5, t, color=WHITE, fontsize=7.5,
                 ha="center", va="center", fontweight="bold",
                 transform=bax.transAxes)

    fig.text(0.5, 0.10,
             "This report covers project overview, technical architecture,\n"
             "petrophysical methods, AI module, challenges, and interview Q&A.",
             fontsize=10, color="#AABBCC", ha="center", linespacing=1.6)

    save(fig, pdf)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 — OVERVIEW & OBJECTIVES
# ─────────────────────────────────────────────────────────────────────────────

def page_overview(pdf):
    fig = new_page(pdf, "1.  Project Overview & Objectives")
    y = 0.88

    section(fig, y, "1.1  Background")
    y -= 0.07
    overview = (
        "Well log analysis (petrophysics) is a fundamental process in the oil and gas industry. "
        "Raw well log data recorded in LAS (Log ASCII Standard) format must be interpreted to "
        "identify reservoir zones, estimate porosity, shale volume, and water saturation. "
        "Traditionally this requires expensive desktop software (Petrel, IP, etc.)."
    )
    fig.text(0.07, y, overview, fontsize=9.5, color=DKGREY,
             wrap=True, linespacing=1.6, va="top",
             bbox=dict(boxstyle="round,pad=0.4", fc=GREY, ec=LBLUE, lw=0.8))

    y -= 0.14
    section(fig, y, "1.2  Problem Statement")
    y -= 0.07
    problems = [
        "Existing tools are expensive and require licenced desktop software.",
        "No lightweight, mobile-friendly petrophysical analysis tool exists.",
        "Engineers in the field cannot perform quick log interpretation without a full workstation.",
        "LAS file column naming varies widely between acquisition companies, making automated reading difficult.",
    ]
    for p in problems:
        bullet(fig, 0.09, y, p)
        y -= 0.045

    y -= 0.01
    section(fig, y, "1.3  Objectives")
    y -= 0.065
    objectives = [
        "Develop a cross-platform (Windows / Android) well log viewer that reads LAS files.",
        "Implement automated petrophysical calculations: Vshale, Porosity, and Water Saturation.",
        "Identify potential reservoir intervals automatically using Gamma Ray cut-off method.",
        "Provide an AI-powered curve recognition and data quality checking module.",
        "Export professional multi-track petrophysical reports as PDF.",
    ]
    for i, o in enumerate(objectives, 1):
        fig.text(0.09, y, f"{i}.  {o}", fontsize=9.5, color=DKGREY, linespacing=1.5)
        y -= 0.048

    y -= 0.01
    section(fig, y, "1.4  Scope")
    y -= 0.055
    scopes = [
        "Input: LAS 2.0 format well log files (ASCII).",
        "Curves supported: Gamma Ray (GR), Density (RHOB), Neutron (NPHI), Resistivity (RT).",
        "Platform: Windows desktop (primary); Android APK via Buildozer (secondary).",
        "Output: Interactive well log tracks + PDF petrophysical report.",
    ]
    for s in scopes:
        bullet(fig, 0.09, y, s)
        y -= 0.042

    save(fig, pdf)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 — TECHNOLOGY STACK
# ─────────────────────────────────────────────────────────────────────────────

def page_tech(pdf):
    fig = new_page(pdf, "2.  Technology Stack")

    headers = ["Category", "Technology", "Purpose"]
    rows = [
        ["UI Framework",        "Kivy 2.x + KivyMD",     "Cross-platform GUI (Material Design)"],
        ["Language",            "Python 3.10",            "Core application logic"],
        ["Plotting",            "Matplotlib",             "Well log track rendering"],
        ["Data Processing",     "NumPy + Pandas",         "Array math & DataFrame handling"],
        ["LAS File Reading",    "lasio",                  "Parse LAS 2.0 / 3.0 files"],
        ["PDF Export",          "Matplotlib PdfPages",    "Multi-page A4 PDF generation"],
        ["AI Module",           "Rule-based Python",      "Curve recognition & QC checks"],
        ["Build (Android)",     "Buildozer / python-for-android", "APK packaging"],
        ["CI/CD",               "GitHub Actions",         "Automated APK build workflow"],
        ["Version Control",     "Git / GitHub",           "Source management"],
    ]

    col_x  = [0.07, 0.30, 0.55]
    col_w  = [0.22, 0.24, 0.40]
    row_h  = 0.048
    start_y = 0.82

    # Header row
    hax = fig.add_axes([0.07, start_y, 0.86, row_h])
    hax.set_facecolor(BLUE)
    hax.axis("off")
    for j, (h, cx) in enumerate(zip(headers, col_x)):
        rel_x = (cx - 0.07) / 0.86
        hax.text(rel_x + 0.01, 0.5, h, color=WHITE, fontsize=9,
                 fontweight="bold", va="center", transform=hax.transAxes)

    for i, row in enumerate(rows):
        y = start_y - (i + 1) * row_h
        fc = GREY if i % 2 == 0 else WHITE
        rax = fig.add_axes([0.07, y, 0.86, row_h])
        rax.set_facecolor(fc)
        for sp in rax.spines.values():
            sp.set_color("#CCCCCC")
            sp.set_linewidth(0.5)
        rax.axis("off")
        for j, (cell, cx) in enumerate(zip(row, col_x)):
            rel_x = (cx - 0.07) / 0.86
            bold = j == 1
            rax.text(rel_x + 0.01, 0.5, cell,
                     fontsize=8.5, va="center",
                     fontweight="bold" if bold else "normal",
                     color=LBLUE if bold else DKGREY,
                     transform=rax.transAxes)

    y_after = start_y - len(rows) * row_h - 0.04
    section(fig, y_after, "Why Kivy / KivyMD?")
    y_after -= 0.055
    reasons = [
        "Single codebase runs on Windows, Linux, macOS, and Android — ideal for field engineers.",
        "KivyMD provides Material Design components (cards, buttons, spinners) out of the box.",
        "FigureCanvasKivyAgg bridges Matplotlib figures directly into Kivy widgets — no image export needed.",
        "Free and open-source; no licensing cost unlike commercial alternatives.",
    ]
    for r in reasons:
        bullet(fig, 0.09, y_after, r)
        y_after -= 0.042

    save(fig, pdf)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 4 — SYSTEM ARCHITECTURE
# ─────────────────────────────────────────────────────────────────────────────

def page_arch(pdf):
    fig = new_page(pdf, "3.  System Architecture")

    section(fig, 0.88, "3.1  Application Flow")

    # Flow diagram boxes
    flow = [
        (0.10, 0.74, "User\nUploads LAS"),
        (0.30, 0.74, "android_file_utils\nread_las_file()"),
        (0.52, 0.74, "DataFrame\n(Depth, GR, RHOB\nNPHI, RT)"),
        (0.74, 0.74, "Screen\nPlots Tracks"),
    ]
    for bx, by, label in flow:
        bax = fig.add_axes([bx, by, 0.16, 0.08])
        bax.set_facecolor(BLUE)
        bax.axis("off")
        bax.text(0.5, 0.5, label, color=WHITE, fontsize=8,
                 ha="center", va="center", fontweight="bold",
                 transform=bax.transAxes, linespacing=1.4)

    # Arrows
    for ax_x in [0.265, 0.475, 0.695]:
        arr = fig.add_axes([ax_x, 0.775, 0.04, 0.03])
        arr.axis("off")
        arr.annotate("", xy=(1, 0.5), xytext=(0, 0.5),
                     arrowprops=dict(arrowstyle="->", color=ACCENT, lw=2),
                     xycoords="axes fraction", textcoords="axes fraction")

    section(fig, 0.68, "3.2  Screen Structure (MVC)")

    screens = [
        ("StartScreen",           "Entry point, navigation hub"),
        ("WellLogScreen",         "LAS file upload, well metadata input"),
        ("ViewLogScreen",         "Raw log tracks: GR, Density/Neutron, Resistivity"),
        ("InterpretationScreen",  "Hub for analysis screens"),
        ("VshaleScreen",          "Shale volume calculation & visualisation"),
        ("PorosityScreen",        "Density-Neutron crossplot porosity"),
        ("WaterSaturationScreen", "Archie equation Sw + all tracks"),
        ("ReservoirScreen",       "Full petrophysical suite + interval detection"),
    ]

    y = 0.63
    for name, desc in screens:
        bax = box(fig, 0.07, y - 0.01, 0.30, 0.038, fc="#EEF4FF", ec=LBLUE)
        bax.text(0.5, 0.5, name, color=BLUE, fontsize=8.5,
                 fontweight="bold", ha="center", va="center",
                 transform=bax.transAxes)
        fig.text(0.40, y + 0.004, f"→  {desc}", fontsize=9, color=DKGREY)
        y -= 0.052

    section(fig, y - 0.005, "3.3  Utility Modules")
    y -= 0.055
    utils = [
        ("utils/android_file_utils.py", "Reads LAS files via lasio; fallback pure-Python parser for Android"),
        ("utils/plot_utils.py",         "create_consistent_plot(), create_depth_track() — shared by all screens"),
        ("utils/constants.py",          "COLORS dict — single source of truth for all plot colours"),
        ("ai_welllog.py",               "AICurveRecognizer + AIQualityChecker — standalone AI module"),
    ]
    for fname, desc in utils:
        fig.text(0.09, y, fname, fontsize=8.5, color=LBLUE, fontweight="bold")
        fig.text(0.09, y - 0.022, desc, fontsize=8.5, color=DKGREY)
        y -= 0.052

    save(fig, pdf)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 5 — PETROPHYSICAL METHODS
# ─────────────────────────────────────────────────────────────────────────────

def page_petro(pdf):
    fig = new_page(pdf, "4.  Petrophysical Methods Implemented")

    y = 0.88
    # --- GR / Vshale ---
    section(fig, y, "4.1  Gamma Ray & Shale Volume (Vshale)")
    y -= 0.07

    fig.text(0.07, y,
             "The Gamma Ray log measures natural radioactivity of the formation.\n"
             "High GR → shale (clay-rich).  Low GR → clean sand (potential reservoir).",
             fontsize=9.5, color=DKGREY, linespacing=1.6)
    y -= 0.07

    bax = box(fig, 0.07, y - 0.045, 0.86, 0.058, fc="#EEF4FF")
    bax.text(0.5, 0.65, "Vshale (Linear method):", color=BLUE, fontsize=9,
             fontweight="bold", ha="center", transform=bax.transAxes)
    bax.text(0.5, 0.25,
             "Vsh = (GR − GR_clean) / (GR_shale − GR_clean)",
             color=DKGREY, fontsize=10, ha="center",
             fontfamily="monospace", transform=bax.transAxes)

    y -= 0.065
    bullets_vsh = [
        "GR_clean  = 10th percentile of GR (cleanest sand)",
        "GR_shale  = 90th percentile of GR (purest shale)",
        "Result clipped to [0, 1];  × 100 to display as %",
        "Cut-off line = midpoint (GR_max − GR_min)/2 + GR_min  to highlight reservoir intervals",
    ]
    for b in bullets_vsh:
        bullet(fig, 0.09, y, b)
        y -= 0.038

    # --- Porosity ---
    y -= 0.01
    section(fig, y, "4.2  Porosity (Density-Neutron Crossplot)")
    y -= 0.065

    bax2 = box(fig, 0.07, y - 0.055, 0.86, 0.068, fc="#EEF4FF")
    bax2.text(0.5, 0.75, "Density Porosity:", color=BLUE, fontsize=9,
              fontweight="bold", ha="center", transform=bax2.transAxes)
    bax2.text(0.5, 0.48,
              "φ_D = (ρ_matrix − ρ_b) / (ρ_matrix − ρ_fluid)",
              color=DKGREY, fontsize=10, ha="center",
              fontfamily="monospace", transform=bax2.transAxes)
    bax2.text(0.5, 0.18,
              "φ_total = (φ_D + φ_N) / 2   [Density-Neutron average]",
              color=DKGREY, fontsize=9.5, ha="center",
              fontfamily="monospace", transform=bax2.transAxes)

    y -= 0.08
    bullets_phi = [
        "ρ_matrix = 2.65 g/cm³  (sandstone matrix)",
        "ρ_fluid  = 1.00 g/cm³  (fresh water)",
        "φ_N (Neutron) normalised to v/v if recorded as percentage (÷100)",
        "Result clipped to [0, 1];  displayed as %",
    ]
    for b in bullets_phi:
        bullet(fig, 0.09, y, b)
        y -= 0.038

    # --- Sw ---
    y -= 0.01
    section(fig, y, "4.3  Water Saturation — Archie's Equation")
    y -= 0.065

    bax3 = box(fig, 0.07, y - 0.055, 0.86, 0.068, fc="#EEF4FF")
    bax3.text(0.5, 0.75, "Archie (1942):", color=BLUE, fontsize=9,
              fontweight="bold", ha="center", transform=bax3.transAxes)
    bax3.text(0.5, 0.42,
              "Sw = ( a · Rw / (φ^m · Rt) )^(1/n)",
              color=DKGREY, fontsize=11, ha="center",
              fontfamily="monospace", transform=bax3.transAxes)
    bax3.text(0.5, 0.12,
              "a = 0.62  |  Rw = 0.1 Ω·m  |  m = 2.0  |  n = 2.0  (default, user-adjustable)",
              color=DKGREY, fontsize=8.5, ha="center", transform=bax3.transAxes)

    y -= 0.08
    bullets_sw = [
        "Sw < 50 %  →  Potential hydrocarbon zone  (green shade)",
        "50–90 %   →  Transition zone",
        "Sw > 90 %  →  Water-bearing zone",
        "m and n are adjustable via UI sliders; re-plot triggered without reloading data.",
    ]
    for b in bullets_sw:
        bullet(fig, 0.09, y, b)
        y -= 0.038

    save(fig, pdf)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 6 — RESERVOIR IDENTIFICATION & AI MODULE
# ─────────────────────────────────────────────────────────────────────────────

def page_reservoir_ai(pdf):
    fig = new_page(pdf, "5.  Reservoir Identification & AI Module")

    y = 0.88
    section(fig, y, "5.1  Automatic Reservoir Interval Detection")
    y -= 0.07

    steps = [
        ("Step 1", "Read Gamma Ray column from LAS file."),
        ("Step 2", "Compute cut-off = (GR_max − GR_min) / 2 + GR_min  (midpoint)."),
        ("Step 3", "Traverse depth rows; flag rows where GR < cut-off as 'in-zone'."),
        ("Step 4", "Record (top, bottom, min_GR, max_GR) for each continuous zone."),
        ("Step 5", "Shade detected intervals across ALL tracks (GR, RHOB/NPHI, RT, φ, Vsh, Sw)."),
        ("Step 6", "Display interval table in sidebar; include in PDF report."),
    ]
    for step, desc in steps:
        bax = box(fig, 0.07, y - 0.03, 0.14, 0.038, fc=BLUE)
        bax.text(0.5, 0.5, step, color=WHITE, fontsize=8,
                 fontweight="bold", ha="center", va="center",
                 transform=bax.transAxes)
        fig.text(0.23, y - 0.012, desc, fontsize=9, color=DKGREY)
        y -= 0.052

    y -= 0.01
    section(fig, y, "5.2  AI Module — ai_welllog.py")
    y -= 0.065

    fig.text(0.07, y,
             "An AI module was designed with two engines:",
             fontsize=9.5, color=DKGREY)
    y -= 0.045

    # AICurveRecognizer
    bax_cr = box(fig, 0.07, y - 0.085, 0.40, 0.095, fc="#EEF4FF")
    bax_cr.text(0.5, 0.88, "AICurveRecognizer", color=BLUE,
                fontsize=9, fontweight="bold", ha="center",
                transform=bax_cr.transAxes)
    for i, line in enumerate([
        "• Abbreviation map (GR → Gamma Ray)",
        "• Primary & secondary pattern matching",
        "• Unit extraction from mnemonic names",
        "• Confidence score 0–1 per curve",
    ]):
        bax_cr.text(0.05, 0.70 - i * 0.17, line, fontsize=7.5,
                    color=DKGREY, transform=bax_cr.transAxes)

    # AIQualityChecker
    bax_qc = box(fig, 0.53, y - 0.085, 0.40, 0.095, fc="#EEF4FF")
    bax_qc.text(0.5, 0.88, "AIQualityChecker", color=BLUE,
                fontsize=9, fontweight="bold", ha="center",
                transform=bax_qc.transAxes)
    for i, line in enumerate([
        "• Missing data detection (% per curve)",
        "• Depth reversal & gap detection",
        "• Statistical spike / outlier detection",
        "• Overall quality score 0–100 %",
    ]):
        bax_qc.text(0.05, 0.70 - i * 0.17, line, fontsize=7.5,
                    color=DKGREY, transform=bax_qc.transAxes)

    y -= 0.12
    fig.text(0.07, y,
             "Current status: Module is complete and tested but not yet integrated into the UI.\n"
             "Integration is planned as a future enhancement (quality report screen).",
             fontsize=9, color=ACCENT, linespacing=1.6,
             bbox=dict(boxstyle="round,pad=0.3", fc="#FFF5F0", ec=ACCENT, lw=1))

    y -= 0.09
    section(fig, y, "5.3  PDF Report Generation")
    y -= 0.055
    pdf_bullets = [
        "Title page (well name, location, depth range, timestamp).",
        "Data tracks grouped 3 per A4-landscape page — depth, GR, RHOB/NPHI, RT, φ, Vsh, Sw.",
        "Reservoir interval shading carried over into the PDF exactly as shown on screen.",
        "Final summary page: methodology, Archie parameters, net pay statistics, QC notes.",
        "Saved to user-selected folder via MDFileManager folder picker.",
    ]
    for b in pdf_bullets:
        bullet(fig, 0.09, y, b)
        y -= 0.042

    save(fig, pdf)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 7 — FEATURES BREAKDOWN
# ─────────────────────────────────────────────────────────────────────────────

def page_features(pdf):
    fig = new_page(pdf, "6.  Features Breakdown")

    features = [
        ("LAS File Loading",
         ["Reads LAS 2.0 via lasio library.",
          "Pure-Python fallback parser for Android (no lasio dependency).",
          "Auto-renames columns: GR→Gamma Ray, RHOB→Density, NPHI→Neutron, RES→Resistivity.",
          "Validates required columns before proceeding."]),
        ("Well Log Viewer",
         ["Three-track display: GR | Density–Neutron (twin axis) | Resistivity (log scale).",
          "Dynamic canvas height scales with depth range (2 px/m).",
          "Spinner + loading label shown while rendering to prevent UI freeze.",
          "Scrollable horizontal layout via ScrollView."]),
        ("Vshale Screen",
         ["GR track with cut-off dashed line and reservoir shading.",
          "Vshale (%) track with three cut-off reference lines (10 %, 30 %, 50 %).",
          "Depth track with 20 m tick markers."]),
        ("Porosity Screen",
         ["GR | Density-Neutron | Porosity (%) tracks.",
          "Porosity cut-off lines: good > 10 %, fair 5–10 %.",
          "Reservoir intervals shaded across all tracks."]),
        ("Water Saturation Screen",
         ["Full 5-track display: GR | RHOB-NPHI | RT | Sw.",
          "Hydrocarbon fill (green) where Sw < 50 %.",
          "Three Sw zone lines: 50 % (HC), 70 % (Transition), 90 % (Water)."]),
        ("Reservoir Screen",
         ["6-track suite: GR | RHOB-NPHI | RT | Porosity | Vshale | Sw.",
          "Adjustable Archie m and n parameters with live re-plot button.",
          "Detected interval list displayed in side panel.",
          "Water & pay indicator reference lines on resistivity track."]),
        ("PDF Export",
         ["Save button on any screen triggers folder picker.",
          "A4 portrait title page + A4 landscape track pages (3 tracks/page).",
          "Summary page with net pay statistics and methodology notes.",
          "Petrophysical parameters (m, n) printed on each page."]),
        ("Navigation",
         ["WellLogApp.change_screen() manages ScreenManager transitions.",
          "Back buttons on all analysis screens.",
          "File selection persists in app.selected_file across screen transitions."]),
    ]

    y = 0.87
    for title, pts in features:
        if y < 0.12:
            break
        section(fig, y, title)
        y -= 0.045
        for p in pts:
            bullet(fig, 0.09, y, p)
            y -= 0.036
        y -= 0.012

    save(fig, pdf)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 8 — CHALLENGES & SOLUTIONS
# ─────────────────────────────────────────────────────────────────────────────

def page_challenges(pdf):
    fig = new_page(pdf, "7.  Challenges & Solutions")

    challenges = [
        (
            "Cross-platform LAS Reading (Android)",
            "lasio cannot be compiled for Android via Buildozer due to C-extension dependencies.",
            "Implemented a pure-Python fallback LAS reader (read_las_pure_python) that parses the ASCII format "
            "without any external library. Detected at runtime: if lasio import fails, fallback is used automatically."
        ),
        (
            "Matplotlib inside Kivy",
            "Matplotlib figures run on a different render loop from Kivy's UI thread, causing UI freezes when "
            "plotting large datasets.",
            "Used Clock.schedule_once() to defer plotting by 0.1 s, allowing the loading spinner to render first. "
            "FigureCanvasKivyAgg wraps Matplotlib figures as Kivy widgets seamlessly."
        ),
        (
            "Dynamic Canvas Height",
            "Well logs with different depth ranges need different canvas heights to maintain consistent "
            "depth scale (pixels per metre).",
            "Computed canvas_height = depth_range × 2 px/m, clamped between 800 and 20 000 px. "
            "fig_height_inches derived from canvas_height / 100, clamped to [8, 100]."
        ),
        (
            "PDF Export — Axis Fidelity",
            "Matplotlib axes cannot be directly copied between figures. Early attempts produced blank or "
            "incorrectly-scaled tracks in the exported PDF.",
            "Extracted raw data from each original axis (get_lines(), get_collections()), re-plotted on new "
            "axes in the PDF figure with the same axis limits. Twin axes (RHOB-NPHI) handled with twinx()."
        ),
        (
            "Reservoir Re-interpretation Without Data Reload",
            "Changing Archie parameters required reloading the LAS file, which was slow.",
            "Stored self.df, self.cut_off, and self.intervals as instance variables in ReservoirScreen. "
            "reinterpret_with_new_parameters() re-draws plots using cached data — no file I/O."
        ),
        (
            "LAS Column Name Variability",
            "Different logging contractors use different mnemonics (e.g. GR, GAMMA, GR_CORR for Gamma Ray).",
            "Implemented pattern-based renaming in read_las_file() using .upper() substring matching. "
            "ai_welllog.AICurveRecognizer provides a more robust AI-based alternative."
        ),
        (
            "Keeping All Tracks Depth-Aligned",
            "Each track is an independent Matplotlib figure; mismatched ylim causes visual misalignment.",
            "Every plot sets ax.set_ylim(depth_max, depth_min) using the same depth_min/depth_max values "
            "from the DataFrame. Canvas height is identical across all tracks."
        ),
    ]

    y = 0.88
    for i, (title, problem, solution) in enumerate(challenges):
        if y < 0.09:
            break
        fig.text(0.07, y, f"{i+1}.  {title}", fontsize=10, color=BLUE, fontweight="bold")
        y -= 0.032
        fig.text(0.09, y, "Problem:", fontsize=8.5, color=ACCENT, fontweight="bold")
        fig.text(0.21, y, problem, fontsize=8.5, color=DKGREY, wrap=True)
        y -= 0.032
        fig.text(0.09, y, "Solution:", fontsize=8.5, color="#2E8B57", fontweight="bold")
        fig.text(0.21, y, solution, fontsize=8.5, color=DKGREY, wrap=True)
        y -= 0.052

    save(fig, pdf)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 9 — INTERVIEW Q&A
# ─────────────────────────────────────────────────────────────────────────────

def page_qa(pdf):
    fig = new_page(pdf, "8.  Likely Interview Questions & Model Answers")

    qas = [
        (
            "What does your app do, in one sentence?",
            "WellLog Insight reads LAS well log files and automatically calculates and visualises "
            "Vshale, porosity, and water saturation to identify potential reservoir zones — without "
            "any expensive commercial software."
        ),
        (
            "Why did you choose Kivy instead of a web framework?",
            "Kivy produces a single Python codebase that compiles to both Windows EXE and Android APK. "
            "Since field engineers often work on tablets, Android support was a key requirement. "
            "A web app would require a backend server, which is not ideal in remote field locations."
        ),
        (
            "Explain Archie's equation and the parameters m and n.",
            "Archie (1942) relates water saturation Sw to formation resistivity: "
            "Sw = (a·Rw / (φ^m · Rt))^(1/n). "
            "φ is porosity, Rt is true resistivity, Rw is water resistivity. "
            "m (cementation factor, ~2) describes how pore-throat tortuosity affects conductivity. "
            "n (saturation exponent, ~2) describes how Sw affects resistivity. "
            "My app lets the user adjust m and n and re-plots instantly using cached data."
        ),
        (
            "How do you identify reservoir intervals automatically?",
            "I compute a GR midpoint cut-off = (GR_max + GR_min) / 2. "
            "I then iterate through depth rows: when GR drops below cut-off I mark the start of a zone, "
            "and when it rises back above I close the zone. Each zone's top, bottom, min-GR and max-GR "
            "are stored and shaded yellow across all log tracks."
        ),
        (
            "What is the AI module and why isn't it integrated?",
            "ai_welllog.py contains two classes: AICurveRecognizer (maps arbitrary LAS mnemonics to "
            "standard names using pattern matching and confidence scoring) and AIQualityChecker "
            "(flags missing data, depth reversals, spikes, and stuck-tool signatures). "
            "The module works standalone; UI integration is a planned next step — a Quality Report screen."
        ),
        (
            "How did you handle the UI freezing during plotting?",
            "Matplotlib rendering is CPU-intensive. I wrap each plot call in Clock.schedule_once(lambda dt: plot(), 0.1). "
            "This yields control back to Kivy for one frame, allowing the MDSpinner loading indicator "
            "to appear before computation begins. The hide_loading() call is in a finally block to "
            "ensure the spinner always disappears even on error."
        ),
        (
            "What would you improve if you had more time?",
            "1. Fully integrate the AI quality checker as a dedicated screen. "
            "2. Add depth-track zooming (pinch-to-zoom on Android). "
            "3. Support LAS 3.0 and DLIS file formats. "
            "4. Add a cross-plot view (density vs neutron) for lithology identification. "
            "5. Cloud sync — save interpreted logs to a server for team collaboration."
        ),
        (
            "How did you manage Android compatibility?",
            "The main issue was lasio's C-extension dependency. I wrote a pure-Python LAS parser "
            "(read_las_pure_python) that works without compiled extensions. The app detects which "
            "reader to use at runtime. I also set up a GitHub Actions workflow that runs Buildozer "
            "on Ubuntu to produce the APK automatically on every push."
        ),
        (
            "How is the PDF report generated?",
            "I use matplotlib.backends.backend_pdf.PdfPages. After plotting, each Matplotlib figure "
            "is re-drawn on sub-axes of a new A4-landscape figure (3 tracks per page). "
            "Data is extracted from the original axes using get_lines() and get_collections(), "
            "then re-plotted with the same axis limits. A title page and a summary page "
            "(with net pay stats and methodology) bookend the track pages."
        ),
    ]

    y = 0.88
    for i, (q, a) in enumerate(qas):
        if y < 0.07:
            break
        bax = box(fig, 0.07, y - 0.012, 0.86, 0.028, fc=BLUE)
        bax.text(0.02, 0.5, f"Q{i+1}:  {q}", color=WHITE, fontsize=8.5,
                 fontweight="bold", va="center", transform=bax.transAxes)
        y -= 0.040
        fig.text(0.09, y, a, fontsize=8.5, color=DKGREY,
                 wrap=True, linespacing=1.5)
        y -= 0.062

    save(fig, pdf)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 10 — PROJECT STRUCTURE & KNOWN ISSUES
# ─────────────────────────────────────────────────────────────────────────────

def page_structure(pdf):
    fig = new_page(pdf, "9.  Project Structure & Known Issues / Future Work")

    section(fig, 0.88, "9.1  File Structure")

    tree = [
        ("k_vscode/",                              0, True),
        ("├── main.py",                            1, False),
        ("├── ai_welllog.py",                      1, False),
        ("├── generate_report.py",                 1, False),
        ("├── screens/",                           1, True),
        ("│   ├── start_screen.py",                2, False),
        ("│   ├── welllog_screen.py",              2, False),
        ("│   ├── viewlog_screen.py",              2, False),
        ("│   ├── interpretation_screen.py",       2, False),
        ("│   ├── vshale_screen.py",               2, False),
        ("│   ├── porosity_screen.py",             2, False),
        ("│   ├── water_saturation_screen.py",     2, False),
        ("│   └── reservoir_screen.py",            2, False),
        ("├── kv_files/   (8 × .kv UI layouts)",   1, True),
        ("├── utils/",                             1, True),
        ("│   ├── android_file_utils.py",          2, False),
        ("│   ├── plot_utils.py",                  2, False),
        ("│   └── constants.py",                   2, False),
        ("└── assets/   (icons, images)",          1, True),
    ]
    y = 0.82
    for name, indent, is_dir in tree:
        color = BLUE if is_dir else DKGREY
        weight = "bold" if is_dir else "normal"
        fig.text(0.07 + indent * 0.03, y, name,
                 fontsize=8.5, color=color, fontweight=weight,
                 fontfamily="monospace")
        y -= 0.030

    y -= 0.01
    section(fig, y, "9.2  Known Issues (identified, not yet fixed)")
    y -= 0.055
    issues = [
        "main.py — resource_path() defined twice; Config.set() called twice; debug prints remain.",
        "interpretation_screen.py:48 — navigates to 'watersaturation' (missing underscore); should be 'water_saturation'.",
        "reservoir_screen.py — two lines of dead code after return in reinterpret_with_new_parameters().",
        "viewlog_screen.py — 8 debug print() statements left in production code.",
        "utils/file_utils.py — duplicate of android_file_utils.py; never imported; should be deleted.",
    ]
    for iss in issues:
        bullet(fig, 0.09, y, iss, color="#CC0000")
        y -= 0.040

    y -= 0.01
    section(fig, y, "9.3  Future Work")
    y -= 0.055
    future = [
        "Integrate AIQualityChecker as a dedicated 'Data Quality Report' screen.",
        "Support DLIS and LAS 3.0 file formats.",
        "Add pinch-to-zoom depth track on Android.",
        "Crossplot view: Density vs Neutron for lithology identification.",
        "Formation evaluation export to Excel / CSV.",
        "Cloud save: sync interpreted logs to Firebase or similar backend.",
        "Machine learning model for lithofacies classification from log curves.",
    ]
    for f in future:
        bullet(fig, 0.09, y, f, color="#2E8B57")
        y -= 0.040

    save(fig, pdf)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("Generating PDF report...")
    with PdfPages(OUTPUT) as pdf:
        page_cover(pdf)
        page_overview(pdf)
        page_tech(pdf)
        page_arch(pdf)
        page_petro(pdf)
        page_reservoir_ai(pdf)
        page_features(pdf)
        page_challenges(pdf)
        page_qa(pdf)
        page_structure(pdf)

        # PDF metadata
        d = pdf.infodict()
        d["Title"]   = "WellLog Insight — FYP II Project Report"
        d["Author"]  = "Afiq Syahmi"
        d["Subject"] = "Interview Preparation Report"
        d["Keywords"] = "petrophysics, kivy, well log, LAS, python"

    print(f"\nDone!  Report saved to:  {os.path.abspath(OUTPUT)}")


if __name__ == "__main__":
    main()
