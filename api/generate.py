"""
Vercel Python serverless function.
GET /api/generate?division=Math
Returns the rankings PDF as application/pdf.
"""

import csv
import re
import io
import os

import pdfplumber
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# ── Valid divisions (must match filenames in /data) ───────────────────────────
DIVISIONS = ["Arts", "Engineering", "Innovate", "Math", "Science", "Spirit", "Technology"]

# Paths relative to repo root — Vercel includes everything committed to the repo
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")

# ── Colours ───────────────────────────────────────────────────────────────────
VEX_RED    = colors.HexColor("#CC0000")
VEX_DARK   = colors.HexColor("#1A1A2E")
VEX_MID    = colors.HexColor("#16213E")
VEX_ACCENT = colors.HexColor("#E94560")
ROW_ALT    = colors.HexColor("#F5F7FA")
GOLD       = colors.HexColor("#FFD700")
SILVER     = colors.HexColor("#C0C0C0")
BRONZE     = colors.HexColor("#CD7F32")
TEXT_DARK  = colors.HexColor("#1A1A2E")
TEXT_MID   = colors.HexColor("#4A4A6A")
TEXT_LIGHT = colors.white
MUTED      = colors.HexColor("#AAAACC")


# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_from_pdf(pdf_bytes: bytes):
    team_pat  = re.compile(r'\b(\d+[A-Z])\b')
    title_pat = re.compile(
        r'(\d{4}\s+VEX\s+Robotics\s+World\s+Championship)\s*[-–]\s*(.+Division)',
        re.IGNORECASE,
    )
    teams, seen = [], set()
    event_title = division_name = None

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            if event_title is None:
                m = title_pat.search(text)
                if m:
                    event_title   = m.group(1).strip()
                    division_name = m.group(2).strip()
            for m in team_pat.finditer(text):
                t = m.group(1)
                if t not in seen:
                    seen.add(t)
                    teams.append(t)

    return teams, event_title or "2026 VEX Robotics World Championship", division_name or "Division"


def load_skills(csv_path: str):
    skills = {}
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            t = row["Team Number"].strip()
            skills[t] = {
                "global_rank": int(row["Rank"]),
                "score":       int(row["Score"]),
                "auto":        int(row["Autonomous Coding Skills"]),
                "driver":      int(row["Driver Skills"]),
                "team_name":   row["Team Name"].strip(),
                "country":     row["Country / Region"].strip(),
            }
    return skills


def build_ranking(division_teams, skills):
    ranked, no_score = [], []
    for t in division_teams:
        if t in skills:
            ranked.append({"team_number": t, **skills[t]})
        else:
            no_score.append(t)
    ranked.sort(key=lambda x: (-x["score"], x["global_rank"]))
    for i, r in enumerate(ranked, 1):
        r["div_rank"] = i
    return ranked, no_score


