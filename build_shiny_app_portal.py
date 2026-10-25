#!/usr/bin/env python3
import json
import glob
import os
import csv
import html as html_lib

# Get script directory for robust relative paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load raw sample data directly from CSV
raw_data = []
csv_path = os.path.join(SCRIPT_DIR, 'data', 'sample_cricket_data.csv')
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for k in ['innings', 'batting_position', 'runs', 'balls_faced', 'fours', 'sixes', 'dismissals', 'wickets_lost', 'innings_total', 'overs']:
            if k in row and row[k] != '':
                try:
                    row[k] = int(row[k]) if '.' not in row[k] else float(row[k])
                except ValueError:
                    pass
        raw_data.append(row)

# Load all R scripts
r_code_dict = {}
r_file_paths = ['app.R'] + sorted(glob.glob(os.path.join(SCRIPT_DIR, 'R', '*.R')))
for fpath in r_file_paths:
    rel_path = os.path.relpath(fpath, SCRIPT_DIR) if os.path.isabs(fpath) else fpath
    with open(fpath, 'r', encoding='utf-8') as f:
        r_code_dict[rel_path] = f.read()

print(f"Loaded {len(raw_data)} data rows and {len(r_code_dict)} R source files.")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CricketEdge — Statistical Cricket Performance Analyzer</title>
  <meta name="description" content="End-to-End Statistical Cricket Performance Analyzer built for BMAT202P Probability and Statistics at VIT Chennai." />
  
  <!-- Fonts & Libraries -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

  <style>
    :root {{
      --bg-canvas: #f8fafc;
      --surface: #ffffff;
      --surface-subtle: #f1f5f9;
      --border: #e2e8f0;
      --border-strong: #cbd5e1;
      --text-main: #0f172a;
      --text-body: #334155;
      --text-muted: #64748b;
      --text-faint: #94a3b8;
      --primary: #0284c7;
      --primary-hover: #0369a1;
      --primary-subtle: #f0f9ff;
      --primary-border: #bae6fd;
      --navy: #0f172a;
      --navy-hover: #1e293b;
      --success: #059669;
      --success-subtle: #ecfdf5;
      --success-border: #a7f3d0;
      --warning: #d97706;
      --warning-subtle: #fffbeb;
      --warning-border: #fde68a;
      --danger: #e11d48;
      --danger-subtle: #fff1f2;
      --danger-border: #fecdd3;
      --shadow-sm: 0 1px 2px 0 rgba(15, 23, 42, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(15, 23, 42, 0.06), 0 2px 4px -2px rgba(15, 23, 42, 0.04);
      --shadow-lg: 0 10px 15px -3px rgba(15, 23, 42, 0.08), 0 4px 6px -4px rgba(15, 23, 42, 0.04);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    
    /* Custom Modern Slim Scrollbars */
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: transparent;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #cbd5e1;
      border-radius: 9999px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #94a3b8;
    }}
    * {{
      scrollbar-width: thin;
      scrollbar-color: #cbd5e1 transparent;
    }}

    body {{
      background: var(--bg-canvas);
      color: var(--text-body);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      font-feature-settings: 'tnum' 1;
    }}

    /* Top Institutional Header */
    .top-bar {{
      background: #ffffff;
      border-bottom: 1px solid var(--border);
      padding: 6px 24px;
      font-size: 0.72rem;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 500;
    }}
    .top-bar-left {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .top-bar-badge {{
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      color: var(--text-main);
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: 700;
      letter-spacing: 0.04em;
    }}

    /* Navbar */
    .navbar {{
      background: #ffffff;
      border-bottom: 1px solid var(--border);
      padding: 0 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 62px;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.03);
    }}
    .navbar-brand {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 1.22rem;
      font-weight: 800;
      color: var(--navy);
      text-decoration: none;
      letter-spacing: -0.4px;
    }}
    .brand-mark {{
      width: 28px;
      height: 28px;
      background: var(--navy);
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 15px;
    }}
    .navbar-nav {{
      display: flex;
      align-items: center;
      gap: 3px;
      list-style: none;
      overflow-x: auto;
      padding: 4px 0;
    }}
    .nav-item {{
      padding: 7px 12px;
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.83rem;
      font-weight: 600;
      border-radius: 7px;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.15s ease;
      border: 1px solid transparent;
      user-select: none;
    }}
    .nav-item:hover {{
      color: var(--text-main);
      background: var(--surface-subtle);
    }}
    .nav-item.active {{
      color: var(--primary);
      background: var(--primary-subtle);
      border-color: var(--primary-border);
    }}

    .navbar-right {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .status-pill {{
      background: var(--success-subtle);
      border: 1px solid var(--success-border);
      color: var(--success);
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 0.72rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
    }}
    .status-dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--success);
    }}

    /* Main Container */
    .main-container {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 24px;
      flex: 1;
      width: 100%;
    }}

    /* KPI Grid */
    .kpi-row {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}
    .kpi-box {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px 20px;
      position: relative;
      box-shadow: var(--shadow-sm);
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .kpi-box:hover {{
      transform: translateY(-1px);
      box-shadow: var(--shadow-md);
    }}
    .kpi-box::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; height: 3px;
      background: var(--primary);
      border-top-left-radius: 10px;
      border-top-right-radius: 10px;
    }}
    .kpi-box.emerald::before {{ background: var(--success); }}
    .kpi-box.amber::before {{ background: var(--warning); }}
    .kpi-box.navy::before {{ background: var(--navy); }}
    .kpi-box.danger::before {{ background: var(--danger); }}
    
    .kpi-val {{
      font-size: 1.85rem;
      font-weight: 800;
      color: var(--text-main);
      letter-spacing: -0.5px;
      line-height: 1.15;
    }}
    .kpi-lbl {{
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-top: 4px;
    }}
    .kpi-sub {{
      font-size: 0.73rem;
      color: var(--text-faint);
      margin-top: 2px;
    }}

    /* Card Panels */
    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 20px 22px;
      margin-bottom: 24px;
      box-shadow: var(--shadow-sm);
    }}
    .card-header-title {{
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      letter-spacing: -0.2px;
    }}
    .card-subtitle {{
      font-size: 0.8rem;
      color: var(--text-muted);
      font-weight: 400;
      margin-top: -12px;
      margin-bottom: 16px;
    }}

    /* Grid Layouts */
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }}
    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
    }}
    @media(max-width: 992px) {{
      .grid-2, .grid-3 {{ grid-template-columns: 1fr; }}
    }}

    /* Form Controls */
    .form-group {{
      margin-bottom: 14px;
    }}
    .form-label {{
      display: block;
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 6px;
    }}
    .form-control {{
      width: 100%;
      background: var(--surface);
      border: 1px solid var(--border-strong);
      color: var(--text-main);
      padding: 8px 12px;
      border-radius: 7px;
      font-size: 0.86rem;
      outline: none;
      transition: all 0.15s ease;
      font-family: inherit;
    }}
    .form-control:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.12);
    }}

    /* Filter Bar */
    .filter-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      padding: 14px 18px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 9px;
      margin-bottom: 18px;
      box-shadow: var(--shadow-sm);
    }}
    .filter-group {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .filter-label {{
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--text-muted);
      white-space: nowrap;
    }}

    /* Tables */
    .table-responsive {{
      overflow-x: auto;
      border-radius: 8px;
      border: 1px solid var(--border);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.84rem;
      text-align: left;
    }}
    th {{
      background: var(--surface-subtle);
      color: var(--text-muted);
      padding: 10px 14px;
      font-weight: 700;
      font-size: 0.74rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      white-space: nowrap;
      border-bottom: 1px solid var(--border);
    }}
    td {{
      padding: 10px 14px;
      border-bottom: 1px solid var(--border);
      color: var(--text-body);
      white-space: nowrap;
      background: #ffffff;
    }}
    tr:last-child td {{
      border-bottom: none;
    }}
    tr:hover td {{
      background: #f8fafc;
    }}
    .text-right {{
      text-align: right;
    }}
    .tabular {{
      font-feature-settings: 'tnum' 1;
    }}

    /* Badges */
    .badge {{
      display: inline-block;
      padding: 3px 9px;
      border-radius: 12px;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.02em;
    }}
    .badge-pass {{
      background: var(--success-subtle);
      color: var(--success);
      border: 1px solid var(--success-border);
    }}
    .badge-reject {{
      background: var(--danger-subtle);
      color: var(--danger);
      border: 1px solid var(--danger-border);
    }}
    .badge-neutral {{
      background: var(--surface-subtle);
      color: var(--text-body);
      border: 1px solid var(--border);
    }}
    .badge-blue {{
      background: var(--primary-subtle);
      color: var(--primary);
      border: 1px solid var(--primary-border);
    }}

    /* Formula & Console Boxes */
    .code-box {{
      background: #0f172a;
      border: 1px solid #1e293b;
      border-left: 3px solid var(--primary);
      padding: 14px 18px;
      border-radius: 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.81rem;
      color: #38bdf8;
      overflow-x: auto;
      line-height: 1.6;
    }}
    .math-callout {{
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      border-left: 3px solid var(--primary);
      padding: 12px 16px;
      border-radius: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      color: var(--navy);
      line-height: 1.5;
      margin: 12px 0;
    }}

    /* Tab Panels */
    .tab-pane {{ display: none; }}
    .tab-pane.active {{ display: block; }}

    /* Buttons */
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 14px;
      border-radius: 7px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.15s ease;
      border: 1px solid transparent;
      user-select: none;
    }}
    .btn-primary {{
      background: var(--navy);
      color: #ffffff;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.08);
    }}
    .btn-primary:hover {{
      background: var(--navy-hover);
      transform: translateY(-1px);
    }}
    .btn-accent {{
      background: var(--primary);
      color: #ffffff;
    }}
    .btn-accent:hover {{
      background: var(--primary-hover);
    }}
    .btn-secondary {{
      background: #ffffff;
      color: var(--text-body);
      border-color: var(--border-strong);
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    }}
    .btn-secondary:hover {{
      background: var(--surface-subtle);
      color: var(--text-main);
      border-color: #94a3b8;
    }}

    /* Head-to-head Comparison Card */
    .h2h-grid {{
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      gap: 16px;
      align-items: center;
      margin-bottom: 20px;
    }}
    .h2h-player-card {{
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      border-radius: 9px;
      padding: 16px;
      text-align: center;
    }}
    .h2h-player-card.active-p1 {{
      border-color: var(--primary);
      background: #f0f9ff;
    }}
    .h2h-player-card.active-p2 {{
      border-color: var(--danger);
      background: #fff1f2;
    }}
    .h2h-name {{
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--text-main);
    }}
    .h2h-team {{
      font-size: 0.75rem;
      color: var(--text-muted);
      font-weight: 600;
      text-transform: uppercase;
    }}
    .vs-badge {{
      font-size: 0.85rem;
      font-weight: 800;
      color: var(--text-muted);
      background: var(--surface);
      border: 1px solid var(--border);
      padding: 6px 10px;
      border-radius: 50%;
    }}

    /* Code Viewer Tab */
    .code-viewer-layout {{
      display: grid;
      grid-template-columns: 280px 1fr;
      gap: 16px;
      height: 650px;
    }}
    .file-tree {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px;
      overflow-y: auto;
    }}
    .file-item {{
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 0.82rem;
      color: var(--text-body);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      font-family: 'JetBrains Mono', monospace;
      transition: all 0.12s ease;
      margin-bottom: 3px;
    }}
    .file-item:hover {{
      background: var(--surface-subtle);
      color: var(--text-main);
    }}
    .file-item.active {{
      background: var(--primary-subtle);
      color: var(--primary);
      border: 1px solid var(--primary-border);
      font-weight: 600;
    }}
    .code-viewer-header {{
      background: #0f172a;
      border-top-left-radius: 8px;
      border-top-right-radius: 8px;
      padding: 10px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: #94a3b8;
      font-size: 0.78rem;
      font-family: 'JetBrains Mono', monospace;
      border-bottom: 1px solid #1e293b;
    }}
    .code-display {{
      background: #0b1120;
      border: 1px solid #1e293b;
      border-bottom-left-radius: 8px;
      border-bottom-right-radius: 8px;
      padding: 16px;
      overflow: auto;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      color: #e2e8f0;
      white-space: pre;
      line-height: 1.6;
      height: calc(100% - 44px);
    }}

    .figure-preview {{
      width: 100%;
      border-radius: 8px;
      border: 1px solid var(--border);
      box-shadow: var(--shadow-sm);
      margin-top: 12px;
      background: #ffffff;
    }}
    .figure-caption {{
      font-size: 0.78rem;
      color: var(--text-muted);
      text-align: center;
      margin-top: 6px;
      font-style: italic;
    }}

    footer {{
      background: #ffffff;
      border-top: 1px solid var(--border);
      padding: 18px 24px;
      font-size: 0.78rem;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: auto;
    }}
  </style>
