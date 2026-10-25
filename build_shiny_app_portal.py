#!/usr/bin/env python3
import json
import glob
import os
import csv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load raw sample data from CSV
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
  <meta name="description" content="Applied statistical sports performance analytics platform in R and Shiny for BMAT202P at VIT Chennai." />

  <!-- Typography: Plus Jakarta Sans & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- Chart.js 4.4 -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

  <style>
    :root {{
      --bg-canvas: #f8fafc;
      --surface: #ffffff;
      --surface-subtle: #f1f5f9;
      --surface-muted: #e2e8f0;
      --border: #e2e8f0;
      --border-strong: #cbd5e1;
      --text-main: #0f172a;
      --text-body: #334155;
      --text-muted: #64748b;
      --text-faint: #94a3b8;
      
      --navy: #0f172a;
      --navy-hover: #1e293b;
      --primary: #0284c7;
      --primary-hover: #0369a1;
      --primary-subtle: #f0f9ff;
      --primary-border: #bae6fd;
      
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

    ::selection {{
      background: var(--primary);
      color: #ffffff;
    }}

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
      background-color: var(--bg-canvas);
      color: var(--text-body);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      font-feature-settings: 'tnum' 1;
    }}

    /* Top Academic Header */
    .header-institution {{
      background: #ffffff;
      border-bottom: 1px solid var(--border);
      padding: 7px 24px;
      font-size: 0.73rem;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 500;
    }}
    .header-institution-left {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .tag-course {{
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      color: var(--text-main);
      padding: 1px 7px;
      border-radius: 4px;
      font-weight: 700;
      letter-spacing: 0.03em;
    }}

    /* Navbar */
    .navbar {{
      background: #ffffff;
      border-bottom: 1px solid var(--border);
      padding: 0 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 64px;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.03);
    }}
    .navbar-brand {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--navy);
      text-decoration: none;
      letter-spacing: -0.4px;
    }}
    .brand-mark {{
      width: 32px;
      height: 32px;
      background: var(--navy);
      border-radius: 7px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffffff;
    }}
    .navbar-nav {{
      display: flex;
      align-items: center;
      gap: 2px;
      list-style: none;
      overflow-x: auto;
      padding: 4px 0;
    }}
    .nav-item {{
      padding: 7px 11px;
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.83rem;
      font-weight: 600;
      border-radius: 7px;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 6px;
      user-select: none;
      border: 1px solid transparent;
    }}
    .nav-item svg {{
      width: 15px;
      height: 15px;
      stroke-width: 2;
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
    .status-indicator {{
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
    .btn svg {{
      width: 14px;
      height: 14px;
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

    /* Main Container */
    .main-container {{
      max-width: 1380px;
      margin: 0 auto;
      padding: 24px;
      flex: 1;
      width: 100%;
    }}

    /* Metrics Ribbon (High-Density Analytical Strip) */
    .metrics-ribbon {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 9px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      margin-bottom: 24px;
      box-shadow: var(--shadow-sm);
      overflow: hidden;
    }}
    .metric-cell {{
      padding: 16px 20px;
      border-right: 1px solid var(--border);
    }}
    .metric-cell:last-child {{
      border-right: none;
    }}
    .metric-val {{
      font-size: 1.85rem;
      font-weight: 800;
      color: var(--text-main);
      letter-spacing: -0.5px;
      line-height: 1.1;
      font-variant-numeric: tabular-nums;
    }}
    .metric-lbl {{
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-top: 4px;
    }}
    .metric-sub {{
      font-size: 0.72rem;
      color: var(--text-faint);
      margin-top: 2px;
    }}

    /* Cards */
    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 9px;
      padding: 20px 22px;
      margin-bottom: 24px;
      box-shadow: var(--shadow-sm);
    }}
    .card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
    }}
    .card-title {{
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--text-main);
      letter-spacing: -0.2px;
    }}
    .card-subtitle {{
      font-size: 0.8rem;
      color: var(--text-muted);
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

    /* Segmented Control Pill Toggles */
    .segmented-control {{
      display: inline-flex;
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      border-radius: 7px;
      padding: 2px;
      gap: 2px;
    }}
    .segment-btn {{
      padding: 4px 10px;
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--text-muted);
      background: transparent;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: all 0.12s ease;
      font-family: inherit;
    }}
    .segment-btn:hover {{
      color: var(--text-main);
    }}
    .segment-btn.active {{
      background: #ffffff;
      color: var(--text-main);
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.08);
      font-weight: 700;
    }}

    /* Form Inputs */
    .form-control {{
      width: 100%;
      background: #ffffff;
      border: 1px solid var(--border-strong);
      color: var(--text-main);
      padding: 8px 12px;
      border-radius: 7px;
      font-size: 0.85rem;
      outline: none;
      font-family: inherit;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }}
    .form-control:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.12);
    }}
    .form-label {{
      display: block;
      font-size: 0.74rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 5px;
    }}

    /* Table Styles */
    .table-container {{
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow-x: auto;
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
      cursor: pointer;
      user-select: none;
    }}
    th:hover {{
      color: var(--text-main);
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
      font-variant-numeric: tabular-nums;
    }}

    /* Badges */
    .badge {{
      display: inline-block;
      padding: 3px 8px;
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

    /* Team Pill Badges */
    .team-badge {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-weight: 700;
      font-size: 0.72rem;
      padding: 2px 7px;
      border-radius: 4px;
    }}
    .team-ind {{ background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }}
    .team-aus {{ background: #fefce8; color: #a16207; border: 1px solid #fef08a; }}
    .team-eng {{ background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }}
    .team-nz  {{ background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }}

    /* Head-to-Head Profiler */
    .h2h-container {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 9px;
      padding: 20px;
      margin-bottom: 24px;
      box-shadow: var(--shadow-sm);
    }}
    .h2h-controls {{
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      gap: 16px;
      align-items: center;
      margin-bottom: 20px;
    }}
    .player-select-card {{
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px 16px;
    }}
    .player-select-card.p1 {{
      border-left: 3px solid var(--primary);
    }}
    .player-select-card.p2 {{
      border-left: 3px solid var(--danger);
    }}
    .battle-bars {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-top: 16px;
    }}
    .battle-row {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}
    .battle-header {{
      display: flex;
      justify-content: space-between;
      font-size: 0.75rem;
      font-weight: 700;
    }}
    .battle-track {{
      display: flex;
      height: 8px;
      border-radius: 4px;
      overflow: hidden;
      background: var(--surface-subtle);
    }}
    .battle-fill-p1 {{
      background: var(--primary);
      transition: width 0.3s ease;
    }}
    .battle-fill-p2 {{
      background: var(--danger);
      transition: width 0.3s ease;
    }}

    /* Code Viewer */
    .code-viewer-grid {{
      display: grid;
      grid-template-columns: 260px 1fr;
      gap: 16px;
      height: 640px;
    }}
    .file-tree {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px;
      overflow-y: auto;
    }}
    .file-entry {{
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
      margin-bottom: 2px;
    }}
    .file-entry:hover {{
      background: var(--surface-subtle);
      color: var(--text-main);
    }}
    .file-entry.active {{
      background: var(--primary-subtle);
      color: var(--primary);
      border: 1px solid var(--primary-border);
      font-weight: 600;
    }}
    .editor-pane {{
      display: flex;
      flex-direction: column;
      height: 100%;
      border: 1px solid #1e293b;
      border-radius: 8px;
      overflow: hidden;
    }}
    .editor-topbar {{
      background: #0f172a;
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
      padding: 16px;
      overflow: auto;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      color: #e2e8f0;
      white-space: pre;
      line-height: 1.6;
      flex: 1;
    }}

    /* Math Box */
    .math-card {{
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      border-radius: 7px;
      padding: 12px 16px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.81rem;
      color: var(--navy);
      line-height: 1.5;
      margin: 12px 0;
    }}

    .figure-img {{
      width: 100%;
      border-radius: 8px;
      border: 1px solid var(--border);
      box-shadow: var(--shadow-sm);
      margin-top: 10px;
      background: #ffffff;
    }}
    .figure-caption {{
      font-size: 0.77rem;
      color: var(--text-muted);
      text-align: center;
      margin-top: 6px;
      font-style: italic;
    }}

    .tab-pane {{ display: none; }}
    .tab-pane.active {{ display: block; }}

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

  <!-- Academic Metadata Bar -->
  <div class="header-institution">
    <div class="header-institution-left">
      <span class="tag-course">BMAT202P</span>
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

  <!-- Primary Sticky Navbar -->
  <header class="navbar">
    <a href="#" class="navbar-brand">
      <div class="brand-mark">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <path d="M12 2a14.5 14.5 0 0 0 0 20"></path>
          <path d="M2 12h20"></path>
        </svg>
      </div>
      <span>CricketEdge</span>
    </a>

    <ul class="navbar-nav">
      <li class="nav-item active" onclick="showTab('overview', this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
        Overview
      </li>
      <li class="nav-item" onclick="showTab('players', this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
        Players
      </li>
      <li class="nav-item" onclick="showTab('regression', this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
        Regression
      </li>
      <li class="nav-item" onclick="showTab('probability', this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"></circle><path d="M8 12h8"></path><path d="M12 8v8"></path></svg>
        Probability
      </li>
      <li class="nav-item" onclick="showTab('hypothesis', this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M10 2v7.31"></path><path d="M14 9.3V2"></path><path d="M8.5 2h7"></path><path d="M14 9.3a6.5 6.5 0 1 1-4 0"></path><path d="M5.52 16h12.96"></path></svg>
        Hypothesis Testing
      </li>
      <li class="nav-item" onclick="showTab('chisq', this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="3" y1="15" x2="21" y2="15"></line><line x1="9" y1="3" x2="9" y2="21"></line><line x1="15" y1="3" x2="15" y2="21"></line></svg>
        Chi-Square
      </li>
      <li class="nav-item" onclick="showTab('anova', this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
        ANOVA
      </li>
      <li class="nav-item" onclick="showTab('data', this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path></svg>
        Data Explorer
      </li>
      <li class="nav-item" onclick="showTab('code', this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
        R Codebase
      </li>
    </ul>

    <div class="navbar-right">
      <div class="status-indicator">
        <span class="status-dot"></span>
        <span>260 Innings Sample</span>
      </div>
      <a href="CricketEdge_Lab_Report.pdf" target="_blank" class="btn btn-secondary">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
        PDF Report
      </a>
      <a href="CricketEdge_Lab_Report.docx" download class="btn btn-primary">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
        DOCX Report
      </a>
    </div>
  </header>

  <main class="main-container">

    <!-- 1. OVERVIEW TAB -->
    <section id="tab-overview" class="tab-pane active">
      <!-- High-Precision Metrics Ribbon -->
      <div class="metrics-ribbon">
        <div class="metric-cell">
          <div class="metric-val">260</div>
          <div class="metric-lbl">Total Innings</div>
          <div class="metric-sub">50 matches across 6 stadiums</div>
        </div>
        <div class="metric-cell">
          <div class="metric-val">8</div>
          <div class="metric-lbl">Elite Batsmen</div>
          <div class="metric-sub">India, Australia, England, NZ</div>
        </div>
        <div class="metric-cell">
          <div class="metric-val">10,205</div>
          <div class="metric-lbl">Tournament Runs</div>
          <div class="metric-sub">7,492 balls faced in total</div>
        </div>
        <div class="metric-cell">
          <div class="metric-val">39.25</div>
          <div class="metric-lbl">Mean Innings Score</div>
          <div class="metric-sub">Standard Deviation: 26.85 runs</div>
        </div>
        <div class="metric-cell">
          <div class="metric-val">136.2</div>
          <div class="metric-lbl">Aggregate Strike Rate</div>
          <div class="metric-sub">55.8% runs from boundaries</div>
        </div>
      </div>

      <div class="grid-2">
        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">Batsman Performance Ranking</div>
            </div>
            <div class="segmented-control">
              <button class="segment-btn active" onclick="switchOverviewMetric('runs', this)">Runs</button>
              <button class="segment-btn" onclick="switchOverviewMetric('sr', this)">Strike Rate</button>
              <button class="segment-btn" onclick="switchOverviewMetric('avg', this)">Average</button>
            </div>
          </div>
          <div class="card-subtitle">Comparative scoring output across all recorded tournament appearances</div>
          <canvas id="chartRuns" height="230"></canvas>
        </div>

        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">Score Distribution &amp; Central Tendency</div>
            </div>
            <span class="badge badge-neutral">Mean: 39.3 | Median: 33.0</span>
          </div>
          <div class="card-subtitle">Empirical scoring frequency grouped by 20-run bins</div>
          <canvas id="chartDist" height="230"></canvas>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">Batsman Summary &amp; Consistency Metric (Coefficient of Variation)</div>
          </div>
          <span class="badge badge-blue">R/descriptive_stats.R</span>
        </div>
        <div class="card-subtitle">Formulation: CV = (Standard Deviation / Mean) × 100. Lower values reflect consistent scoring anchors.</div>
        <div class="table-container">
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
                <td><span class="team-badge team-ind">IND</span></td>
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
                <td><span class="team-badge team-eng">ENG</span></td>
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
                <td><span class="team-badge team-aus">AUS</span></td>
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
                <td><span class="team-badge team-ind">IND</span></td>
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
                <td><span class="team-badge team-ind">IND</span></td>
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
                <td><span class="team-badge team-nz">NZ</span></td>
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
                <td><span class="team-badge team-aus">AUS</span></td>
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
                <td><span class="team-badge team-eng">ENG</span></td>
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

    <!-- 2. PLAYERS TAB (SIGNATURE BATTLE PROFILER) -->
    <section id="tab-players" class="tab-pane">
      <div class="h2h-container">
        <div class="card-header">
          <div>
            <div class="card-title">Head-to-Head Batsman Profiler &amp; Radar Arena</div>
            <div class="card-subtitle" style="margin-top: 4px; margin-bottom: 0;">Direct multivariate comparison across consistency, boundary volume, acceleration, and conversion</div>
          </div>
          <span class="badge badge-blue">Interactive Radar</span>
        </div>

        <div class="h2h-controls">
          <div class="player-select-card p1">
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
          <div style="font-weight: 800; font-size: 0.9rem; color: var(--text-faint); padding: 0 10px;">VS</div>
          <div class="player-select-card p2">
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

        <div class="grid-2">
          <div>
            <canvas id="chartPlayerRadar" height="280"></canvas>
          </div>
          <div>
            <div class="battle-bars" id="battleBarsContainer"></div>
            <div class="math-card" style="margin-top: 18px;">
              <strong>Scoring Stability Metric (CV):</strong><br/>
              CV = (Standard Deviation / Mean) × 100<br/>
              • Lower CV signifies anchor stability (e.g. Root: 45.1%, Kohli: 57.4%).<br/>
              • Higher CV signifies high-risk, high-reward burst acceleration (e.g. Maxwell: 94.8%).
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="card-title">Empirical Score Spread (Boxplots, IQR &amp; Diamond Means)</div>
          <span class="badge badge-neutral">ggplot2 geom_boxplot + geom_jitter</span>
        </div>
        <img src="assets/fig3_player_boxplots.png" alt="Player Boxplots" class="figure-img" />
        <div class="figure-caption">Fig 3: Interquartile ranges, medians, outlier fences, and jittered individual innings scores</div>
      </div>
    </section>

    <!-- 3. REGRESSION TAB -->
    <section id="tab-regression" class="tab-pane">
      <div class="grid-2">
        <div class="card">
          <div class="card-header">
            <div class="card-title">Fitted Simple Linear Model: runs ~ balls_faced</div>
            <span class="badge badge-pass">R² = 0.8986</span>
          </div>
          <div class="card-subtitle">Estimating marginal run output per ball faced via base R lm()</div>
          <div class="table-container" style="margin-bottom: 14px;">
            <table>
              <thead>
                <tr>
                  <th>Parameter</th>
                  <th class="text-right">Estimate</th>
                  <th class="text-right">Std Error</th>
                  <th class="text-right">t Value</th>
                  <th class="text-right">p-Value</th>
                  <th>Significance</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>(Intercept)</code></td>
                  <td class="text-right tabular">-0.5891</td>
                  <td class="text-right tabular">0.8412</td>
                  <td class="text-right tabular">-0.700</td>
                  <td class="text-right tabular">0.484</td>
                  <td><span class="badge badge-neutral">ns</span></td>
                </tr>
                <tr>
                  <td><code>balls_faced</code></td>
                  <td class="text-right tabular"><strong>+1.3412</strong></td>
                  <td class="text-right tabular">0.0280</td>
                  <td class="text-right tabular"><strong>47.89</strong></td>
                  <td class="text-right tabular">&lt; 2e-16</td>
                  <td><span class="badge badge-pass">*** (p &lt; 0.001)</span></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="math-card">
            <strong>Fitted Equation:</strong> <code>runs = -0.589 + 1.341 * balls_faced</code><br/>
            F-statistic: 2,294 on 1 and 259 DF, p &lt; 2.2e-16. Residual SE: 8.56 on 259 df.
          </div>
          <img src="assets/fig4_regression_fit.png" alt="Regression Fit" class="figure-img" />
          <div class="figure-caption">Fig 4: Scatter of observed innings scores against lm() fitted line</div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-title">Residual Diagnostics &amp; Assumption Checks</div>
            <span class="badge badge-neutral">Homoscedasticity</span>
          </div>
          <div class="card-subtitle">Validating constant error variance across predicted scoring ranges</div>
          <div class="math-card">
            <strong>Methodological Note on Boundaries:</strong><br/>
            Regressing runs against boundaries (4s &amp; 6s) produces an artificial R² &gt; 0.95. This reflects an arithmetic accounting decomposition (runs = 4×4s + 6×6s + singles) rather than an exogenous causal mechanism.
          </div>
          <img src="assets/fig5_regression_residuals.png" alt="Residuals" class="figure-img" />
          <div class="figure-caption">Fig 5: Residuals vs Fitted values with green Loess trend line and red zero-error baseline</div>
        </div>
      </div>
    </section>

    <!-- 4. PROBABILITY TAB -->
    <section id="tab-probability" class="tab-pane">
      <div class="grid-2">
        <div class="card">
          <div class="card-header">
            <div class="card-title">Binomial Distribution B(n = 6, p = 0.25)</div>
            <span class="badge badge-blue">dbinom()</span>
          </div>
          <div class="card-subtitle">Discrete probability model for boundary occurrences in a 6-ball over</div>
          <div class="table-container" style="margin-bottom: 12px;">
            <table>
              <thead>
                <tr>
                  <th>Boundaries (k)</th>
                  <th class="text-right">P(X = k)</th>
                  <th class="text-right">Cumulative P(X &le; k)</th>
                  <th>Interpretation</th>
                </tr>
              </thead>
              <tbody>
                <tr><td>k = 0</td><td class="text-right tabular">17.80%</td><td class="text-right tabular">17.80%</td><td>No boundary hit</td></tr>
                <tr><td>k = 1</td><td class="text-right tabular">35.60%</td><td class="text-right tabular">53.39%</td><td>Single boundary in over</td></tr>
                <tr><td>k = 2</td><td class="text-right tabular">29.66%</td><td class="text-right tabular">83.06%</td><td>Two boundaries in over</td></tr>
                <tr><td>k = 3</td><td class="text-right tabular">13.18%</td><td class="text-right tabular">96.24%</td><td>Three boundaries in over</td></tr>
                <tr><td>k = 4</td><td class="text-right tabular">3.30%</td><td class="text-right tabular">99.54%</td><td>Four boundaries in over</td></tr>
                <tr><td>k = 5</td><td class="text-right tabular">0.44%</td><td class="text-right tabular">99.98%</td><td>Five boundaries in over</td></tr>
                <tr><td>k = 6</td><td class="text-right tabular">0.02%</td><td class="text-right tabular">100.00%</td><td>Six boundaries in over</td></tr>
              </tbody>
            </table>
          </div>
          <img src="assets/fig6_binomial_pmf.png" alt="Binomial PMF" class="figure-img" />
          <div class="figure-caption">Fig 6: Discrete impulse needle plot matching base R plot(x, px, type="h")</div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-title">Continuous Normal Density N(μ = 160, σ = 25)</div>
            <span class="badge badge-blue">dnorm() &amp; pnorm()</span>
          </div>
          <div class="card-subtitle">Continuous model for total team innings scores with shaded probability area</div>
          <div class="math-card">
            <strong>Exact Interval Probabilities via pnorm():</strong><br/>
            • P(140 &le; X &le; 180) = pnorm(180) - pnorm(140) = <strong>57.63%</strong><br/>
            • P(Score &ge; 200) = pnorm(200, lower.tail=FALSE) = <strong>5.48%</strong><br/>
            • Theoretical Mean = 160.0 | Variance = 625.0
          </div>
          <img src="assets/fig7_normal_distribution.png" alt="Normal Density" class="figure-img" />
          <div class="figure-caption">Fig 7: Continuous bell density curve with shaded probability interval</div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="card-title">Monte Carlo Cricket Over Simulation (1,000 Overs)</div>
          <span class="badge badge-pass">Central Limit Theorem</span>
        </div>
        <div class="card-subtitle">Simulating discrete categorical deliveries and observing convergence toward normality</div>
        <div class="grid-2">
          <div>
            <div class="math-card">
              <strong>Ball-by-Ball Probabilities:</strong><br/>
              P(0) = 0.35, P(1) = 0.35, P(2) = 0.10, P(3) = 0.02, P(4) = 0.12, P(6) = 0.06<br/><br/>
              • Theoretical Single-Ball Mean: 1.34 runs (Var: 2.82)<br/>
              • Theoretical 6-Ball Over Mean: 8.04 runs (SD: 4.11)<br/>
              • Empirical 1,000 Over Mean: 8.08 runs (SD: 4.14)<br/>
              • Probability of Scoring &ge; 10 Runs in an Over: <strong>33.7%</strong>
            </div>
          </div>
          <div>
            <img src="assets/fig8_simulation_totals.png" alt="Simulation Totals" class="figure-img" />
            <div class="figure-caption">Fig 8: Frequency of 6-ball over totals converging toward normal profile</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 5. HYPOTHESIS TESTING TAB -->
    <section id="tab-hypothesis" class="tab-pane">
      <div class="card">
        <div class="card-header">
          <div class="card-title">Inferential Statistical Hypothesis Testing Engine</div>
          <span class="badge badge-blue">R/hypothesis_tests.R</span>
        </div>
        <div class="card-subtitle">Parametric and non-parametric tests with formal decisions strictly avoiding naive acceptance of H₀</div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Test Specification</th>
                <th>Null Hypothesis (H₀)</th>
                <th>Alternative (H₁)</th>
                <th>R Base Function</th>
                <th class="text-right">Statistic</th>
                <th class="text-right">p-Value</th>
                <th>Decision (α = 0.05)</th>
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
                <td><span class="badge badge-pass">Fail to Reject H₀</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- 6. CHI-SQUARE TAB -->
    <section id="tab-chisq" class="tab-pane">
      <div class="grid-2">
        <div class="card">
          <div class="card-header">
            <div class="card-title">Chi-Square Goodness-of-Fit Test</div>
            <span class="badge badge-pass">Uniform Fit Valid</span>
          </div>
          <div class="card-subtitle">Evaluating categorical innings frequencies against uniform condition expectations</div>
          <div class="math-card">
            <strong>R chisq.test() Output:</strong><br/>
            χ² = 3.824, df = 4, p-value = 0.4305<br/><br/>
            Decision: Since p &ge; 0.05, we <strong>fail to reject H₀</strong>. The categorical match conditions follow a uniform distribution.
          </div>
          <img src="assets/fig10_chisq_gof.png" alt="Chi-Square GOF" class="figure-img" />
          <div class="figure-caption">Fig 10: Observed vs Theoretical Expected Cell Counts across Conditions</div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-title">Contingency Independence &amp; Cochran's Audit</div>
            <span class="badge badge-neutral">Independence Test</span>
          </div>
          <div class="card-subtitle">Testing independence between batsman dismissal and order position</div>
          <div class="math-card">
            <strong>Cochran's Rule Audit:</strong><br/>
            • Condition 1: Minimum expected cell count &ge; 1.0 (Passed: min E_ij = 6.2)<br/>
            • Condition 2: No more than 20% cells &lt; 5 (Passed: 0.0% &lt; 5)<br/><br/>
            χ² = 6.14 (df = 7, p = 0.5234). Dismissal rate is statistically independent of batting order.
          </div>
        </div>
      </div>
    </section>

    <!-- 7. ANOVA TAB -->
    <section id="tab-anova" class="tab-pane">
      <div class="card">
        <div class="card-header">
          <div class="card-title">One-Way Analysis of Variance: aov(runs ~ player)</div>
          <span class="badge badge-pass">F-Test Significant</span>
        </div>
        <div class="card-subtitle">Evaluating between-group mean differences across 8 batsmen with Tukey HSD post-hoc</div>
        <div class="table-container" style="margin-bottom: 14px;">
          <table>
            <thead>
              <tr>
                <th>Source of Variation</th>
                <th class="text-right">Df</th>
                <th class="text-right">Sum of Squares</th>
                <th class="text-right">Mean Square</th>
                <th class="text-right">F Value</th>
                <th class="text-right">Pr(&gt;F)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>player (Between Groups)</code></td>
                <td class="text-right tabular">7</td>
                <td class="text-right tabular">9,842</td>
                <td class="text-right tabular">1,406.0</td>
                <td class="text-right tabular"><strong>2.164</strong></td>
                <td class="text-right tabular"><strong>0.0378 *</strong></td>
              </tr>
              <tr>
                <td><code>Residuals (Within Groups)</code></td>
                <td class="text-right tabular">253</td>
                <td class="text-right tabular">164,412</td>
                <td class="text-right tabular">649.9</td>
                <td class="text-right tabular">-</td>
                <td class="text-right tabular">-</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="math-card">
          <strong>Tukey HSD Post-Hoc Finding:</strong><br/>
          V. Kohli vs G. Maxwell: Difference = +22.6 runs, 95% CI: [+2.4, +42.8], p_adj = 0.0284*. All other pairwise comparisons do not reach family-wise significance at α = 0.05.
        </div>
        <img src="assets/fig9_anova_groups.png" alt="ANOVA Boxplot" class="figure-img" />
        <div class="figure-caption">Fig 9: Group Score Spread with Overlaid Means and Standard Error Bars</div>
      </div>
    </section>

    <!-- 8. DATA EXPLORER TAB -->
    <section id="tab-data" class="tab-pane">
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">Dataset Schema &amp; Full Innings Records (sample_cricket_data.csv)</div>
            <div class="card-subtitle" style="margin-top: 4px; margin-bottom: 0;">260 reproducible synthetic match records across 8 batsmen</div>
          </div>
          <button onclick="downloadCSV()" class="btn btn-primary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
            Download CSV
          </button>
        </div>

        <!-- Filter Controls -->
        <div style="display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 16px; align-items: center;">
          <input type="text" id="filterInput" placeholder="Search player, opponent, venue, ID..." onkeyup="filterData()" class="form-control" style="max-width: 280px;" />
          <select id="filterPlayer" class="form-control" style="max-width: 180px;" onchange="filterData()">
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
          <select id="filterCondition" class="form-control" style="max-width: 180px;" onchange="filterData()">
            <option value="">All Conditions</option>
            <option value="Day">Day</option>
            <option value="Day/Night">Day/Night</option>
            <option value="Dry/Spin">Dry/Spin</option>
            <option value="Overcast">Overcast</option>
            <option value="Pace-friendly">Pace-friendly</option>
          </select>
          <button class="btn btn-secondary" onclick="resetFilters()">Reset Filters</button>
          <span id="recordCount" style="font-size: 0.78rem; color: var(--text-muted); font-weight: 600; margin-left: auto;">Showing 260 of 260 innings</span>
        </div>

        <div class="table-container" style="max-height: 520px; overflow-y: auto;">
          <table>
            <thead>
              <tr>
                <th onclick="sortTable('match_id')">Match ID</th>
                <th onclick="sortTable('date')">Date</th>
                <th onclick="sortTable('player')">Batsman</th>
                <th onclick="sortTable('team')">Team</th>
                <th onclick="sortTable('opponent')">Opponent</th>
                <th onclick="sortTable('venue')">Venue</th>
                <th>Condition</th>
                <th class="text-right" onclick="sortTable('innings')">Inn</th>
                <th class="text-right" onclick="sortTable('runs')">Runs</th>
                <th class="text-right" onclick="sortTable('balls_faced')">Balls</th>
                <th class="text-right" onclick="sortTable('fours')">4s</th>
                <th class="text-right" onclick="sortTable('sixes')">6s</th>
                <th class="text-right">SR</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody id="dataTableBody"></tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- 9. R CODEBASE TAB -->
    <section id="tab-code" class="tab-pane">
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">RStudio Modular Codebase Explorer</div>
            <div class="card-subtitle" style="margin-top: 4px; margin-bottom: 0;">Direct access to all 11 backend R scripts and Shiny reactive modules</div>
          </div>
          <span style="font-size: 0.8rem; color: var(--primary); font-family: 'JetBrains Mono', monospace; font-weight: 700;">shiny::runApp()</span>
        </div>

        <div class="code-viewer-grid">
          <div class="file-tree" id="fileTree"></div>
          <div class="editor-pane">
            <div class="editor-topbar">
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

    // Comprehensive Player Profiles
    const playerStats = {{
      "V. Kohli": {{ team: "India", pos: "Pos 3 (Anchor)", runs: 1776, inn: 34, mean: 52.2, sd: 30.0, cv: 57.4, sr: 140.6, avg: 61.2, bPct: 58.6, fiftyRate: 50.0 }},
      "J. Root": {{ team: "England", pos: "Pos 3 (Anchor)", runs: 1576, inn: 36, mean: 43.8, sd: 19.7, cv: 45.1, sr: 125.9, avg: 60.6, bPct: 45.4, fiftyRate: 36.1 }},
      "S. Smith": {{ team: "Australia", pos: "Pos 3 (Anchor)", runs: 1360, inn: 33, mean: 41.2, sd: 22.5, cv: 54.5, sr: 130.5, avg: 59.1, bPct: 48.2, fiftyRate: 30.3 }},
      "R. Sharma": {{ team: "India", pos: "Pos 1 (Opener)", runs: 1344, inn: 40, mean: 33.6, sd: 23.7, cv: 70.5, sr: 134.5, avg: 39.5, bPct: 62.1, fiftyRate: 27.5 }},
      "KL Rahul": {{ team: "India", pos: "Pos 2 (Opener)", runs: 1178, inn: 27, mean: 43.6, sd: 31.7, cv: 72.7, sr: 131.8, avg: 53.5, bPct: 56.4, fiftyRate: 29.6 }},
      "K. Williamson": {{ team: "New Zealand", pos: "Pos 3 (Anchor)", runs: 1149, inn: 27, mean: 42.6, sd: 22.2, cv: 52.2, sr: 132.8, avg: 54.7, bPct: 47.9, fiftyRate: 33.3 }},
      "G. Maxwell": {{ team: "Australia", pos: "Pos 5 (Finisher)", runs: 918, inn: 31, mean: 29.6, sd: 28.1, cv: 94.8, sr: 152.7, avg: 30.6, bPct: 74.5, fiftyRate: 22.6 }},
      "B. Stokes": {{ team: "England", pos: "Pos 5 (All-Rounder)", runs: 904, inn: 32, mean: 28.2, sd: 21.2, cv: 75.1, sr: 138.7, avg: 33.5, bPct: 53.1, fiftyRate: 12.5 }}
    }};

    let radarChartInstance = null;
    let runsChartInstance = null;
    let currentSortCol = null;
    let currentSortAsc = true;

    function showTab(id, el) {{
      document.querySelectorAll('.tab-pane').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
      document.getElementById('tab-' + id).classList.add('active');
      if (el) el.classList.add('active');

      if (id === 'players' && radarChartInstance) {{
        radarChartInstance.resize();
      }}
      if (id === 'overview' && runsChartInstance) {{
        runsChartInstance.resize();
      }}
    }}

    function renderTableRows(items) {{
      const tbody = document.getElementById('dataTableBody');
      tbody.innerHTML = '';
      items.slice(0, 100).forEach(r => {{
        const tr = document.createElement('tr');
        const sr = r.balls_faced > 0 ? ((r.runs / r.balls_faced) * 100).toFixed(1) : '0.0';
        const teamClass = r.team === 'India' ? 'team-ind' : r.team === 'Australia' ? 'team-aus' : r.team === 'England' ? 'team-eng' : 'team-nz';
        tr.innerHTML = `
          <td><code style="font-size:0.8rem; font-weight:700;">${{r.match_id}}</code></td>
          <td class="tabular">${{r.date}}</td>
          <td><strong>${{r.player}}</strong></td>
          <td><span class="team-badge ${{teamClass}}">${{r.team.substring(0,3).toUpperCase()}}</span></td>
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

    function sortTable(col) {{
      if (currentSortCol === col) {{
        currentSortAsc = !currentSortAsc;
      }} else {{
        currentSortCol = col;
        currentSortAsc = true;
      }}
      data.sort((a, b) => {{
        let vA = a[col];
        let vB = b[col];
        if (typeof vA === 'string') {{
          return currentSortAsc ? vA.localeCompare(vB) : vB.localeCompare(vA);
        }} else {{
          return currentSortAsc ? vA - vB : vB - vA;
        }}
      }});
      filterData();
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

    // Switch Overview Metric
    function switchOverviewMetric(metric, btn) {{
      document.querySelectorAll('.segmented-control .segment-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const labels = ['V. Kohli', 'J. Root', 'S. Smith', 'R. Sharma', 'KL Rahul', 'K. Williamson', 'G. Maxwell', 'B. Stokes'];
      let values = [];
      let labelText = '';

      if (metric === 'runs') {{
        values = [1776, 1576, 1360, 1344, 1178, 1149, 918, 904];
        labelText = 'Total Runs';
        runsChartInstance.data.datasets[0].backgroundColor = '#0284c7';
      }} else if (metric === 'sr') {{
        values = [140.6, 125.9, 130.5, 134.5, 131.8, 132.8, 152.7, 138.7];
        labelText = 'Strike Rate';
        runsChartInstance.data.datasets[0].backgroundColor = '#059669';
      }} else if (metric === 'avg') {{
        values = [61.2, 60.6, 59.1, 39.5, 53.5, 54.7, 30.6, 33.5];
        labelText = 'Batting Average';
        runsChartInstance.data.datasets[0].backgroundColor = '#0f172a';
      }}

      runsChartInstance.data.datasets[0].label = labelText;
      runsChartInstance.data.datasets[0].data = values;
      runsChartInstance.update();
    }}

    // Update Player Comparison
    function updatePlayerComparison() {{
      const p1 = document.getElementById('selectP1').value;
      const p2 = document.getElementById('selectP2').value;

      const s1 = playerStats[p1];
      const s2 = playerStats[p2];

      const container = document.getElementById('battleBarsContainer');
      const metrics = [
        {{ name: 'Batting Average', v1: s1.avg, v2: s2.avg, unit: '' }},
        {{ name: 'Strike Rate', v1: s1.sr, v2: s2.sr, unit: '' }},
        {{ name: 'Stability Index (100 - CV)', v1: Math.max(0, 100 - s1.cv), v2: Math.max(0, 100 - s2.cv), unit: '%' }},
        {{ name: 'Boundary Dominance', v1: s1.bPct, v2: s2.bPct, unit: '%' }},
        {{ name: 'Fifty+ Conversion Rate', v1: s1.fiftyRate, v2: s2.fiftyRate, unit: '%' }}
      ];

      container.innerHTML = metrics.map(m => {{
        const total = m.v1 + m.v2;
        const pct1 = ((m.v1 / total) * 100).toFixed(1);
        const pct2 = (100 - pct1).toFixed(1);
        return `
          <div class="battle-row">
            <div class="battle-header">
              <span><strong>${{p1}}:</strong> ${{m.v1.toFixed(1)}}${{m.unit}}</span>
              <span style="color:var(--text-muted);">${{m.name}}</span>
              <span><strong>${{p2}}:</strong> ${{m.v2.toFixed(1)}}${{m.unit}}</span>
            </div>
            <div class="battle-track">
              <div class="battle-fill-p1" style="width: ${{pct1}}%;"></div>
              <div class="battle-fill-p2" style="width: ${{pct2}}%;"></div>
            </div>
          </div>
        `;
      }}).join('');

      if (radarChartInstance) {{
        radarChartInstance.data.datasets[0].label = `${{p1}} (${{s1.team}})`;
        radarChartInstance.data.datasets[0].data = [s1.avg, s1.sr / 2, Math.max(0, 100 - s1.cv), s1.bPct, s1.fiftyRate];

        radarChartInstance.data.datasets[1].label = `${{p2}} (${{s2.team}})`;
        radarChartInstance.data.datasets[1].data = [s2.avg, s2.sr / 2, Math.max(0, 100 - s2.cv), s2.bPct, s2.fiftyRate];
        radarChartInstance.update();
      }}
    }}

    // Setup Code Viewer
    function setupCodeViewer() {{
      const tree = document.getElementById('fileTree');
      const display = document.getElementById('codeDisplay');
      const headerTitle = document.getElementById('activeFileTitle');
      tree.innerHTML = '';

      const filenames = Object.keys(rFiles);
      filenames.forEach((fname, idx) => {{
        const item = document.createElement('div');
        item.className = 'file-entry' + (idx === 0 ? ' active' : '');
        item.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg> <span>${{fname}}</span>`;
        item.onclick = () => {{
          document.querySelectorAll('.file-entry').forEach(i => i.classList.remove('active'));
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
        btn.textContent = 'Copied to Clipboard!';
        setTimeout(() => {{ btn.textContent = 'Copy Code'; }}, 2000);
      }});
    }}

    window.onload = function() {{
      renderTableRows(data);
      setupCodeViewer();
      updatePlayerComparison();

      Chart.defaults.color = '#64748b';
      Chart.defaults.font.family = "'Plus Jakarta Sans', -apple-system, sans-serif";

      // Runs Chart
      runsChartInstance = new Chart(document.getElementById('chartRuns'), {{
        type: 'bar',
        data: {{
          labels: ['V. Kohli', 'J. Root', 'S. Smith', 'R. Sharma', 'KL Rahul', 'K. Williamson', 'G. Maxwell', 'B. Stokes'],
          datasets: [{{
            label: 'Total Runs',
            data: [1776, 1576, 1360, 1344, 1178, 1149, 918, 904],
            backgroundColor: '#0284c7',
            hoverBackgroundColor: '#0369a1',
            borderRadius: 5
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
              ticks: {{ color: '#334155', font: {{ weight: '600' }} }}
            }},
            y: {{
              grid: {{ color: '#f1f5f9' }},
              ticks: {{ color: '#64748b' }}
            }}
          }}
        }}
      }});

      // Score Distribution Chart
      new Chart(document.getElementById('chartDist'), {{
        type: 'bar',
        data: {{
          labels: ['0-19', '20-39', '40-59', '60-79', '80-99', '100+'],
          datasets: [{{
            label: 'Innings Count',
            data: [78, 79, 53, 33, 11, 6],
            backgroundColor: '#0f172a',
            hoverBackgroundColor: '#1e293b',
            borderRadius: 5
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
              ticks: {{ color: '#334155', font: {{ weight: '600' }} }}
            }},
            y: {{
              grid: {{ color: '#f1f5f9' }},
              ticks: {{ color: '#64748b' }}
            }}
          }}
        }}
      }});

      // Radar Chart
      radarChartInstance = new Chart(document.getElementById('chartPlayerRadar'), {{
        type: 'radar',
        data: {{
          labels: ['Batting Avg', 'Strike Rate / 2', 'Stability Index', 'Boundary Dominance', 'Fifty+ Rate'],
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

print(f"Generated CricketEdge Impeccable Light-Themed Web Portal at {output_path} successfully!")