def build_pdf_bytes(ranked, no_score, event_title, division_name) -> bytes:
    buf = io.BytesIO()
    W, H = A4

    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=14*mm, rightMargin=14*mm,
        topMargin=14*mm,  bottomMargin=16*mm,
        title=f"{division_name} – Skills Rankings",
        author="HABS Gliders Scouting",
    )

    def sty(name, **kw): return ParagraphStyle(name, **kw)
    event_s = sty("ev",  fontSize=9,   textColor=MUTED,      alignment=TA_CENTER, fontName="Helvetica")
    div_s   = sty("dv",  fontSize=22,  textColor=TEXT_LIGHT, alignment=TA_CENTER, fontName="Helvetica-Bold")
    sub_s   = sty("sb",  fontSize=9,   textColor=MUTED,      alignment=TA_CENTER, fontName="Helvetica")
    stats_s = sty("st",  fontSize=8,   textColor=MUTED,      alignment=TA_CENTER, fontName="Helvetica")
    cc      = sty("cc",  fontSize=7.5, textColor=TEXT_DARK,  alignment=TA_CENTER, fontName="Helvetica",      leading=10)
    cl      = sty("cl",  fontSize=7.5, textColor=TEXT_DARK,  alignment=TA_LEFT,   fontName="Helvetica",      leading=10)
    rg      = sty("rg",  fontSize=9,   textColor=TEXT_DARK,  alignment=TA_CENTER, fontName="Helvetica-Bold")
    rr      = sty("rr",  fontSize=9,   textColor=VEX_RED,    alignment=TA_CENTER, fontName="Helvetica-Bold")
    hdr_s   = sty("hdr", fontSize=7.5, textColor=TEXT_LIGHT, alignment=TA_CENTER, fontName="Helvetica-Bold")
    note_s  = sty("note",fontSize=7.5, textColor=TEXT_MID,   alignment=TA_LEFT,   fontName="Helvetica",      leading=11)

    story = []

    banner = Table([
        [Paragraph(event_title,   event_s)],
        [Paragraph(division_name, div_s)],
        [Paragraph("Skills Rankings", sub_s)],
        [Paragraph(
            f"{len(ranked)} teams ranked  ·  "
            f"{len(no_score)} team{'s' if len(no_score) != 1 else ''} with no skills score recorded",
            stats_s,
        )],
    ], colWidths=[W - 28*mm])
    banner.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), VEX_DARK),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("TOPPADDING",    (0,0), (-1,0),  12),
        ("BOTTOMPADDING", (0,0), (-1,0),  6),
        ("TOPPADDING",    (0,1), (-1,1),  0),
        ("BOTTOMPADDING", (0,1), (-1,1),  6),
        ("TOPPADDING",    (0,2), (-1,2),  0),
        ("BOTTOMPADDING", (0,2), (-1,2),  4),
        ("TOPPADDING",    (0,3), (-1,3),  0),
        ("BOTTOMPADDING", (0,3), (-1,3),  12),
    ]))
    story.append(banner)
    story.append(Spacer(1, 5*mm))

    col_labels = ["Div #", "Global #", "Score", "Auto", "Driver",
                  "Team #", "Team Name", "Country / Region"]
    col_widths = [16*mm, 20*mm, 15*mm, 13*mm, 15*mm, 17*mm, 52*mm, 0]
    col_widths[-1] = (W - 28*mm) - sum(col_widths[:-1])

    table_data = [[Paragraph(h, hdr_s) for h in col_labels]]
    for r in ranked:
        rs = rg if r["div_rank"] <= 3 else rr
        table_data.append([
            Paragraph(f"#{r['div_rank']}",    rs),
            Paragraph(f"#{r['global_rank']}", cc),
            Paragraph(str(r["score"]),        cc),
            Paragraph(str(r["auto"]),         cc),
            Paragraph(str(r["driver"]),       cc),
            Paragraph(r["team_number"],       cc),
            Paragraph(r["team_name"],         cl),
            Paragraph(r["country"],           cl),
        ])

    cmds = [
        ("BACKGROUND",    (0,0), (-1,0),  VEX_MID),
        ("LINEBELOW",     (0,0), (-1,0),  1.5, VEX_ACCENT),
        ("LINEBELOW",     (0,1), (-1,-1), 0.3, colors.HexColor("#DDDDEE")),
        ("BOX",           (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCDD")),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 4),
        ("RIGHTPADDING",  (0,0), (-1,-1), 4),
    ]
    medal = {1: GOLD, 2: SILVER, 3: BRONZE}
    for i, r in enumerate(ranked, 1):
        if r["div_rank"] in medal:
            cmds.append(("BACKGROUND", (0,i), (-1,i), medal[r["div_rank"]]))
        elif i % 2 == 0:
            cmds.append(("BACKGROUND", (0,i), (-1,i), ROW_ALT))
        else:
            cmds.append(("BACKGROUND", (0,i), (-1,i), colors.white))

    main = Table(table_data, colWidths=col_widths, repeatRows=1)
    main.setStyle(TableStyle(cmds))
    story.append(main)

    if no_score:
        story.append(Spacer(1, 5*mm))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CCCCDD")))
        story.append(Spacer(1, 2*mm))
        story.append(Paragraph(
            f"<b>No skills score recorded ({len(no_score)}):</b>  " + ",  ".join(no_score),
            note_s,
        ))

    story.append(Spacer(1, 4*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CCCCDD")))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "Generated from official VEX Robotics global skills standings  ·  "
        "Auto = Autonomous Coding Skills  ·  Driver = Driver Skills  ·  "
        "Ranked by Score (desc), then Global Rank (asc) on ties",
        note_s,
    ))

    footer_label = f"{division_name}  ·  Skills Rankings  ·  HABS Gliders Scouting"

    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(VEX_DARK)
        canvas.rect(0, H - 3*mm, W, 3*mm, fill=1, stroke=0)
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(TEXT_MID)
        canvas.drawRightString(W - 14*mm, 8*mm, f"Page {doc.page}  ·  {footer_label}")
        canvas.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    buf.seek(0)
    return buf.read()


# ── Vercel handler ────────────────────────────────────────────────────────────

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        qs = parse_qs(urlparse(self.path).query)
        division = qs.get("division", [None])[0]

        if not division or division not in DIVISIONS:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            valid = ", ".join(DIVISIONS)
            self.wfile.write(f'{{"error": "Invalid division. Choose from: {valid}"}}'.encode())
            return

        pdf_path = os.path.join(DATA_DIR, f"{division.lower()}-division-team-list.pdf")
        csv_path = os.path.join(DATA_DIR, "skills-standings.csv")

        for path in (pdf_path, csv_path):
            if not os.path.exists(path):
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(f'{{"error": "File not found: {os.path.basename(path)}"}}'.encode())
                return

        try:
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            teams, event_title, division_name = extract_from_pdf(pdf_bytes)
            skills = load_skills(csv_path)
            ranked, no_score = build_ranking(teams, skills)
            out_bytes = build_pdf_bytes(ranked, no_score, event_title, division_name)

            filename = f"{division.lower()}-division-skills-ranking.pdf"
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Disposition", f'inline; filename="{filename}"')
            self.send_header("Content-Length", str(len(out_bytes)))
            self.end_headers()
            self.wfile.write(out_bytes)

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(f'{{"error": "{str(e)}"}}'.encode())