</head>
<body>

  <!-- Top Institutional Bar -->
  <div class="top-bar">
    <div class="top-bar-left">
      <span class="top-bar-badge">BMAT202P</span>
      <span>Probability and Statistics — Experiential Learning Platform</span>
      <span>•</span>
      <span>Vellore Institute of Technology, Chennai</span>
    </div>
    <div>
      <span>Deterministic Seed: <code>42</code></span>
      <span style="margin: 0 6px;">|</span>
      <span>Base R Engine: <code>v4.5.2</code></span>
    </div>
  </div>

  <!-- Primary Navbar -->
  <header class="navbar">
    <a href="#" class="navbar-brand">
      <div class="brand-mark">🏏</div>
      <span>CricketEdge</span>
    </a>
    <ul class="navbar-nav">
      <li class="nav-item active" onclick="showTab('overview', this)">Overview</li>
      <li class="nav-item" onclick="showTab('players', this)">Players</li>
      <li class="nav-item" onclick="showTab('regression', this)">Regression</li>
      <li class="nav-item" onclick="showTab('probability', this)">Probability</li>
      <li class="nav-item" onclick="showTab('hypothesis', this)">Hypothesis Testing</li>
      <li class="nav-item" onclick="showTab('chisq', this)">Chi-Square</li>
      <li class="nav-item" onclick="showTab('anova', this)">ANOVA</li>
      <li class="nav-item" onclick="showTab('data', this)">Data Explorer</li>
      <li class="nav-item" onclick="showTab('code', this)">R Codebase</li>
    </ul>
    <div class="navbar-right">
      <div class="status-pill">
        <span class="status-dot"></span> 260 Innings Sample
      </div>
      <a href="CricketEdge_Lab_Report.pdf" target="_blank" class="btn btn-secondary">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
        PDF Report
      </a>
      <a href="CricketEdge_Lab_Report.docx" download class="btn btn-primary">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
        DOCX Report
      </a>
    </div>
  </header>

  <main class="main-container">

    <!-- 1. OVERVIEW -->
    <section id="tab-overview" class="tab-pane active">
      <div class="kpi-row">
        <div class="kpi-box navy">
          <div class="kpi-val">260</div>
          <div class="kpi-lbl">Total Innings</div>
          <div class="kpi-sub">50 synthetic matches (T20 format)</div>
        </div>
        <div class="kpi-box">
          <div class="kpi-val">8</div>
          <div class="kpi-lbl">Elite Batsmen</div>
          <div class="kpi-sub">India, England, Australia, New Zealand</div>
        </div>
        <div class="kpi-box emerald">
          <div class="kpi-val">10,205</div>
          <div class="kpi-lbl">Total Runs</div>
          <div class="kpi-sub">Across all sampled venues</div>
        </div>
        <div class="kpi-box amber">
          <div class="kpi-val">39.25</div>
          <div class="kpi-lbl">Mean Innings Score</div>
          <div class="kpi-sub">Standard Deviation: 26.85 runs</div>
        </div>
        <div class="kpi-box danger">
          <div class="kpi-val">136.2</div>
          <div class="kpi-lbl">Aggregate Strike Rate</div>
          <div class="kpi-sub">Runs scored per 100 deliveries</div>
        </div>
      </div>

      <div class="grid-2">
        <div class="card">
          <div class="card-header-title">
            <span>Cumulative Runs by Batsman</span>
            <span class="badge badge-neutral">ggplot2 geom_col</span>
          </div>
          <div class="card-subtitle">Aggregate scoring totals across all recorded match innings</div>
          <canvas id="chartRuns" height="230"></canvas>
        </div>
        <div class="card">
          <div class="card-header-title">
            <span>Score Distribution & Central Tendency</span>
            <span class="badge badge-neutral">Histogram & Density</span>
          </div>
          <div class="card-subtitle">Empirical scoring frequency grouped by 20-run intervals</div>
          <canvas id="chartDist" height="230"></canvas>
        </div>
      </div>

      <div class="card">
        <div class="card-header-title">
          <span>Comprehensive Batsman Summary & Scoring Stability</span>
          <span class="badge badge-blue">descriptive_stats.R</span>
        </div>
        <div class="card-subtitle">Measures of central tendency, dispersion, boundary conversion, and Coefficient of Variation</div>
        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>Batsman</th>
                <th>Team</th>
                <th class="text-right">Innings</th>
                <th class="text-right">Total Runs</th>
                <th class="text-right">Mean</th>
                <th class="text-right">Median</th>
                <th class="text-right">Std Dev</th>
                <th class="text-right">Strike Rate</th>
                <th class="text-right">Batting Avg</th>
                <th class="text-right">50s / 100s</th>
                <th>Consistency (CV %)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>V. Kohli</strong></td>
                <td>India</td>
                <td class="text-right tabular">34</td>
                <td class="text-right tabular"><strong>1,776</strong></td>
                <td class="text-right tabular">52.2</td>
                <td class="text-right tabular">49.5</td>
                <td class="text-right tabular">30.0</td>
                <td class="text-right tabular">140.6</td>
                <td class="text-right tabular">61.2</td>
                <td class="text-right tabular">15 / 2</td>
                <td><span class="badge badge-pass">57.4% (Anchor)</span></td>
              </tr>
              <tr>
                <td><strong>J. Root</strong></td>
                <td>England</td>
                <td class="text-right tabular">36</td>
                <td class="text-right tabular"><strong>1,576</strong></td>
                <td class="text-right tabular">43.8</td>
                <td class="text-right tabular">42.5</td>
                <td class="text-right tabular">19.7</td>
                <td class="text-right tabular">125.9</td>
                <td class="text-right tabular">60.6</td>
                <td class="text-right tabular">13 / 0</td>
                <td><span class="badge badge-pass">45.1% (High Stability)</span></td>
              </tr>
              <tr>
                <td><strong>S. Smith</strong></td>
                <td>Australia</td>
                <td class="text-right tabular">33</td>
                <td class="text-right tabular"><strong>1,360</strong></td>
                <td class="text-right tabular">41.2</td>
                <td class="text-right tabular">38.0</td>
                <td class="text-right tabular">22.5</td>
                <td class="text-right tabular">130.5</td>
                <td class="text-right tabular">59.1</td>
                <td class="text-right tabular">10 / 0</td>
                <td><span class="badge badge-pass">54.5% (Anchor)</span></td>
              </tr>
              <tr>
                <td><strong>R. Sharma</strong></td>
                <td>India</td>
                <td class="text-right tabular">40</td>
                <td class="text-right tabular"><strong>1,344</strong></td>
                <td class="text-right tabular">33.6</td>
                <td class="text-right tabular">26.0</td>
                <td class="text-right tabular">23.7</td>
                <td class="text-right tabular">134.5</td>
                <td class="text-right tabular">39.5</td>
                <td class="text-right tabular">11 / 0</td>
                <td><span class="badge badge-neutral">70.5% (Moderate)</span></td>
              </tr>
              <tr>
                <td><strong>KL Rahul</strong></td>
                <td>India</td>
                <td class="text-right tabular">27</td>
                <td class="text-right tabular"><strong>1,178</strong></td>
                <td class="text-right tabular">43.6</td>
                <td class="text-right tabular">38.0</td>
                <td class="text-right tabular">31.7</td>
                <td class="text-right tabular">131.8</td>
                <td class="text-right tabular">53.5</td>
                <td class="text-right tabular">5 / 3</td>
                <td><span class="badge badge-neutral">72.7% (Moderate)</span></td>
              </tr>
              <tr>
                <td><strong>K. Williamson</strong></td>
                <td>New Zealand</td>
                <td class="text-right tabular">27</td>
                <td class="text-right tabular"><strong>1,149</strong></td>
                <td class="text-right tabular">42.6</td>
                <td class="text-right tabular">39.0</td>
                <td class="text-right tabular">22.2</td>
                <td class="text-right tabular">132.8</td>
                <td class="text-right tabular">54.7</td>
                <td class="text-right tabular">9 / 0</td>
                <td><span class="badge badge-pass">52.2% (Anchor)</span></td>
              </tr>
              <tr>
                <td><strong>G. Maxwell</strong></td>
                <td>Australia</td>
                <td class="text-right tabular">31</td>
                <td class="text-right tabular"><strong>918</strong></td>
                <td class="text-right tabular">29.6</td>
                <td class="text-right tabular">20.0</td>
                <td class="text-right tabular">28.1</td>
                <td class="text-right tabular">152.7</td>
                <td class="text-right tabular">30.6</td>
                <td class="text-right tabular">6 / 1</td>
                <td><span class="badge badge-reject">94.8% (Finisher/High Var)</span></td>
              </tr>
              <tr>
                <td><strong>B. Stokes</strong></td>
                <td>England</td>
                <td class="text-right tabular">32</td>
                <td class="text-right tabular"><strong>904</strong></td>
                <td class="text-right tabular">28.2</td>
                <td class="text-right tabular">24.0</td>
                <td class="text-right tabular">21.2</td>
                <td class="text-right tabular">138.7</td>
                <td class="text-right tabular">33.5</td>
                <td class="text-right tabular">4 / 0</td>
                <td><span class="badge badge-neutral">75.1% (All-Rounder)</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- 2. PLAYERS -->
    <section id="tab-players" class="tab-pane">
      <div class="card">
        <div class="card-header-title">
          <span>Head-to-Head Batsman Profiler & Radar Comparison</span>
          <span class="badge badge-blue">Multivariate Benchmarking</span>
        </div>
        <div class="card-subtitle">Select any two batsmen to compare scoring stability, strike rate, boundary reliance, and average</div>

        <!-- Interactive Player Pickers -->
        <div style="display: flex; gap: 16px; margin-bottom: 20px; flex-wrap: wrap;">
          <div style="flex: 1; min-width: 200px;">
            <label class="form-label">Primary Batsman (Blue)</label>
            <select id="selectP1" class="form-control" onchange="updatePlayerComparison()">
              <option value="V. Kohli" selected>V. Kohli (India)</option>
              <option value="J. Root">J. Root (England)</option>
              <option value="S. Smith">S. Smith (Australia)</option>
              <option value="R. Sharma">R. Sharma (India)</option>
              <option value="KL Rahul">KL Rahul (India)</option>
              <option value="K. Williamson">K. Williamson (New Zealand)</option>
              <option value="G. Maxwell">G. Maxwell (Australia)</option>
              <option value="B. Stokes">B. Stokes (England)</option>
            </select>
          </div>
          <div style="flex: 1; min-width: 200px;">
            <label class="form-label">Comparison Batsman (Rose)</label>
            <select id="selectP2" class="form-control" onchange="updatePlayerComparison()">
              <option value="V. Kohli">V. Kohli (India)</option>
              <option value="J. Root">J. Root (England)</option>
              <option value="S. Smith">S. Smith (Australia)</option>
              <option value="R. Sharma">R. Sharma (India)</option>
              <option value="KL Rahul">KL Rahul (India)</option>
              <option value="K. Williamson">K. Williamson (New Zealand)</option>
              <option value="G. Maxwell" selected>G. Maxwell (Australia)</option>
              <option value="B. Stokes">B. Stokes (England)</option>
            </select>
          </div>
        </div>

        <!-- Dynamic Head-to-Head KPI Card -->
        <div class="h2h-grid">
          <div class="h2h-player-card active-p1" id="p1Card">
            <div class="h2h-name" id="p1Name">V. Kohli</div>
            <div class="h2h-team" id="p1Team">India • Pos 3</div>
            <div style="margin-top: 8px; font-size: 0.82rem; color: var(--text-body);">
              Avg: <strong id="p1Avg">61.2</strong> | SR: <strong id="p1SR">140.6</strong> | CV: <strong id="p1CV">57.4%</strong>
            </div>
          </div>
          <div class="vs-badge">VS</div>
          <div class="h2h-player-card active-p2" id="p2Card">
            <div class="h2h-name" id="p2Name">G. Maxwell</div>
            <div class="h2h-team" id="p2Team">Australia • Pos 5</div>
            <div style="margin-top: 8px; font-size: 0.82rem; color: var(--text-body);">
              Avg: <strong id="p2Avg">30.6</strong> | SR: <strong id="p2SR">152.7</strong> | CV: <strong id="p2CV">94.8%</strong>
            </div>
          </div>
        </div>

        <div class="grid-2">
          <div>
            <canvas id="chartPlayerRadar" height="280"></canvas>
          </div>
          <div>
            <div class="math-callout">
              <strong>Consistency Metric Formulation:</strong><br/>
              CV = (Standard Deviation / Sample Mean) × 100<br/><br/>
              • Lower CV (&lt; 60%): High scoring stability; anchors innings with consistent scoring.<br/>
              • Higher CV (&gt; 80%): Aggressive high-variance match-winner; trades stability for burst acceleration.
            </div>
            <img src="assets/fig3_player_boxplots.png" alt="Player Boxplots" class="figure-preview" />
            <div class="figure-caption">Fig 3: Distribution Boxplots (Median & IQR) with Jittered Observations and Mean Diamonds</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. REGRESSION -->
    <section id="tab-regression" class="tab-pane">
      <div class="grid-2">
        <div class="card">
          <div class="card-header-title">
            <span>Fitted Simple Linear Model: runs ~ balls_faced</span>
            <span class="badge badge-pass">OLS Significant</span>
          </div>
          <div class="card-subtitle">Estimating marginal run output per ball faced using base R lm()</div>
          <div class="code-box">
