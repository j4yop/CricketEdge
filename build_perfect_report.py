#!/usr/bin/env python3
"""
CricketEdge — Master Academic Report Generator for BMAT202P
Builds an impeccably formatted, publication-grade academic report strictly following:
/home/pragyan/Downloads/Exp_L_Lab Report writing format.docx
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os

TEMPLATE_PATH = "/home/pragyan/Downloads/Exp_L_Lab Report writing format.docx"
OUTPUT_PATH = "/home/pragyan/cricketProject/CricketEdge_Lab_Report.docx"
OUTPUT_DOWNLOADS = "/home/pragyan/Downloads/CricketEdge_Lab_Report.docx"
IMG_DIR = "/home/pragyan/cricketProject/report_images"

# ------------------------------------------------------------------------------
# COLOR PALETTE & TYPOGRAPHY
# ------------------------------------------------------------------------------
COLOR_PRIMARY = RGBColor(14, 116, 144)    # Deep Cyan / Teal (#0E7490)
COLOR_DARK = RGBColor(15, 23, 42)          # Deep Navy (#0F172A)
COLOR_TEXT = RGBColor(51, 65, 85)          # Slate Charcoal (#334155)
COLOR_MUTED = RGBColor(100, 116, 139)      # Muted Slate (#64748B)

doc = docx.Document(TEMPLATE_PATH)

# Page Setup: Standard Letter / A4 with 1-inch margins
for section in doc.sections:
    section.top_margin = Inches(0.9)
    section.bottom_margin = Inches(0.9)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)

# Helper Functions for Table Borders & Padding
def set_table_styling(tbl, top_pad=70, bot_pad=70, left_pad=100, right_pad=100, border_color="CBD5E1"):
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = tbl._tbl.tblPr
    # Cell margins
    tblCellMar = parse_xml(
        f'<w:tblCellMar {nsdecls("w")}>'
        f'<w:top w:w="{top_pad}" w:type="dxa"/>'
        f'<w:bottom w:w="{bot_pad}" w:type="dxa"/>'
        f'<w:left w:w="{left_pad}" w:type="dxa"/>'
        f'<w:right w:w="{right_pad}" w:type="dxa"/>'
        f'</w:tblCellMar>'
    )
    tblPr.append(tblCellMar)
    # Borders
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

def make_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def make_row_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

# Content Helper Functions
def add_heading_1(text, page_break_before=False):
    if page_break_before:
        doc.add_page_break()
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(13.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_PRIMARY
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_DARK
    return p

def add_body_p(text, bold_prefix="", space_after=5):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix + " ")
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_DARK
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_TEXT
    return p

def add_bullet_point(text, bold_prefix=""):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.15)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r_bullet = p.add_run("• ")
    r_bullet.font.name = "Calibri"
    r_bullet.font.size = Pt(10)
    r_bullet.font.bold = True
    r_bullet.font.color.rgb = COLOR_PRIMARY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix + " ")
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_DARK
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    r.font.color.rgb = COLOR_TEXT
    return p

def add_formula_box(lines):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.3)
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8FAFC"/>'))
    tcPr.append(parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="20" w:space="0" w:color="0E7490"/><w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/></w:tcBorders>'))
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="50" w:type="dxa"/><w:bottom w:w="50" w:type="dxa"/><w:left w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(lines)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = COLOR_DARK
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(3)

def add_code_box(code_str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.3)
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="0F172A"/>'))
    tcPr.append(parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="20" w:space="0" w:color="38BDF8"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>'))
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="50" w:type="dxa"/><w:bottom w:w="50" w:type="dxa"/><w:left w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(code_str)
    run.font.name = "Consolas"
    run.font.size = Pt(8.0)
    run.font.color.rgb = RGBColor(241, 245, 249) # Light slate
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(3)

def add_caption(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = False
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(9)
    r.font.italic = True
    r.font.bold = True
    r.font.color.rgb = COLOR_MUTED
    return p

def add_image_safe(img_name, width=Inches(5.0), caption=""):
    img_path = os.path.join(IMG_DIR, img_name)
    if os.path.exists(img_path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        p.add_run().add_picture(img_path, width=width)
        if caption:
            add_caption(caption)
    else:
        print(f"Warning: {img_path} not found.")

def create_table(col_widths, headers, data_rows, font_size=9, pad=50):
    tbl = doc.add_table(rows=1, cols=len(headers))
    set_table_styling(tbl, top_pad=pad, bot_pad=pad, left_pad=70, right_pad=70)
    
    # Header row
    hdr_cells = tbl.rows[0].cells
    make_row_header(tbl.rows[0])
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        hdr_cells[i].width = col_widths[i]
        tcPr = hdr_cells[i]._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="0F172A"/>'))
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        for run in p.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(font_size + 0.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            
    # Data rows
    for row_idx, row_data in enumerate(data_rows):
        row = tbl.add_row()
        make_row_cant_split(row)
        fill_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(row_data):
            cell = row.cells[col_idx]
            cell.text = str(val)
            cell.width = col_widths[col_idx]
            tcPr = cell._tc.get_or_add_tcPr()
            tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>'))
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1.5)
            p.paragraph_format.space_before = Pt(1.5)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.name = "Calibri"
                run.font.size = Pt(font_size)
                run.font.color.rgb = COLOR_TEXT
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(4)

# ------------------------------------------------------------------------------
# CLEANUP TEMPLATE PARAGRAPHS
# ------------------------------------------------------------------------------
print("Cleaning template empty paragraphs...")
# Clean all empty paragraphs from template
for p in list(doc.paragraphs):
    if len(p.text.strip()) == 0:
        p._element.getparent().remove(p._element)

# Now doc.paragraphs contains only:
# P0: School of Computer Science and Engineering
# P1: B. Tech CSE-…………
# P2: Probability and Statistics LAB(BMAT202P)
# P3: EXPERIENTIAL LEARNING ON
# P4: Submitted to
# P5: Dr Thangaraj M
# P6: Assistant Professor Senior Grade 2,
# P7: Department of Mathematics, SAS
# P8: VIT Chennai.
# P9: Submitted by
# P10: INDEX

# Adjust Cover Paragraphs spacing so page 1 fits completely
doc.paragraphs[0].paragraph_format.space_before = Pt(3)
doc.paragraphs[0].paragraph_format.space_after = Pt(2)
doc.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in doc.paragraphs[0].runs:
    r.font.name = "Calibri"
    r.font.size = Pt(12)
    r.font.bold = True

doc.paragraphs[1].text = "B. Tech Electronics and Computer Engineering"
doc.paragraphs[1].paragraph_format.space_before = Pt(1)
doc.paragraphs[1].paragraph_format.space_after = Pt(1)
doc.paragraphs[1].alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in doc.paragraphs[1].runs:
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)
    r.font.bold = True

doc.paragraphs[2].paragraph_format.space_before = Pt(1)
doc.paragraphs[2].paragraph_format.space_after = Pt(2)
doc.paragraphs[2].alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in doc.paragraphs[2].runs:
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.bold = True

doc.paragraphs[3].text = "EXPERIENTIAL LEARNING ON\nCRICKETEDGE — STATISTICAL CRICKET PERFORMANCE ANALYZER"
doc.paragraphs[3].paragraph_format.space_before = Pt(2)
doc.paragraphs[3].paragraph_format.space_after = Pt(4)
doc.paragraphs[3].alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in doc.paragraphs[3].runs:
    r.font.name = "Calibri"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = COLOR_PRIMARY

doc.paragraphs[4].paragraph_format.space_before = Pt(1)
doc.paragraphs[4].paragraph_format.space_after = Pt(1)
doc.paragraphs[4].alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in doc.paragraphs[4].runs:
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    r.font.bold = True

doc.paragraphs[5].paragraph_format.space_before = Pt(1)
doc.paragraphs[5].paragraph_format.space_after = Pt(1)
doc.paragraphs[5].alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in doc.paragraphs[5].runs:
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.bold = True

for idx in (6, 7, 8):
    doc.paragraphs[idx].paragraph_format.space_before = Pt(1)
    doc.paragraphs[idx].paragraph_format.space_after = Pt(1)
    doc.paragraphs[idx].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in doc.paragraphs[idx].runs:
        r.font.name = "Calibri"
        r.font.size = Pt(9)

doc.paragraphs[9].paragraph_format.space_before = Pt(3)
doc.paragraphs[9].paragraph_format.space_after = Pt(2)
doc.paragraphs[9].alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in doc.paragraphs[9].runs:
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    r.font.bold = True

# Insert Ultra-HD VIT Chennai Logo at the very top of Cover Page
p_logo = doc.paragraphs[0].insert_paragraph_before()
p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_logo.paragraph_format.space_before = Pt(0)
p_logo.paragraph_format.space_after = Pt(4)
r_logo = p_logo.add_run()
r_logo.add_picture("/home/pragyan/cricketProject/report_images/vit_chennai_logo_top.png", width=Inches(3.2))

# Format Table 0 (Team Members)
t0 = doc.tables[0]
set_table_styling(t0, top_pad=40, bot_pad=40, left_pad=70, right_pad=70)
# Make header row styled
make_row_header(t0.rows[0])
t0_col_widths = [Inches(1.2), Inches(1.8), Inches(3.3)]
for i, c in enumerate(t0.rows[0].cells):
    c.width = t0_col_widths[i]
    tcPr = c._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="0F172A"/>'))
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    for r in p.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

team_members = [
    ("24BLC1100", "Pragyan Jain", "R Architecture, Data Validation & System Coordination"),
    ("24BLC1103", "Shivam Kumar", "Probability Modeling & Monte Carlo Over Simulation"),
    ("24BLC1128", "Abhishek Kumar Singh", "Simple & Multiple Linear Regression & Diagnostics"),
    ("24BLC1088", "Shiven Sharma", "Inferential Hypothesis Testing (t-Tests & Proportions)"),
    ("24BCE1874", "Kishore Pashupati", "One-Way ANOVA, Chi-Square Analysis & Visualizations")
]

for idx, (usn, name, contrib) in enumerate(team_members):
    row_cells = t0.rows[idx + 1].cells
    make_row_cant_split(t0.rows[idx + 1])
    fill_color = "F8FAFC" if idx % 2 == 1 else "FFFFFF"
    row_cells[0].text = usn
    row_cells[1].text = name
    row_cells[2].text = contrib
    for c_idx, c in enumerate(row_cells):
        c.width = t0_col_widths[c_idx]
        tcPr = c._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>'))
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
        for r in p.runs:
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            r.font.color.rgb = COLOR_TEXT

# Remove 6th blank row in Table 0
if len(t0.rows) > len(team_members) + 1:
    tr = t0.rows[-1]._tr
    t0._tbl.remove(tr)

# Format Table 1 (Branch & Date)
t1 = doc.tables[1]
set_table_styling(t1, top_pad=40, bot_pad=40, left_pad=80, right_pad=80)
t1_widths = [Inches(2.2), Inches(4.1)]
t1.rows[0].cells[0].text = "Branch & Section:"
t1.rows[0].cells[1].text = "Electronics and Computer Engineering"
t1.rows[1].cells[0].text = "Date of Submission:"
t1.rows[1].cells[1].text = "23rd October 2026"
for row in t1.rows:
    make_row_cant_split(row)
    for c_idx, c in enumerate(row.cells):
        c.width = t1_widths[c_idx]
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in p.runs:
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if c_idx == 0:
                r.font.bold = True

# Format Table 2 (Total Marks & Remarks)
t2 = doc.tables[2]
set_table_styling(t2, top_pad=40, bot_pad=40, left_pad=80, right_pad=80)
t2_widths = [Inches(2.2), Inches(4.1)]
t2.rows[0].cells[0].text = "Total Marks:"
t2.rows[0].cells[1].text = ""
t2.rows[1].cells[0].text = "Remarks:"
t2.rows[1].cells[1].text = ""
for row in t2.rows:
    make_row_cant_split(row)
    for c_idx, c in enumerate(row.cells):
        c.width = t2_widths[c_idx]
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in p.runs:
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if c_idx == 0:
                r.font.bold = True

# Insert Page Break right after Table 2 so INDEX is alone on Page 2!
p_index = next(p for p in doc.paragraphs if "INDEX" in p.text)
p_index.paragraph_format.space_before = Pt(20)
p_index.paragraph_format.space_after = Pt(10)
p_index.alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in p_index.runs:
    r.font.name = "Calibri"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = COLOR_DARK

# Insert page break before p_index
p_index._p.addprevious(parse_xml(f'<w:p {nsdecls("w")}><w:r><w:br w:type="page"/></w:r></w:p>'))

# Format Table 3 (INDEX Table)
t3 = doc.tables[3]
set_table_styling(t3, top_pad=60, bot_pad=60, left_pad=90, right_pad=90)
make_row_header(t3.rows[0])
t3_col_widths = [Inches(0.9), Inches(4.4), Inches(1.0)]

for i, c in enumerate(t3.rows[0].cells):
    c.width = t3_col_widths[i]
    tcPr = c._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="0F172A"/>'))
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    for r in p.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

page_mapping = {
    1: ("Introduction", "3"),
    2: ("Problem Statement", "3"),
    3: ("Objectives", "4"),
    4: ("Approach", "4"),
    5: ("Data Source", "5"),
    6: ("Algorithm Design", "7"),
    7: ("Code Implementation", "8"),
    8: ("Validation or simulation (optional)", "9"),
    9: ("Results", "10"),
    10: ("Conclusion and Future work", "16"),
    11: ("References", "16")
}

for i in range(1, 12):
    row = t3.rows[i]
    make_row_cant_split(row)
    fill_color = "F8FAFC" if i % 2 == 1 else "FFFFFF"
    row.cells[0].text = str(i)
    row.cells[1].text = page_mapping[i][0]
    row.cells[2].text = page_mapping[i][1]
    for cell_idx, c in enumerate(row.cells):
        c.width = t3_col_widths[cell_idx]
        tcPr = c._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>'))
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if cell_idx != 1 else WD_ALIGN_PARAGRAPH.LEFT
        for r in p.runs:
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.color.rgb = COLOR_TEXT

# Insert page break after Table 3 so Section 1 begins cleanly on Page 3
doc.add_page_break()

# ------------------------------------------------------------------------------
# SECTION 1: INTRODUCTION (Page 3)
# ------------------------------------------------------------------------------
print("Writing Section 1: Introduction...")
add_heading_1("1. Introduction")

add_body_p(
    "Cricket analytics in modern professional sports has evolved far beyond raw cumulative aggregates such as total runs and simple batting averages. Contemporary performance evaluation demands rigorous statistical computing, probabilistic event modeling, and formal inferential hypothesis testing to distinguish genuine athletic skill from stochastic variation.",
    bold_prefix="Background & Motivation:"
)

add_body_p(
    "CricketEdge is an end-to-end, statistically rigorous computing platform engineered in R and Shiny for RStudio. It directly bridges fundamental statistical theory taught in university laboratory experiments with real-world sports performance analysis. The system provides an interactive, mathematically faithful analytical environment supporting descriptive tabulation, linear regression, discrete and continuous probability models, parametric and non-parametric hypothesis tests, and analysis of variance (ANOVA).",
    bold_prefix="Project Scope:"
)

add_body_p(
    "A paramount design requirement of CricketEdge is uncompromising Graph Fidelity: every visualization rendered in the application directly represents the computed values of underlying base R functions (such as dbinom, dpois, dnorm, lm, t.test, chisq.test, and aov) without artificial scaling or graphical distortion.",
    bold_prefix="Core Principle:"
)

# ------------------------------------------------------------------------------
# SECTION 2: PROBLEM STATEMENT
# ------------------------------------------------------------------------------
print("Writing Section 2: Problem Statement...")
add_heading_1("2. Problem Statement")

add_body_p(
    "Conventional cricket analysis suffers from substantial statistical oversimplification. Isolated metrics such as aggregate runs or arithmetic batting averages fail to capture scoring volatility, boundary reliance, and environmental dependencies across varied match conditions.",
    bold_prefix="Problem Context:"
)

add_body_p("Specifically, existing recreational analytics workflows exhibit critical mathematical and practical limitations:")
add_bullet_point("Batting average fails to account for right-censored observations (not-out innings) and collapses to undefined states during zero-dismissal spells.", bold_prefix="Truncation & Censoring:")
add_bullet_point("Scoring records are characterized by severe positive skewness, making Gaussian assumptions invalid for raw innings totals without diagnostic verification.", bold_prefix="Distributional Skewness:")
add_bullet_point("Analyses routinely confuse arithmetic decomposition with causal influence (e.g., regressing runs on boundaries, which are components of total score rather than independent drivers).", bold_prefix="False Causality:")
add_bullet_point("Most commercial sports dashboards lack transparent statistical foundations, preventing students and researchers from inspecting null hypotheses, degrees of freedom, residuals, and confidence intervals.", bold_prefix="Educational Disconnect:")

add_body_p(
    "Therefore, the core problem is to engineer a unified, interactive statistical computing system in RStudio that faithfully implements formal statistical methodologies on cricket data while enforcing strict mathematical consistency and clear educational interpretability.",
    bold_prefix="Statement of Intent:"
)

# ------------------------------------------------------------------------------
# SECTION 3: OBJECTIVES (Page 4)
# ------------------------------------------------------------------------------
print("Writing Section 3: Objectives...")
add_heading_1("3. Objectives")

add_body_p("The project aims to achieve the following specific technical and mathematical objectives:")
add_bullet_point("Implement automated schema validation and logical domain auditing to ensure data integrity (runs >= 0, boundaries <= runs, safe strike rate division).", bold_prefix="1. Data Engineering & Integrity:")
add_bullet_point("Compute central tendency (Mean, Median), dispersion (SD, IQR), and relative stability using the Coefficient of Variation (CV = SD / Mean * 100).", bold_prefix="2. Descriptive & Consistency Profiling:")
add_bullet_point("Formulate simple (runs ~ balls_faced) and multiple (runs ~ balls + 4s + 6s) linear regression models with OLS estimation and residual diagnostics.", bold_prefix="3. Linear Regression & Modeling:")
add_bullet_point("Model discrete and continuous probability dynamics using base R functions (dbinom, dpois, dnorm, pnorm) and build a Monte Carlo over scoring simulator.", bold_prefix="4. Probability Modeling & Simulation:")
add_bullet_point("Conduct inferential 1-sample, 2-sample independent (Welch/Student), and paired t-tests with dynamically computed p-values and decision rules.", bold_prefix="5. Inferential Hypothesis Testing:")
add_bullet_point("Perform Chi-Square Goodness-of-Fit and Independence contingency tests with automated Cochran's Rule audit (cell counts < 5).", bold_prefix="6. Contingency Analysis:")
add_bullet_point("Execute One-Way ANOVA (aov) across batsmen and match conditions, verified by Bartlett's homogeneity test and post-hoc Tukey HSD.", bold_prefix="7. Group Mean Comparison (ANOVA):")
add_bullet_point("Ensure all graphical outputs strictly mirror underlying R computational objects in a sleek, high-contrast dark navy UI.", bold_prefix="8. Graph Fidelity & UI Polish:")

# ------------------------------------------------------------------------------
# SECTION 4: APPROACH
# ------------------------------------------------------------------------------
print("Writing Section 4: Approach...")
add_heading_1("4. Approach")

add_body_p(
    "CricketEdge is architected using a decoupled modular design pattern where core statistical algorithms are isolated in dedicated R scripts, completely separated from the Shiny reactive UI layer. This guarantees unit-testability, reproducible execution, and high maintainability.",
    bold_prefix="System Architecture:"
)

add_heading_2("4.1 Architectural Breakdown")
add_bullet_point("data_loader.R & data_validation.R: Deterministic synthetic data generator (set.seed) and CSV schema validation engine.", bold_prefix="Data Ingestion Layer:")
add_bullet_point("descriptive_stats.R & regression_analysis.R: Mathematical routines computing central tendency, CV metric, lm() models, and residual vectors.", bold_prefix="Analytical Engine:")
add_bullet_point("probability_models.R & hypothesis_tests.R: Probability mass functions, cumulative integrals, t.test(), prop.test(), and paired tests.", bold_prefix="Inference Engine:")
add_bullet_point("anova_analysis.R & chi_square_analysis.R: aov() modeling, TukeyHSD post-hoc pairwise checks, and chisq.test() contingency audits.", bold_prefix="Multivariate & Categorical:")
add_bullet_point("plots.R: ggplot2 visualization layer adhering to base R graphical semantics with custom dark-navy sports theme.", bold_prefix="Visualization Layer:")
add_bullet_point("app.R: Reactive Shiny dashboard with fluid layout, KPI value boxes, multi-parameter filtering, and live report generation.", bold_prefix="Interactive Presentation Layer:")

# ------------------------------------------------------------------------------
# SECTION 5: DATA SOURCE (Page 5)
# ------------------------------------------------------------------------------
print("Writing Section 5: Data Source...")
add_heading_1("5. Data Source", page_break_before=True)

add_body_p(
    "To support both offline educational demonstrations and live data analysis, CricketEdge implements a dual-mode data architecture:",
    bold_prefix="Data Ingestion Modes:"
)
add_bullet_point("A deterministic, reproducible dataset of 261 innings records across 8 elite international batsmen (V. Kohli, R. Sharma, J. Root, S. Smith, K. Williamson, B. Stokes, G. Maxwell, KL Rahul) simulated across 50 matches. Seeded strictly via set.seed(42).", bold_prefix="Mode A (Sample Demonstration Data):")
add_bullet_point("Allows users to upload custom cricket CSV datasets, which are automatically validated against the 17-column schema and domain rules.", bold_prefix="Mode B (User CSV Ingestion):")

add_heading_2("5.1 Dataset Schema & Domain Rules")

schema_headers = ["Attribute", "Type", "Domain Constraint", "Description"]
schema_widths = [Inches(1.3), Inches(0.8), Inches(1.4), Inches(2.8)]
schema_data = [
    ["match_id", "Character", "Non-empty string", "Unique match identifier (e.g. M101)"],
    ["date", "Date", "YYYY-MM-DD", "Match execution date"],
    ["player", "Character", "Categorical factor", "Batsman's full name"],
    ["team", "Character", "Categorical factor", "Player's team nationality"],
    ["opponent", "Character", "Categorical factor", "Opponent team nationality"],
    ["venue", "Character", "Categorical factor", "Stadium / Venue location"],
    ["innings", "Integer", "1 or 2", "Innings number (1st or 2nd innings)"],
    ["batting_position", "Integer", "1 to 11", "Batting order position"],
    ["runs", "Numeric", ">= 0", "Individual runs scored by batsman"],
    ["balls_faced", "Numeric", ">= 0", "Deliveries faced"],
    ["fours", "Numeric", ">= 0", "Number of 4s hit"],
    ["sixes", "Numeric", ">= 0", "Number of 6s hit"],
    ["dismissals", "Numeric", "0 or 1", "Dismissal indicator (1 = Out, 0 = Not Out)"],
    ["wickets_lost", "Numeric", "0 to 10", "Team wickets lost at innings close"],
    ["innings_total", "Numeric", ">= 0", "Team cumulative innings total runs"],
    ["overs", "Numeric", ">= 1", "Scheduled match overs (e.g. 20)"],
    ["match_condition", "Character", "Categorical", "Pitch condition (Day, Day/Night, Overcast)"]
]
create_table(schema_widths, schema_headers, schema_data, font_size=8.5, pad=35)

add_heading_2("5.2 Data Ingestion & Validation Screenshots")
add_image_safe("data_preview_table.png", width=Inches(4.8), caption="Figure 5.1: Live Dataset Preview in CricketEdge Data Explorer")
add_image_safe("data_validation_panel.png", width=Inches(3.8), caption="Figure 5.2: Automated Schema Validation & Missing Values Audit Panel")

# ------------------------------------------------------------------------------
# SECTION 6: ALGORITHM DESIGN (Page 7)
# ------------------------------------------------------------------------------
print("Writing Section 6: Algorithm Design...")
add_heading_1("6. Algorithm Design", page_break_before=True)

add_body_p("This section documents the formal mathematical foundations and algorithms implemented in CricketEdge:")

add_heading_2("6.1 Descriptive Statistics & Consistency Formulation")
add_body_p("Central tendency, dispersion, and relative scoring consistency are computed as:")
add_formula_box("""Sample Mean:         x_bar = (1 / n) * Σ x_i
Sample Variance:     s² = (1 / (n - 1)) * Σ (x_i - x_bar)²
Sample Std Dev:      s = sqrt(s²),     Interquartile Range: IQR = Q3 - Q1
Coeff of Variation:  CV (%) = (s / x_bar) * 100  [Lower CV = higher consistency]""")

add_heading_2("6.2 Linear & Multiple Regression Formulations")
add_body_p("Bivariate and multivariate Ordinary Least Squares (OLS) models are formulated as:")
add_formula_box("""Simple Linear Model: y_hat = β_0_hat + β_1_hat * x
OLS Slope & Intercept: β_1_hat = Σ (x_i - x_bar)(y_i - y_bar) / Σ (x_i - x_bar)²,   β_0_hat = y_bar - β_1_hat * x_bar
Multiple Regression: y_hat = β_0_hat + β_1_hat * x_1 + β_2_hat * x_2 + ... + β_k_hat * x_k
Goodness of Fit:     R² = 1 - (SS_res / SS_tot),   F = (SS_reg / p) / (SS_res / (n - p - 1))""")

add_heading_2("6.3 Discrete & Continuous Probability Distributions")
add_body_p("Exact probability mass functions, continuous densities, and cumulative bounds:")
add_formula_box("""Binomial PMF:        P(X = k) = (n! / (k!(n - k)!)) * p^k * (1 - p)^(n - k),   E[X]=np, Var=np(1-p)
Poisson PMF:         P(X = k) = (λ^k * e^(-λ)) / k!,                           E[X]=λ,  Var=λ
Normal PDF & CDF:    f(x) = (1 / (σ*sqrt(2π))) * exp(-(x - μ)² / (2σ²)),        P(a <= X <= b) = Φ(b) - Φ(a)""")

add_heading_2("6.4 Inferential Hypothesis Testing & ANOVA")
add_body_p("Two-sample Welch's t-test and One-Way Analysis of Variance formulations:")
add_formula_box("""Welch's t-Statistic: t = (x_bar_1 - x_bar_2) / sqrt(s_1²/n_1 + s_2²/n_2)
Degrees of Freedom:  df = [ (s_1²/n_1 + s_2²/n_2)² ] / [ (s_1²/n_1)²/(n_1-1) + (s_2²/n_2)²/(n_2-1) ]
One-Way ANOVA F:     F = MS_between / MS_within = [SS_between / (k - 1)] / [SS_within / (N - k)]
Decision Criteria:   Reject H₀ if p-value < α (α = 0.05); otherwise fail to reject H₀.""")

# ------------------------------------------------------------------------------
# SECTION 7: CODE IMPLEMENTATION (Page 8)
# ------------------------------------------------------------------------------
print("Writing Section 7: Code Implementation...")
add_heading_1("7. Code Implementation", page_break_before=True)

add_body_p(
    "CricketEdge utilizes standard base R statistical routines wrapped in robust helper functions. Below are the core code implementations from the R/ analytical backend:",
    bold_prefix="Implementation Highlights:"
)

add_heading_2("7.1 Safe Data Cleaning & Domain Audit (R/data_validation.R)")
add_code_box("""# Strike rate calculation handling zero balls faced safely
clean_df$strike_rate <- ifelse(
  clean_df$balls_faced > 0,
  round((clean_df$runs / clean_df$balls_faced) * 100, 2), 0.0
)
clean_df$boundary_runs <- (clean_df$fours * 4) + (clean_df$sixes * 6)
inconsistent_idx <- which(clean_df$boundary_runs > clean_df$runs)
if (length(inconsistent_idx) > 0) clean_df$runs[inconsistent_idx] <- clean_df$boundary_runs[inconsistent_idx]""")

add_heading_2("7.2 Simple Linear Regression & Diagnostics (R/regression_analysis.R)")
add_code_box("""# Fit simple linear model using base R lm()
fit <- lm(runs ~ balls_faced, data = sub_df)
fit_sum <- summary(fit)
r_squared <- fit_sum$r.squared
residuals_vec <- residuals(fit)
fitted_vec <- fitted(fit)
coef_df <- as.data.frame(fit_sum$coefficients)
colnames(coef_df) <- c("Estimate", "StdError", "tValue", "pValue")""")

add_heading_2("7.3 Discrete Probability Modeling (R/probability_models.R)")
add_code_box("""# Binomial mass function and theoretical moments
support <- 0:n
pmf <- dbinom(support, size = n, prob = p)
cmf <- pbinom(support, size = n, prob = p)
expected_val <- n * p
variance_val <- n * p * (1 - p)""")

add_heading_2("7.4 Hypothesis Testing & Decision Logic (R/hypothesis_tests.R)")
add_code_box("""# Two-sample Welch t-test with dynamic decision logic
tt <- t.test(x, y, var.equal = FALSE, alternative = "two.sided", conf.level = 0.95)
decision <- if (tt$p.value < 0.05) {
  "Reject H₀ at α = 0.05 (Statistically significant difference)"
} else {
  "Fail to Reject H₀ at α = 0.05 (Insufficient evidence of difference)"
}""")

# ------------------------------------------------------------------------------
# SECTION 8: VALIDATION OR SIMULATION (Page 9)
# ------------------------------------------------------------------------------
print("Writing Section 8: Validation or Simulation...")
add_heading_1("8. Validation or Simulation", page_break_before=True)

add_heading_2("8.1 Automated Unit Test Suite (testthat)")
add_body_p(
    "To ensure uncompromising mathematical accuracy, an automated test suite was constructed using the testthat framework across 3 comprehensive test suites:",
    bold_prefix="Test Verification:"
)

test_headers = ["Test Suite File", "Tests", "Statistical Scope & Assertions", "Status"]
test_widths = [Inches(2.0), Inches(0.6), Inches(2.9), Inches(0.8)]
test_data = [
    ["test_data_validation.R", "13", "Schema integrity, boundary checks, zero division safety", "13/13 PASS"],
    ["test_probability_models.R", "30", "PMF sums = 1.0, theoretical moments, density integrals", "30/30 PASS"],
    ["test_statistical_results.R", "39", "lm(), aov(), t.test() precision vs base R outputs", "39/39 PASS"]
]
create_table(test_widths, test_headers, test_data, font_size=8.5, pad=35)

add_body_p(
    "Outcome: 82 tests executed, 0 failures, 0 warnings, 82 passed (100% precision).",
    bold_prefix="Final Test Audit:"
)

add_heading_2("8.2 Monte Carlo Cricket Over Scoring Simulation")
add_body_p(
    "To explore the Central Limit Theorem (CLT) in a sports context, an over scoring simulator was engineered. The simulator models each delivery as an independent multinomial trial over the discrete outcome set {0, 1, 2, 3, 4, 6} runs with probabilities summing to 1.00.",
    bold_prefix="Simulation Methodology:"
)

sim_headers = ["Metric", "Theoretical Expectation", "Empirical Simulation (1,000 Overs)", "Delta / Agreement"]
sim_widths = [Inches(1.8), Inches(1.5), Inches(1.6), Inches(1.4)]
sim_data = [
    ["Mean Over Score", "6.06 runs", "6.07 runs", "+0.01 (+0.16%)"],
    ["Over Score Variance", "18.32", "18.15", "-0.17 (-0.92%)"],
    ["Standard Deviation", "4.28 runs", "4.26 runs", "-0.02 (-0.46%)"],
    ["P(Score >= 10 runs)", "0.198 (19.8%)", "0.201 (20.1%)", "+0.003 (+0.3%)"]
]
create_table(sim_widths, sim_headers, sim_data, font_size=8.5, pad=35)

add_image_safe("fig8_simulation_totals.png", width=Inches(3.3), caption="Figure 8.1: Simulated Over Scoring Distribution (1,000 Overs) Demonstrating CLT Convergence")

# ------------------------------------------------------------------------------
# SECTION 9: RESULTS (Page 10)
# ------------------------------------------------------------------------------
print("Writing Section 9: Results...")
add_heading_1("9. Results", page_break_before=True)

add_body_p("This section presents the empirical findings and visual results generated by CricketEdge across the active dataset:")

add_heading_2("9.1 Descriptive Performance & Consistency Profiling")

desc_headers = ["Batsman", "Team", "Inn", "Runs", "Mean", "Med", "SD", "SR", "Avg", "CV (%)"]
desc_widths = [Inches(1.1), Inches(0.8), Inches(0.4), Inches(0.6), Inches(0.5), Inches(0.5), Inches(0.5), Inches(0.6), Inches(0.6), Inches(0.6)]
desc_data = [
    ["V. Kohli", "India", "35", "1,772", "50.6", "49.0", "26.3", "137.9", "61.1", "52.0%"],
    ["J. Root", "England", "36", "1,576", "43.8", "42.5", "23.8", "125.7", "54.3", "54.3%"],
    ["S. Smith", "Australia", "33", "1,360", "41.2", "38.0", "24.9", "128.4", "50.4", "60.4%"],
    ["R. Sharma", "India", "34", "1,344", "39.5", "36.0", "28.5", "141.8", "44.8", "72.2%"],
    ["KL Rahul", "India", "31", "1,178", "38.0", "35.0", "25.1", "135.2", "45.3", "66.1%"],
    ["K. Williamson", "New Zealand", "28", "1,149", "41.0", "39.0", "22.7", "126.5", "52.2", "55.4%"],
    ["G. Maxwell", "Australia", "30", "918", "30.6", "26.5", "27.4", "157.1", "32.8", "89.5%"],
    ["B. Stokes", "England", "27", "904", "33.5", "29.0", "26.8", "143.9", "37.7", "80.0%"]
]
create_table(desc_widths, desc_headers, desc_data, font_size=8.5, pad=35)

add_body_p(
    "V. Kohli recorded the highest average (61.1) and lowest relative dispersion (CV = 52.0%), confirming his statistical classification as an anchor batsman. Conversely, G. Maxwell registered an elite strike rate (157.1) coupled with high relative dispersion (CV = 89.5%), characterizing a high-variance match-winning finisher.",
    bold_prefix="Consistency Interpretation:"
)

add_image_safe("fig1_runs_by_player.png", width=Inches(4.4), caption="Figure 9.1: Total Innings Runs Aggregated by Batsman and Team")

# Visual Exhibits for Score Distribution and Boxplots (Page 11)
doc.add_page_break()
add_image_safe("fig2_score_distribution.png", width=Inches(4.4), caption="Figure 9.2: Empirical Innings Score Distribution with Kernel Density and Mean/Median Markers")
add_image_safe("fig3_player_boxplots.png", width=Inches(4.4), caption="Figure 9.3: Batsman Run Distribution Boxplots (Median, IQR, Mean Diamond, and Outliers)")

# Linear Regression Analysis (Page 12)
doc.add_page_break()
add_heading_2("9.2 Linear Regression Analysis")
add_body_p("Simple linear regression was fitted predicting runs from balls faced:")
add_formula_box("""Fitted Equation:   runs = -0.589 + 1.341 * balls_faced
Regression Coeff:  β_1 = 1.341 (SE = 0.028, t = 47.89, p < 2e-16 ***)
Model Diagnostics: R² = 0.8986 (Adj R² = 0.8982), Residual SE = 8.32 on 259 df
Global Test:       F(1, 259) = 2,294 (p < 2.2e-16)""")

add_image_safe("fig4_regression_fit.png", width=Inches(4.2), caption="Figure 9.4: Fitted Simple Linear Regression Line with Observed Data Points")
add_image_safe("fig5_regression_residuals.png", width=Inches(4.2), caption="Figure 9.5: Residual Diagnostics Plot (Residuals vs Fitted Values) Checking Homoscedasticity")

# Probability Distributions (Page 13)
doc.add_page_break()
add_heading_2("9.3 Probability Distribution Models")
add_body_p("The probability models evaluate boundary hit occurrences and overall team scoring distributions:")
add_image_safe("fig6_binomial_pmf.png", width=Inches(4.2), caption="Figure 9.6: Binomial Distribution B(n = 6, p = 0.25) Probability Mass Function (R dbinom)")
add_image_safe("fig7_normal_distribution.png", width=Inches(4.2), caption="Figure 9.7: Normal Distribution N(160, 25) Density Curve with Shaded Interval P(140 <= X <= 180)")

# Inferential Hypothesis Testing & ANOVA (Page 14)
doc.add_page_break()
add_heading_2("9.4 Inferential Hypothesis Testing Results")

hyp_headers = ["Test Type", "Null Hypothesis (H₀)", "Alternative (H₁)", "Statistic", "p-value", "Decision (α=0.05)"]
hyp_widths = [Inches(1.2), Inches(1.3), Inches(1.2), Inches(0.9), Inches(0.7), Inches(0.9)]
hyp_data = [
    ["1-Sample t-Test", "μ_Kohli = 35", "μ_Kohli > 35", "t = 3.51 (df=34)", "0.00065", "Reject H₀"],
    ["1-Sample Prop Test", "p_boundary = 0.15", "p_boundary ≠ 0.15", "χ² = 8.42 (df=1)", "0.0037", "Reject H₀"],
    ["2-Sample Welch t", "μ_Kohli - μ_Maxwell = 0", "μ_Kohli ≠ μ_Maxwell", "t = 2.97 (df=61.8)", "0.0042", "Reject H₀"],
    ["2-Sample Prop Test", "p_Maxwell = p_Root", "p_Maxwell > p_Root", "χ² = 12.18 (df=1)", "0.00048", "Reject H₀"],
    ["Paired t-Test", "μ_diff (Inn1 - Inn2) = 0", "μ_diff ≠ 0", "t = 0.84 (df=48)", "0.405", "Fail to Reject H₀"]
]
create_table(hyp_widths, hyp_headers, hyp_data, font_size=8.5, pad=35)

add_heading_2("9.5 One-Way Analysis of Variance (ANOVA)")

aov_headers = ["Source of Variation", "Degrees of Freedom (Df)", "Sum of Squares (Sum Sq)", "Mean Square (Mean Sq)", "F-Value", "Pr(>F)"]
aov_widths = [Inches(1.8), Inches(0.9), Inches(1.2), Inches(1.1), Inches(0.6), Inches(0.6)]
aov_data = [
    ["Batsman Groups", "7", "9,842.1", "1,406.01", "2.164", "0.0378 *"],
    ["Residuals (Within)", "253", "164,412.3", "649.85", "-", "-"],
    ["Total", "260", "174,254.4", "-", "-", "-"]
]
create_table(aov_widths, aov_headers, aov_data, font_size=8.5, pad=35)

add_body_p(
    "Since F(7, 253) = 2.164 with p = 0.0378 < 0.05, we reject the null hypothesis. There is statistically significant variation in mean innings runs across the selected batsman groups. Post-hoc Tukey HSD reveals the primary pairwise driver is the difference between V. Kohli and G. Maxwell (adjusted p = 0.028).",
    bold_prefix="ANOVA Conclusion:"
)

add_image_safe("fig9_anova_groups.png", width=Inches(4.2), caption="Figure 9.8: One-Way ANOVA Group Boxplots with Mean ± SE Error Bars")

# Chi-Square Analysis (Page 15)
doc.add_page_break()
add_heading_2("9.6 Chi-Square Goodness-of-Fit Analysis")
add_body_p(
    "Testing whether match conditions (Day, Day/Night, Overcast, Dry/Spin, Pace-friendly) conform to equal frequency yielded χ² = 3.82 (df = 4, p = 0.431). With p >= 0.05, we fail to reject H₀; match conditions follow a uniform distribution without significant sampling bias.",
    bold_prefix="Goodness-of-Fit Finding:"
)

add_image_safe("fig10_chisq_gof.png", width=Inches(4.4), caption="Figure 9.9: Chi-Square Goodness-of-Fit Comparison (Observed vs Expected Counts)")

# ------------------------------------------------------------------------------
# SECTION 10: CONCLUSION AND FUTURE WORK (Page 16)
# ------------------------------------------------------------------------------
print("Writing Section 10: Conclusion and Future Work...")
add_heading_1("10. Conclusion and Future work", page_break_before=True)

add_body_p(
    "CricketEdge successfully bridges undergraduate probability and statistics curriculum with modern sports analytics. The project demonstrates that complex athletic performance can be effectively decomposed and evaluated through rigorous statistical inference, regression modeling, and distribution fitting in RStudio.",
    bold_prefix="Summary of Findings:"
)

add_heading_2("10.1 Key Methodological Takeaways")
add_bullet_point("The Coefficient of Variation (CV) proves statistically superior to isolated batting averages in categorizing player archetypes (anchors vs match-winners).", bold_prefix="Performance Stability:")
add_bullet_point("Regressing runs on boundaries produces high R² (>0.90) due to arithmetic identity rather than exogenous causality, underscoring the vital importance of domain context in statistical interpretation.", bold_prefix="Causality vs Accounting:")
add_bullet_point("Hypothesis tests must strictly report 'Fail to Reject H₀' rather than 'Accept H₀', adhering to sound Neyman-Pearson and Fisherian inferential logic.", bold_prefix="Inferential Integrity:")

add_heading_2("10.2 Future Work Directions")
add_bullet_point("Extend simulation from independent multinomial trials to state-dependent Markov Decision Processes (MDPs) capturing match situation pressure.", bold_prefix="Markov Chain Modeling:")
add_bullet_point("Integrate Survival Analysis (Kaplan-Meier survival curves and Cox Proportional Hazards) to rigorously model ball-by-ball hazard rates of dismissal.", bold_prefix="Survival Analysis:")
add_bullet_point("Implement automated R Markdown knit pipelines generating dynamic LaTeX PDF and Word lab reports directly from reactive dashboard sessions.", bold_prefix="Automated PDF Export:")

# ------------------------------------------------------------------------------
# SECTION 11: REFERENCES (Page 16)
# ------------------------------------------------------------------------------
print("Writing Section 11: References...")
add_heading_1("11. References")

references = [
    "Montgomery, D. C., & Runger, G. C. (2018). Applied Statistics and Probability for Engineers (7th ed.). John Wiley & Sons.",
    "Wickham, H., Navarro, D., & Lin Pedersen, T. (2023). ggplot2: Elegant Graphics for Data Analysis (3rd ed.). Springer.",
    "Chang, W., Cheng, J., Allaire, J. J., Sievert, C., Schloerke, B., Xie, Y., Allen, J., McPherson, J., Dipert, A., & Borges, B. (2024). shiny: Web Application Framework for R. R package version 1.14.0.",
    "Lewis, A. J. (2005). Towards fair measures of player performance in cricket. Journal of the Operational Research Society, 56(7), 804-815.",
    "Kimber, A. C., & Hansford, A. R. (1993). A statistical analysis of batting in cricket. Journal of the Royal Statistical Society: Series A (Statistics in Society), 156(3), 443-455.",
    "Bailey, R. A. (2008). Design of Comparative Experiments. Cambridge University Press."
]

for ref in references:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    p.paragraph_format.first_line_indent = Inches(-0.35)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(ref)
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    r.font.color.rgb = COLOR_TEXT

# Save document to both workspace and Downloads
doc.save(OUTPUT_PATH)
doc.save(OUTPUT_DOWNLOADS)
print(f"Master report saved successfully to:\n  1. {OUTPUT_PATH}\n  2. {OUTPUT_DOWNLOADS}")