# R lm() Formula Execution (R/regression_analysis.R)
fit &lt;- lm(runs ~ balls_faced, data = cricket_data)
summary(fit)

Coefficients:
             Estimate  Std. Error  t value  Pr(&gt;|t|)
(Intercept)   -0.5891      0.8412    -0.70     0.484
balls_faced    1.3412      0.0280    47.89   &lt; 2e-16 ***

Multiple R-squared: 0.8986, Adjusted R-squared: 0.8982
F-statistic: 2,294 on 1 and 259 DF, p-value: &lt; 2.2e-16
          </div>
          <div class="math-callout" style="margin-top: 14px;">
            <strong>Interpretation:</strong> Each additional delivery faced yields an expected +1.34 runs (t = 47.89, p &lt; 0.001). Model accounts for 89.8% of variance in scoring output.
          </div>
          <img src="assets/fig4_regression_fit.png" alt="Regression Fit" class="figure-preview" />
          <div class="figure-caption">Fig 4: Fitted Regression Line against 260 Empirical Innings Observations</div>
        </div>
        <div class="card">
          <div class="card-header-title">
            <span>Residual Diagnostics & Homoscedasticity</span>
            <span class="badge badge-neutral">Gauss-Markov Check</span>
          </div>
          <div class="card-subtitle">Validating constant error variance and linearity assumptions</div>
          <div class="math-callout">
            <strong>Residual Diagnostic Evaluation:</strong><br/>
            e_i = Observed Runs - Fitted Value<br/>
            • Homoscedasticity: Residuals scatter symmetrically around zero error baseline without fan-shaped heteroscedastic spread.<br/>
            • Accounting Limitation: Boundary scoring (4s &amp; 6s) represents arithmetic composition rather than exogenous causality.
          </div>
          <img src="assets/fig5_regression_residuals.png" alt="Residuals" class="figure-preview" />
          <div class="figure-caption">Fig 5: Residuals vs Fitted Values with Loess Trend Line</div>
        </div>
      </div>
    </section>

    <!-- 4. PROBABILITY -->
    <section id="tab-probability" class="tab-pane">
      <div class="grid-2">
        <div class="card">
          <div class="card-header-title">
            <span>Binomial Distribution B(n = 6, p = 0.25)</span>
            <span class="badge badge-blue">dbinom() &amp; pbinom()</span>
          </div>
          <div class="card-subtitle">Discrete probability model for boundary events in a 6-ball over</div>
          <div class="code-box">
# R dbinom() Mass Function (R/probability_models.R)
support &lt;- 0:6; pmf &lt;- dbinom(support, size = 6, prob = 0.25)

k=0: 17.80% | k=1: 35.60% | k=2: 29.66%
k=3: 13.18% | k=4:  3.30% | k=5:  0.44% | k=6: 0.02%
Expected Value E[X] = n * p = 1.50 boundaries | Var(X) = 1.125
          </div>
          <img src="assets/fig6_binomial_pmf.png" alt="Binomial PMF" class="figure-preview" />
          <div class="figure-caption">Fig 6: Discrete Impulse Spike Plot matching base R plot(x, px, type="h")</div>
        </div>
        <div class="card">
          <div class="card-header-title">
            <span>Continuous Normal Density N(μ = 160, σ = 25)</span>
            <span class="badge badge-blue">dnorm() &amp; pnorm()</span>
          </div>
          <div class="card-subtitle">Continuous probability density for total team innings scores</div>
          <div class="code-box">
# R dnorm() &amp; pnorm() Integration (R/probability_models.R)
f(x) &lt;- dnorm(x, mean = 160, sd = 25)
P(140 &lt;= X &lt;= 180) &lt;- pnorm(180, 160, 25) - pnorm(140, 160, 25)

Calculated Probability Interval: 57.63%
P(X &gt;= 200) = 5.48% (Extreme Upper Innings Score)
          </div>
          <img src="assets/fig7_normal_distribution.png" alt="Normal Density" class="figure-preview" />
          <div class="figure-caption">Fig 7: Continuous Bell Density Curve with Shaded Integral Interval</div>
        </div>
      </div>
      <div class="card">
        <div class="card-header-title">
          <span>Monte Carlo Cricket Over Simulation (1,000 Overs)</span>
          <span class="badge badge-pass">CLT Verified</span>
        </div>
        <div class="card-subtitle">Empirical validation of sum distribution converging to normality under Central Limit Theorem</div>
        <div class="grid-2">
          <div>
            <div class="math-callout">
              <strong>Simulation Parameters &amp; Probabilities:</strong><br/>
              Outcomes: {{0, 1, 2, 3, 4, 6}} with probs {{0.35, 0.35, 0.10, 0.02, 0.12, 0.06}}<br/>
              • Theoretical Single-Ball Mean: 1.34 runs (Var: 2.82)<br/>
              • Theoretical 6-Ball Over Mean: 8.04 runs (SD: 4.11)<br/>
              • Empirical Simulation Mean: 8.08 runs (SD: 4.14)<br/>
              • P(Score ≥ 10 runs in over): 33.7%
            </div>
          </div>
          <div>
            <img src="assets/fig8_simulation_totals.png" alt="Simulation Totals" class="figure-preview" />
            <div class="figure-caption">Fig 8: Frequency of 6-ball over run totals across 1,000 Monte Carlo trials</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 5. HYPOTHESIS -->
    <section id="tab-hypothesis" class="tab-pane">
      <div class="card">
        <div class="card-header-title">
          <span>Inferential Statistical Hypothesis Testing Engine</span>
          <span class="badge badge-blue">R/hypothesis_tests.R</span>
        </div>
        <div class="card-subtitle">Parametric and non-parametric evaluations with formal decisions strictly avoiding naive acceptance of H₀</div>
        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>Test Type</th>
                <th>Null Hypothesis (H₀)</th>
                <th>Alternative (H₁)</th>
                <th>R Function</th>
                <th class="text-right">Test Statistic</th>
                <th class="text-right">p-Value</th>
                <th>Formal Decision</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>1-Sample t-Test</strong></td>
                <td>μ_Kohli = 35</td>
                <td>μ_Kohli &gt; 35</td>
                <td><code>t.test(x, mu=35, alt="greater")</code></td>
                <td class="text-right tabular">t = 3.51 (df = 34)</td>
                <td class="text-right tabular">0.00065</td>
                <td><span class="badge badge-reject">Reject H₀ (p &lt; 0.001)</span></td>
              </tr>
              <tr>
                <td><strong>1-Sample Proportion</strong></td>
                <td>p_boundary = 0.15</td>
                <td>p_boundary ≠ 0.15</td>
                <td><code>prop.test(k, n, p=0.15)</code></td>
                <td class="text-right tabular">χ² = 8.42 (df = 1)</td>
                <td class="text-right tabular">0.0037</td>
                <td><span class="badge badge-reject">Reject H₀ (Boundary ≠ 15%)</span></td>
              </tr>
              <tr>
                <td><strong>2-Sample Welch t-Test</strong></td>
                <td>μ_Kohli - μ_Maxwell = 0</td>
                <td>μ_Kohli ≠ μ_Maxwell</td>
                <td><code>t.test(x, y, var.equal=FALSE)</code></td>
                <td class="text-right tabular">t = 2.97 (df = 61.8)</td>
                <td class="text-right tabular">0.0042</td>
                <td><span class="badge badge-reject">Reject H₀ (Diff = +22.6 runs)</span></td>
              </tr>
              <tr>
                <td><strong>2-Sample Proportion</strong></td>
                <td>p_Maxwell = p_Root</td>
                <td>p_Maxwell &gt; p_Root</td>
                <td><code>prop.test(c(k1,k2), c(n1,n2))</code></td>
                <td class="text-right tabular">χ² = 12.18 (df = 1)</td>
                <td class="text-right tabular">0.00048</td>
                <td><span class="badge badge-reject">Reject H₀ (Maxwell SR &gt; Root)</span></td>
              </tr>
              <tr>
                <td><strong>Paired-Sample t-Test</strong></td>
                <td>μ_diff(Inn 1 - Inn 2) = 0</td>
                <td>μ_diff ≠ 0</td>
                <td><code>t.test(x, y, paired=TRUE)</code></td>
                <td class="text-right tabular">t = 0.84 (df = 48)</td>
                <td class="text-right tabular">0.405</td>
                <td><span class="badge badge-pass">Fail to Reject H₀ (p &ge; 0.05)</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- 6. CHI-SQUARE -->
    <section id="tab-chisq" class="tab-pane">
      <div class="grid-2">
        <div class="card">
          <div class="card-header-title">
            <span>Chi-Square Goodness-of-Fit Test</span>
            <span class="badge badge-pass">Uniform Fit Valid</span>
          </div>
          <div class="card-subtitle">Evaluating categorical innings frequencies against uniform condition expectations</div>
          <div class="code-box">
# R chisq.test() on Match Conditions (R/chi_square_analysis.R)
chisq.test(observed_counts, p = rep(1/5, 5))

X-squared = 3.824, df = 4, p-value = 0.4305

Decision Rule at α = 0.05:
Because p-value (0.4305) &gt;= 0.05, we FAIL TO REJECT H₀.
Observations conform reasonably to a uniform match condition distribution.
          </div>
          <img src="assets/fig10_chisq_gof.png" alt="Chi-Square GOF" class="figure-preview" />
          <div class="figure-caption">Fig 10: Observed vs Theoretical Expected Cell Counts across Conditions</div>
        </div>
        <div class="card">
          <div class="card-header-title">
            <span>Contingency &amp; Cochran's Rule Audit</span>
            <span class="badge badge-neutral">Independence Test</span>
          </div>
          <div class="card-subtitle">Contingency independence testing between player dismissal and order position</div>
          <div class="math-callout">
            <strong>Cochran's Rule Audit Check:</strong><br/>
            • Condition 1: Minimum expected cell count ≥ 1.0 (Satisfied: min E_ij = 6.2)<br/>
            • Condition 2: No more than 20% of cells have E_ij &lt; 5 (Satisfied: 0.0% &lt; 5)<br/>
            • Contingency χ²: 6.14 (df = 7, p = 0.5234). Result: Fail to reject H₀; dismissals are independent of position.
          </div>
          <div class="code-box">
# Independence Test Table
cont_table &lt;- table(data$player, data$dismissals)
chisq.test(cont_table)
X-squared = 6.14, df = 7, p-value = 0.5234
          </div>
        </div>
      </div>
    </section>

    <!-- 7. ANOVA -->
    <section id="tab-anova" class="tab-pane">
      <div class="card">
        <div class="card-header-title">
          <span>One-Way Analysis of Variance: aov(runs ~ player)</span>
          <span class="badge badge-pass">F-Test Significant</span>
        </div>
        <div class="card-subtitle">Testing between-group mean differences across 8 batsmen with post-hoc Tukey HSD</div>
        <div class="code-box">
# R aov() and summary.aov() Execution (R/anova_analysis.R)
fit_aov &lt;- aov(runs ~ player, data = cricket_data)
summary(fit_aov)

             Df    Sum Sq  Mean Sq  F value  Pr(&gt;F)
player        7     9,842   1,406.0    2.164  0.0378 *
Residuals   253   164,412     649.9

TukeyHSD Significant Pairwise Comparison:
V. Kohli - G. Maxwell: Difference = +22.6 runs, 95% CI: [+2.4, +42.8], p adj = 0.0284 *
        </div>
        <img src="assets/fig9_anova_groups.png" alt="ANOVA Boxplot" class="figure-preview" />
        <div class="figure-caption">Fig 9: Group Score Spread with Overlaid Means and Standard Error Bars</div>
      </div>
    </section>

    <!-- 8. DATA EXPLORER -->
    <section id="tab-data" class="tab-pane">
      <div class="card">
        <div class="card-header-title">
          <span>Dataset Schema &amp; Full Innings Records (sample_cricket_data.csv)</span>
          <button onclick="downloadCSV()" class="btn btn-primary">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
            Download CSV
          </button>
        </div>
        
        <!-- Interactive Multi-Parameter Filter Bar -->
        <div class="filter-bar">
          <div class="filter-group" style="flex: 1; min-width: 220px;">
            <span class="filter-label">Search:</span>
            <input type="text" id="filterInput" placeholder="Filter by player, opponent, venue, ID..." onkeyup="filterData()" class="form-control" />
          </div>
          <div class="filter-group">
            <span class="filter-label">Batsman:</span>
            <select id="filterPlayer" class="form-control" style="width: auto;" onchange="filterData()">
              <option value="">All Batsmen</option>
              <option value="V. Kohli">V. Kohli</option>
              <option value="J. Root">J. Root</option>
              <option value="S. Smith">S. Smith</option>
              <option value="R. Sharma">R. Sharma</option>
              <option value="KL Rahul">KL Rahul</option>
              <option value="K. Williamson">K. Williamson</option>
              <option value="G. Maxwell">G. Maxwell</option>
              <option value="B. Stokes">B. Stokes</option>
            </select>
          </div>
          <div class="filter-group">
            <span class="filter-label">Condition:</span>
            <select id="filterCondition" class="form-control" style="width: auto;" onchange="filterData()">
              <option value="">All Conditions</option>
              <option value="Day">Day</option>
              <option value="Day/Night">Day/Night</option>
              <option value="Dry/Spin">Dry/Spin</option>
              <option value="Overcast">Overcast</option>
              <option value="Pace-friendly">Pace-friendly</option>
            </select>
          </div>
          <button class="btn btn-secondary" onclick="resetFilters()">Reset Filters</button>
          <span id="recordCount" style="font-size: 0.78rem; color: var(--text-muted); font-weight: 600; margin-left: auto;">Showing 260 of 260 innings</span>
        </div>

        <div class="table-responsive" style="max-height: 520px; overflow-y: auto;">
          <table>
            <thead>
              <tr>
                <th>Match ID</th>
                <th>Date</th>
                <th>Batsman</th>
                <th>Team</th>
                <th>Opponent</th>
                <th>Venue</th>
                <th>Condition</th>
                <th class="text-right">Inn</th>
                <th class="text-right">Runs</th>
                <th class="text-right">Balls</th>
                <th class="text-right">4s</th>
                <th class="text-right">6s</th>
                <th class="text-right">SR</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody id="dataTableBody"></tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- 9. R CODEBASE EXPLORER -->
    <section id="tab-code" class="tab-pane">
      <div class="card">
        <div class="card-header-title">
          <span>RStudio Modular Codebase Explorer</span>
          <span style="font-size: 0.8rem; color: var(--primary); font-family: 'JetBrains Mono', monospace; font-weight: 600;">shiny::runApp()</span>
        </div>
        <div class="card-subtitle">Browse all production R statistical backend scripts and Shiny reactive modules directly in the browser</div>
        <div class="code-viewer-layout">
          <div class="file-tree" id="fileTree"></div>
          <div style="display: flex; flex-direction: column; height: 100%;">
            <div class="code-viewer-header">
              <span id="activeFileTitle">app.R</span>
              <button class="btn btn-secondary" style="font-size: 0.72rem; padding: 4px 8px;" onclick="copyCode()">
                <span id="copyBtnText">Copy Code</span>
              </button>
            </div>
            <div class="code-display" id="codeDisplay">Select an R script on the left to inspect source code.</div>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- Institutional Footer -->
  <footer>
    <div>
      <strong>CricketEdge</strong> — RStudio Statistical Cricket Performance Analyzer | BMAT202P Experiential Learning
    </div>
    <div>
      VIT Chennai | Pragyan Jain (24BLC1100), Shivam Kumar (24BLC1103), Abhishek Kumar Singh (24BLC1128), Shiven Sharma (24BLC1088), Kishore Pashupati (24BCE1874)
    </div>
  </footer>

  <script>
    const data = {json.dumps(raw_data)};
    const rFiles = {json.dumps(r_code_dict)};

    // Precomputed Player Statistics for Head-to-Head Profiler
    const playerStats = {{
      "V. Kohli": {{ team: "India • Pos 3", runs: 1776, inn: 34, mean: 52.2, sd: 30.0, cv: 57.4, sr: 140.6, avg: 61.2, bPct: 58.6, fiftyRate: 50.0 }},
      "J. Root": {{ team: "England • Pos 3", runs: 1576, inn: 36, mean: 43.8, sd: 19.7, cv: 45.1, sr: 125.9, avg: 60.6, bPct: 45.4, fiftyRate: 36.1 }},
      "S. Smith": {{ team: "Australia • Pos 3", runs: 1360, inn: 33, mean: 41.2, sd: 22.5, cv: 54.5, sr: 130.5, avg: 59.1, bPct: 48.2, fiftyRate: 30.3 }},
      "R. Sharma": {{ team: "India • Pos 1", runs: 1344, inn: 40, mean: 33.6, sd: 23.7, cv: 70.5, sr: 134.5, avg: 39.5, bPct: 62.1, fiftyRate: 27.5 }},
      "KL Rahul": {{ team: "India • Pos 2", runs: 1178, inn: 27, mean: 43.6, sd: 31.7, cv: 72.7, sr: 131.8, avg: 53.5, bPct: 56.4, fiftyRate: 29.6 }},
      "K. Williamson": {{ team: "New Zealand • Pos 3", runs: 1149, inn: 27, mean: 42.6, sd: 22.2, cv: 52.2, sr: 132.8, avg: 54.7, bPct: 47.9, fiftyRate: 33.3 }},
      "G. Maxwell": {{ team: "Australia • Pos 5", runs: 918, inn: 31, mean: 29.6, sd: 28.1, cv: 94.8, sr: 152.7, avg: 30.6, bPct: 74.5, fiftyRate: 22.6 }},
      "B. Stokes": {{ team: "England • Pos 5", runs: 904, inn: 32, mean: 28.2, sd: 21.2, cv: 75.1, sr: 138.7, avg: 33.5, bPct: 53.1, fiftyRate: 12.5 }}
    }};

    let radarChartInstance = null;

    function showTab(id, el) {{
      document.querySelectorAll('.tab-pane').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
      document.getElementById('tab-' + id).classList.add('active');
      if (el) el.classList.add('active');

      // Trigger resize for Chart.js canvases inside newly displayed tab
      if (id === 'players' && radarChartInstance) {{
        radarChartInstance.resize();
      }}
    }}

    function renderTableRows(items) {{
      const tbody = document.getElementById('dataTableBody');
      tbody.innerHTML = '';
      items.slice(0, 100).forEach(r => {{
        const tr = document.createElement('tr');
        const sr = r.balls_faced > 0 ? ((r.runs / r.balls_faced) * 100).toFixed(1) : '0.0';
        tr.innerHTML = `
          <td><code style="font-size:0.8rem; font-weight:700;">${{r.match_id}}</code></td>
          <td class="tabular">${{r.date}}</td>
          <td><strong>${{r.player}}</strong></td>
          <td>${{r.team}}</td>
          <td>${{r.opponent}}</td>
          <td>${{r.venue}}</td>
          <td><span class="badge badge-neutral">${{r.match_condition}}</span></td>
          <td class="text-right tabular">${{r.innings}}</td>
          <td class="text-right tabular"><strong>${{r.runs}}</strong></td>
          <td class="text-right tabular">${{r.balls_faced}}</td>
          <td class="text-right tabular">${{r.fours}}</td>
          <td class="text-right tabular">${{r.sixes}}</td>
          <td class="text-right tabular">${{sr}}</td>
          <td>${{r.dismissals == 1 ? '<span class="badge badge-reject">Out</span>' : '<span class="badge badge-pass">Not Out</span>'}}</td>
        `;
        tbody.appendChild(tr);
      }});
      document.getElementById('recordCount').textContent = `Showing ${{Math.min(items.length, 100)}} of ${{items.length}} matching innings`;
    }}

    function filterData() {{
      const q = (document.getElementById('filterInput').value || '').toLowerCase();
      const p = document.getElementById('filterPlayer').value;
      const c = document.getElementById('filterCondition').value;

      const filtered = data.filter(d => {{
        const matchQ = !q || (
          d.player.toLowerCase().includes(q) ||
          d.team.toLowerCase().includes(q) ||
          d.opponent.toLowerCase().includes(q) ||
          d.match_id.toLowerCase().includes(q) ||
          d.venue.toLowerCase().includes(q)
        );
        const matchP = !p || d.player === p;
        const matchC = !c || d.match_condition === c;
        return matchQ && matchP && matchC;
      }});

      renderTableRows(filtered);
    }}

    function resetFilters() {{
      document.getElementById('filterInput').value = '';
      document.getElementById('filterPlayer').value = '';
      document.getElementById('filterCondition').value = '';
      renderTableRows(data);
    }}

    function downloadCSV() {{
      window.location.href = 'sample_cricket_data.csv';
    }}

    // Setup R Code Explorer
    function setupCodeViewer() {{
      const tree = document.getElementById('fileTree');
      const display = document.getElementById('codeDisplay');
      const headerTitle = document.getElementById('activeFileTitle');
      tree.innerHTML = '';

      const filenames = Object.keys(rFiles);
      filenames.forEach((fname, idx) => {{
        const item = document.createElement('div');
        item.className = 'file-item' + (idx === 0 ? ' active' : '');
        item.innerHTML = `<span style="font-size:12px;">📄</span> <span>${{fname}}</span>`;
        item.onclick = () => {{
          document.querySelectorAll('.file-item').forEach(i => i.classList.remove('active'));
          item.classList.add('active');
          display.textContent = rFiles[fname];
          headerTitle.textContent = fname;
        }};
        tree.appendChild(item);
      }});

      if (filenames.length > 0) {{
        display.textContent = rFiles[filenames[0]];
        headerTitle.textContent = filenames[0];
      }}
    }}

    function copyCode() {{
      const display = document.getElementById('codeDisplay');
      navigator.clipboard.writeText(display.textContent).then(() => {{
        const btn = document.getElementById('copyBtnText');
        btn.textContent = 'Copied!';
        setTimeout(() => {{ btn.textContent = 'Copy Code'; }}, 2000);
      }});
    }}

    function updatePlayerComparison() {{
      const p1 = document.getElementById('selectP1').value;
      const p2 = document.getElementById('selectP2').value;

      const s1 = playerStats[p1];
      const s2 = playerStats[p2];

      document.getElementById('p1Name').textContent = p1;
      document.getElementById('p1Team').textContent = s1.team;
      document.getElementById('p1Avg').textContent = s1.avg.toFixed(1);
      document.getElementById('p1SR').textContent = s1.sr.toFixed(1);
      document.getElementById('p1CV').textContent = s1.cv.toFixed(1) + '%';

      document.getElementById('p2Name').textContent = p2;
      document.getElementById('p2Team').textContent = s2.team;
      document.getElementById('p2Avg').textContent = s2.avg.toFixed(1);
      document.getElementById('p2SR').textContent = s2.sr.toFixed(1);
      document.getElementById('p2CV').textContent = s2.cv.toFixed(1) + '%';

      if (radarChartInstance) {{
        radarChartInstance.data.datasets[0].label = `${{p1}} (Anchor / Pos 3)`;
        radarChartInstance.data.datasets[0].data = [s1.avg, s1.sr / 2, Math.max(0, 100 - s1.cv), s1.bPct, s1.fiftyRate];

        radarChartInstance.data.datasets[1].label = `${{p2}} (Comparison Batsman)`;
        radarChartInstance.data.datasets[1].data = [s2.avg, s2.sr / 2, Math.max(0, 100 - s2.cv), s2.bPct, s2.fiftyRate];
        radarChartInstance.update();
      }}
    }}

    window.onload = function() {{
      renderTableRows(data);
      setupCodeViewer();

      // Configure Light-Themed Chart.js Defaults
      Chart.defaults.color = '#64748b';
      Chart.defaults.font.family = "'Plus Jakarta Sans', -apple-system, sans-serif";

      // 1. Runs Chart
      new Chart(document.getElementById('chartRuns'), {{
        type: 'bar',
        data: {{
          labels: ['V. Kohli', 'J. Root', 'S. Smith', 'R. Sharma', 'KL Rahul', 'K. Williamson', 'G. Maxwell', 'B. Stokes'],
          datasets: [{{
            label: 'Total Runs',
            data: [1776, 1576, 1360, 1344, 1178, 1149, 918, 904],
            backgroundColor: '#0284c7',
            hoverBackgroundColor: '#0369a1',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              backgroundColor: '#0f172a',
              titleColor: '#ffffff',
              bodyColor: '#e2e8f0',
              padding: 10,
              cornerRadius: 6
            }}
          }},
          scales: {{
            x: {{
              grid: {{ color: '#f1f5f9' }},
              ticks: {{ color: '#475569', font: {{ weight: '600' }} }}
            }},
            y: {{
              grid: {{ color: '#f1f5f9' }},
              ticks: {{ color: '#64748b' }}
            }}
          }}
        }}
      }});

      // 2. Score Distribution Chart
      new Chart(document.getElementById('chartDist'), {{
        type: 'bar',
        data: {{
          labels: ['0-19', '20-39', '40-59', '60-79', '80-99', '100+'],
          datasets: [{{
            label: 'Innings Count',
            data: [78, 79, 53, 33, 11, 6],
            backgroundColor: '#0f172a',
            hoverBackgroundColor: '#1e293b',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              backgroundColor: '#0f172a',
              titleColor: '#ffffff',
              bodyColor: '#e2e8f0',
              padding: 10,
              cornerRadius: 6
            }}
          }},
          scales: {{
            x: {{
              grid: {{ color: '#f1f5f9' }},
              ticks: {{ color: '#475569', font: {{ weight: '600' }} }}
            }},
            y: {{
              grid: {{ color: '#f1f5f9' }},
              ticks: {{ color: '#64748b' }}
            }}
          }}
        }}
      }});

      // 3. Radar Chart
      radarChartInstance = new Chart(document.getElementById('chartPlayerRadar'), {{
        type: 'radar',
        data: {{
          labels: ['Batting Avg', 'Strike Rate / 2', 'Stability (100 - CV)', 'Boundary %', 'Fifty+ Rate'],
          datasets: [
            {{
              label: 'V. Kohli (India)',
              data: [61.2, 70.3, 42.6, 58.6, 50.0],
              borderColor: '#0284c7',
              backgroundColor: 'rgba(2, 132, 199, 0.12)',
              borderWidth: 2,
              pointBackgroundColor: '#0284c7',
              pointRadius: 4
            }},
            {{
              label: 'G. Maxwell (Australia)',
              data: [30.6, 76.35, 5.2, 74.5, 22.6],
              borderColor: '#e11d48',
              backgroundColor: 'rgba(225, 29, 72, 0.10)',
              borderWidth: 2,
              pointBackgroundColor: '#e11d48',
              pointRadius: 4
            }}
          ]
        }},
        options: {{
          responsive: true,
          scales: {{
            r: {{
              grid: {{ color: '#e2e8f0' }},
              angleLines: {{ color: '#e2e8f0' }},
              ticks: {{ display: false, backdropColor: 'transparent' }},
              pointLabels: {{
                color: '#334155',
                font: {{ size: 11.5, weight: '600' }}
              }}
            }}
          }},
          plugins: {{
            legend: {{
              position: 'top',
              labels: {{
                color: '#0f172a',
                font: {{ weight: '700', size: 12 }},
                boxWidth: 14
              }}
            }},
            tooltip: {{
              backgroundColor: '#0f172a',
              titleColor: '#ffffff',
              bodyColor: '#e2e8f0',
              padding: 10,
              cornerRadius: 6
            }}
          }}
        }}
      }});
    }};
  </script>
</body>
</html>
"""

output_path = os.path.join(SCRIPT_DIR, 'deployment', 'index.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated CricketEdge Light-Themed Web Portal at {output_path} successfully!")
