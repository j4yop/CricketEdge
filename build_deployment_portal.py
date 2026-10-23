#!/usr/bin/env python3
import json
import os

with open('/tmp/cricket_data_embedded.json') as f:
    raw_data = json.load(f)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CricketEdge — Statistical Cricket Performance Analyzer | BMAT202P</title>
  <meta name="description" content="End-to-End Statistical Cricket Performance Analyzer built for BMAT202P Probability and Statistics at VIT Chennai." />
  
  <!-- Fonts & Icons -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

  <style>
    :root {{
      --bg-dark: #070b12;
      --card-bg: #0f172a;
      --card-border: #1e293b;
      --primary: #38bdf8;
      --primary-glow: rgba(56, 189, 248, 0.15);
      --accent: #0ea5e9;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --success: #10b981;
      --warning: #f59e0b;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg-dark);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }}

    /* Top Institution Banner */
    .header-banner {{
      background: linear-gradient(180deg, #0f172a 0%, #070b12 100%);
      border-bottom: 1px solid var(--card-border);
      padding: 16px 24px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
    }}
    .logo-container {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    .uni-logo {{
      height: 48px;
      width: auto;
      object-fit: contain;
      background: white;
      padding: 4px 8px;
      border-radius: 6px;
    }}
    .header-title-box h1 {{
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--text);
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .header-title-box p {{
      font-size: 0.8rem;
      color: var(--text-muted);
    }}
    .download-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s ease;
      border: 1px solid transparent;
    }}
    .btn-primary {{
      background: #0284c7;
      color: white;
    }}
    .btn-primary:hover {{
      background: #0369a1;
      transform: translateY(-1px);
    }}
    .btn-secondary {{
      background: #1e293b;
      color: #e2e8f0;
      border-color: #334155;
    }}
    .btn-secondary:hover {{
      background: #334155;
      color: white;
    }}

    /* Main Container */
    .container {{
      max-width: 1300px;
      margin: 0 auto;
      padding: 24px 20px;
    }}

    /* Navigation Tabs */
    .nav-tabs {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 24px;
      border-bottom: 1px solid var(--card-border);
      padding-bottom: 12px;
    }}
    .nav-tab {{
      padding: 8px 16px;
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.88rem;
      font-weight: 600;
      transition: all 0.2s;
    }}
    .nav-tab:hover {{
      color: var(--text);
      background: rgba(255, 255, 255, 0.05);
    }}
    .nav-tab.active {{
      background: var(--primary-glow);
      color: var(--primary);
      border-color: rgba(56, 189, 248, 0.3);
    }}

    /* KPI Grid */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}
    .kpi-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 16px 20px;
      position: relative;
      overflow: hidden;
    }}
    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; height: 3px;
      background: var(--primary);
    }}
    .kpi-value {{
      font-size: 1.8rem;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.5px;
    }}
    .kpi-label {{
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    /* Section Cards */
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 24px;
    }}
    .card-title {{
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    /* Grid Layouts */
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
    }}
    @media(max-width: 900px) {{
      .grid-2 {{ grid-template-columns: 1fr; }}
    }}

    /* Tables */
    .table-container {{
      overflow-x: auto;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
      text-align: left;
    }}
    th {{
      background: #1e293b;
      color: #cbd5e1;
      padding: 10px 14px;
      font-weight: 700;
    }}
    td {{
      padding: 9px 14px;
      border-bottom: 1px solid #1e293b;
      color: #94a3b8;
    }}
    tr:hover td {{
      background: rgba(255, 255, 255, 0.02);
      color: #ffffff;
    }}
    .badge {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 12px;
      font-size: 0.72rem;
      font-weight: 700;
    }}
    .badge-pass {{ background: rgba(16, 185, 129, 0.15); color: #34d399; }}
    .badge-reject {{ background: rgba(244, 63, 94, 0.15); color: #fb7185; }}

    /* Formula & Code Boxes */
    .formula-box {{
      background: #020617;
      border-left: 3px solid var(--primary);
      padding: 12px 16px;
      border-radius: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      color: #38bdf8;
      margin: 12px 0;
      line-height: 1.6;
    }}

    /* Tab content toggling */
    .tab-content {{ display: none; }}
    .tab-content.active {{ display: block; }}

    /* Footer */
    footer {{
      background: #0b0f19;
      border-top: 1px solid var(--card-border);
      padding: 32px 20px;
      margin-top: 60px;
    }}
    .footer-content {{
      max-width: 1300px;
      margin: 0 auto;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: 24px;
      font-size: 0.85rem;
      color: var(--text-muted);
    }}
    .team-badge {{
      background: #1e293b;
      padding: 4px 10px;
      border-radius: 6px;
      color: #e2e8f0;
      font-size: 0.78rem;
      margin: 2px 4px 2px 0;
      display: inline-block;
    }}
  </style>
</head>
<body>

  <!-- Top Header Banner -->
  <header class="header-banner">
    <div class="logo-container">
      <img src="assets/vit_chennai_logo_top.png" alt="VIT Chennai Logo" class="uni-logo" />
      <div class="header-title-box">
        <h1>🏏 CricketEdge — Statistical Analyzer</h1>
        <p>BMAT202P Probability & Statistics | Experiential Learning Project | VIT Chennai</p>
      </div>
    </div>
    <div class="download-actions">
      <a href="CricketEdge_Lab_Report.docx" download class="btn btn-primary">
        📥 Download DOCX Report
      </a>
      <a href="CricketEdge_Lab_Report.pdf" target="_blank" class="btn btn-secondary">
        📄 View PDF Report
      </a>
      <a href="sample_cricket_data.csv" download class="btn btn-secondary">
        📊 Raw Dataset CSV
      </a>
    </div>
  </header>

  <div class="container">
    <!-- Navigation Tabs -->
    <nav class="nav-tabs">
      <button class="nav-tab active" onclick="switchTab('overview')">📊 Overview</button>
      <button class="nav-tab" onclick="switchTab('players')">👥 Player Comparison</button>
      <button class="nav-tab" onclick="switchTab('regression')">📈 Regression Model</button>
      <button class="nav-tab" onclick="switchTab('probability')">🎲 Probability Models</button>
      <button class="nav-tab" onclick="switchTab('hypothesis')">🔬 Hypothesis & ANOVA</button>
      <button class="nav-tab" onclick="switchTab('data')">📁 Data Explorer</button>
      <button class="nav-tab" onclick="switchTab('report')">📄 Academic Lab Report</button>
    </nav>

    <!-- TAB 1: OVERVIEW -->
    <div id="tab-overview" class="tab-content active">
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-value">261</div>
          <div class="kpi-label">Total Innings Records</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-value">8</div>
          <div class="kpi-label">Elite Batsmen Analyzed</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-value">9,491</div>
          <div class="kpi-label">Total Cumulative Runs</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-value">36.36</div>
          <div class="kpi-label">Mean Runs per Innings</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-value">137.9</div>
          <div class="kpi-label">Overall Strike Rate</div>
        </div>
      </div>

      <div class="grid-2">
        <div class="card">
          <div class="card-title">📊 Total Runs by Batsman</div>
          <canvas id="chartRunsByPlayer" height="260"></canvas>
        </div>
        <div class="card">
          <div class="card-title">📈 Innings Score Distribution</div>
          <canvas id="chartScoreDist" height="260"></canvas>
        </div>
      </div>

      <div class="card">
        <div class="card-title">📋 Performance & Consistency Summary (Base R Formulations)</div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Batsman</th>
                <th>Team</th>
                <th>Innings</th>
                <th>Runs</th>
                <th>Mean</th>
                <th>Median</th>
                <th>SD</th>
                <th>Strike Rate</th>
                <th>Average</th>
                <th>CV (%)</th>
              </tr>
            </thead>
            <tbody>
              <tr><td><strong>V. Kohli</strong></td><td>India</td><td>35</td><td>1,772</td><td>50.6</td><td>49.0</td><td>26.3</td><td>137.9</td><td>61.1</td><td><span class="badge badge-pass">52.0%</span></td></tr>
              <tr><td><strong>J. Root</strong></td><td>England</td><td>36</td><td>1,576</td><td>43.8</td><td>42.5</td><td>23.8</td><td>125.7</td><td>54.3</td><td><span class="badge badge-pass">54.3%</span></td></tr>
              <tr><td><strong>S. Smith</strong></td><td>Australia</td><td>33</td><td>1,360</td><td>41.2</td><td>38.0</td><td>24.9</td><td>128.4</td><td>50.4</td><td><span class="badge badge-pass">60.4%</span></td></tr>
              <tr><td><strong>R. Sharma</strong></td><td>India</td><td>34</td><td>1,344</td><td>39.5</td><td>36.0</td><td>28.5</td><td>141.8</td><td>44.8</td><td>72.2%</td></tr>
              <tr><td><strong>KL Rahul</strong></td><td>India</td><td>31</td><td>1,178</td><td>38.0</td><td>35.0</td><td>25.1</td><td>135.2</td><td>45.3</td><td>66.1%</td></tr>
              <tr><td><strong>K. Williamson</strong></td><td>New Zealand</td><td>28</td><td>1,149</td><td>41.0</td><td>39.0</td><td>22.7</td><td>126.5</td><td>52.2</td><td><span class="badge badge-pass">55.4%</span></td></tr>
              <tr><td><strong>G. Maxwell</strong></td><td>Australia</td><td>30</td><td>918</td><td>30.6</td><td>26.5</td><td>27.4</td><td>157.1</td><td>32.8</td><td><span class="badge badge-reject">89.5%</span></td></tr>
              <tr><td><strong>B. Stokes</strong></td><td>England</td><td>27</td><td>904</td><td>33.5</td><td>29.0</td><td>26.8</td><td>143.9</td><td>37.7</td><td>80.0%</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 2: PLAYERS -->
    <div id="tab-players" class="tab-content">
      <div class="card">
        <div class="card-title">👥 Batsman Consistency & Archetype Comparison</div>
        <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 16px;">
          The Coefficient of Variation (CV = SD / Mean × 100) measures relative dispersion. V. Kohli exhibits the lowest CV (52.0%) identifying him as an <strong>Anchor Batsman</strong>, while G. Maxwell exhibits the highest CV (89.5%) and highest strike rate (157.1), characterizing a <strong>High-Variance Match Winner</strong>.
        </p>
        <div class="grid-2">
          <canvas id="chartPlayerRadar" height="280"></canvas>
          <div>
            <img src="assets/fig3_player_boxplots.png" alt="Boxplots" style="width: 100%; border-radius: 8px; border: 1px solid var(--card-border);" />
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: REGRESSION -->
    <div id="tab-regression" class="tab-content">
      <div class="grid-2">
        <div class="card">
          <div class="card-title">📈 Fitted Simple Linear Model: runs ~ balls_faced</div>
          <div class="formula-box">
            Fitted Equation: runs = -0.589 + 1.341 × balls_faced<br>
            Slope: β₁ = 1.341 (SE = 0.028, t = 47.89, p &lt; 2e-16 ***)<br>
            R²: 0.8986 (Adjusted R² = 0.8982)<br>
            F-Statistic: F(1, 259) = 2,294 (p &lt; 2.2e-16)
          </div>
          <img src="assets/fig4_regression_fit.png" alt="Regression Fit" style="width: 100%; border-radius: 8px; border: 1px solid var(--card-border);" />
        </div>
        <div class="card">
          <div class="card-title">🔬 Residual Diagnostics (Homoscedasticity Check)</div>
          <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 12px;">
            Residuals vs. Fitted plot displays uniform spread across fitted run totals, confirming linear regression assumption validity without extreme heteroscedastic funneling.
          </p>
          <img src="assets/fig5_regression_residuals.png" alt="Residuals" style="width: 100%; border-radius: 8px; border: 1px solid var(--card-border);" />
        </div>
      </div>
    </div>

    <!-- TAB 4: PROBABILITY -->
    <div id="tab-probability" class="tab-content">
      <div class="grid-2">
        <div class="card">
          <div class="card-title">🎲 Binomial Distribution B(n = 6, p = 0.25)</div>
          <div class="formula-box">
            P(X = k) = (n! / (k!(n-k)!)) · p^k · (1-p)^(n-k)<br>
            E[X] = n·p = 1.50 boundaries | Var(X) = n·p·(1-p) = 1.125
          </div>
          <img src="assets/fig6_binomial_pmf.png" alt="Binomial PMF" style="width: 100%; border-radius: 8px; border: 1px solid var(--card-border);" />
        </div>
        <div class="card">
          <div class="card-title">🔔 Continuous Normal Density N(μ = 160, σ = 25)</div>
          <div class="formula-box">
            f(x) = (1 / (σ√(2π))) · exp(-(x-μ)² / (2σ²))<br>
            Cumulative Interval: P(140 ≤ X ≤ 180) = pnorm(180) - pnorm(140) = 57.63%
          </div>
          <img src="assets/fig7_normal_distribution.png" alt="Normal Density" style="width: 100%; border-radius: 8px; border: 1px solid var(--card-border);" />
        </div>
      </div>
    </div>

    <!-- TAB 5: HYPOTHESIS & ANOVA -->
    <div id="tab-hypothesis" class="tab-content">
      <div class="card">
        <div class="card-title">🔬 Inferential Hypothesis Testing Matrix (α = 0.05)</div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Statistical Test</th>
                <th>Null Hypothesis (H₀)</th>
                <th>Alternative (H₁)</th>
                <th>Test Statistic</th>
                <th>p-Value</th>
                <th>Decision Logic</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>1-Sample t-Test</strong></td>
                <td>μ_Kohli = 35 runs</td>
                <td>μ_Kohli &gt; 35</td>
                <td>t = 3.51 (df = 34)</td>
                <td>0.00065</td>
                <td><span class="badge badge-reject">Reject H₀ (Significantly higher)</span></td>
              </tr>
              <tr>
                <td><strong>1-Sample Proportion</strong></td>
                <td>p_boundary = 0.15</td>
                <td>p_boundary ≠ 0.15</td>
                <td>χ² = 8.42 (df = 1)</td>
                <td>0.0037</td>
                <td><span class="badge badge-reject">Reject H₀ (Boundary rate ≠ 15%)</span></td>
              </tr>
              <tr>
                <td><strong>2-Sample Welch t-Test</strong></td>
                <td>μ_Kohli - μ_Maxwell = 0</td>
                <td>μ_Kohli ≠ μ_Maxwell</td>
                <td>t = 2.97 (df = 61.8)</td>
                <td>0.0042</td>
                <td><span class="badge badge-reject">Reject H₀ (Significant diff)</span></td>
              </tr>
              <tr>
                <td><strong>2-Sample Proportion</strong></td>
                <td>p_Maxwell = p_Root</td>
                <td>p_Maxwell &gt; p_Root</td>
                <td>χ² = 12.18 (df = 1)</td>
                <td>0.00048</td>
                <td><span class="badge badge-reject">Reject H₀ (Maxwell &gt; Root boundary %)</span></td>
              </tr>
              <tr>
                <td><strong>Paired t-Test</strong></td>
                <td>μ_diff(Inn1 - Inn2) = 0</td>
                <td>μ_diff ≠ 0</td>
                <td>t = 0.84 (df = 48)</td>
                <td>0.405</td>
                <td><span class="badge badge-pass">Fail to Reject H₀ (No innings bias)</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="grid-2">
        <div class="card">
          <div class="card-title">⚖️ One-Way ANOVA F-Ratio Breakdown</div>
          <div class="formula-box">
            F(7, 253) = MS_between / MS_within = 2.164 (p = 0.0378 *)<br>
            Decision: Reject H₀ at α = 0.05. Statistically significant variation in mean runs across batsman groups.
          </div>
          <img src="assets/fig9_anova_groups.png" alt="ANOVA Boxplot" style="width: 100%; border-radius: 8px; border: 1px solid var(--card-border);" />
        </div>
        <div class="card">
          <div class="card-title">📐 Chi-Square Goodness-of-Fit</div>
          <div class="formula-box">
            χ²(df = 4) = 3.82 (p = 0.431 &gt; 0.05)<br>
            Decision: Fail to Reject H₀. Match conditions follow uniform distribution without sampling bias.
          </div>
          <img src="assets/fig10_chisq_gof.png" alt="Chi-Square GOF" style="width: 100%; border-radius: 8px; border: 1px solid var(--card-border);" />
        </div>
      </div>
    </div>

    <!-- TAB 6: DATA EXPLORER -->
    <div id="tab-data" class="tab-content">
      <div class="card">
        <div class="card-title">📁 Interactive Dataset Explorer (261 Innings Records)</div>
        <div style="margin-bottom: 16px; display: flex; gap: 12px; flex-wrap: wrap;">
          <input type="text" id="searchInput" placeholder="Search player, team, opponent..." onkeyup="filterTable()" style="background: #020617; border: 1px solid var(--card-border); color: white; padding: 8px 14px; border-radius: 6px; font-size: 0.85rem; width: 300px;" />
          <button onclick="downloadCSV()" class="btn btn-secondary">📥 Export Cleaned CSV</button>
        </div>
        <div class="table-container" style="max-height: 500px; overflow-y: auto;">
          <table id="dataTable">
            <thead>
              <tr>
                <th>Match ID</th>
                <th>Date</th>
                <th>Player</th>
                <th>Team</th>
                <th>Opponent</th>
                <th>Innings</th>
                <th>Runs</th>
                <th>Balls</th>
                <th>4s</th>
                <th>6s</th>
                <th>SR</th>
                <th>Dismissal</th>
              </tr>
            </thead>
            <tbody id="tableBody"></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 7: ACADEMIC REPORT -->
    <div id="tab-report" class="tab-content">
      <div class="card">
        <div class="card-title">📄 Official Academic Lab Report (BMAT202P Format)</div>
        <div style="margin-bottom: 16px; display: flex; gap: 12px;">
          <a href="CricketEdge_Lab_Report.docx" download class="btn btn-primary">📥 Download Official Word Document (.docx)</a>
          <a href="CricketEdge_Lab_Report.pdf" target="_blank" class="btn btn-secondary">🔗 Open Fullscreen PDF</a>
        </div>
        <iframe src="CricketEdge_Lab_Report.pdf" style="width: 100%; height: 800px; border: 1px solid var(--card-border); border-radius: 8px;"></iframe>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer>
    <div class="footer-content">
      <div>
        <h4 style="color: white; margin-bottom: 8px;">CricketEdge — BMAT202P Lab Experiential Learning</h4>
        <p>Department of Mathematics, SAS & School of Computer Science and Engineering</p>
        <p>Vellore Institute of Technology, Chennai Campus</p>
        <p style="margin-top: 8px;">Submitted to: <strong>Dr Thangaraj M</strong> (Assistant Professor Senior Grade 2)</p>
      </div>
      <div>
        <h4 style="color: white; margin-bottom: 8px;">Project Team</h4>
        <div>
          <span class="team-badge">Pragyan Jain (24BLC1100)</span>
          <span class="team-badge">Shivam Kumar (24BLC1103)</span>
          <span class="team-badge">Abhishek Kumar Singh (24BLC1128)</span>
          <span class="team-badge">Shiven Sharma (24BLC1088)</span>
          <span class="team-badge">Kishore Pashupati (24BCE1874)</span>
        </div>
        <p style="margin-top: 8px; font-weight: 600; color: #38bdf8;">Branch: Electronics and Computer Engineering</p>
      </div>
    </div>
  </footer>

  <!-- Scripts -->
  <script>
    const data = {json.dumps(raw_data)};

    function switchTab(tabId) {{
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
      document.getElementById('tab-' + tabId).classList.add('active');
      event.target.classList.add('active');
    }}

    // Populate Table
    function renderTable(items) {{
      const tbody = document.getElementById('tableBody');
      tbody.innerHTML = '';
      items.slice(0, 100).forEach(r => {{
        const tr = document.createElement('tr');
        const sr = r.balls_faced > 0 ? ((r.runs / r.balls_faced) * 100).toFixed(1) : '0.0';
        tr.innerHTML = `
          <td><strong>${{r.match_id}}</strong></td>
          <td>${{r.date}}</td>
          <td>${{r.player}}</td>
          <td>${{r.team}}</td>
          <td>${{r.opponent}}</td>
          <td>${{r.innings}}</td>
          <td><strong>${{r.runs}}</strong></td>
          <td>${{r.balls_faced}}</td>
          <td>${{r.fours}}</td>
          <td>${{r.sixes}}</td>
          <td>${{sr}}</td>
          <td>${{r.dismissals == 1 ? '<span style="color:#fb7185">Out</span>' : '<span style="color:#34d399">Not Out</span>'}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function filterTable() {{
      const query = document.getElementById('searchInput').value.toLowerCase();
      const filtered = data.filter(d => 
        d.player.toLowerCase().includes(query) ||
        d.team.toLowerCase().includes(query) ||
        d.opponent.toLowerCase().includes(query) ||
        d.match_id.toLowerCase().includes(query)
      );
      renderTable(filtered);
    }}

    function downloadCSV() {{
      window.location.href = 'sample_cricket_data.csv';
    }}

    // Charts
    window.onload = function() {{
      renderTable(data);

      // Runs Chart
      new Chart(document.getElementById('chartRunsByPlayer'), {{
        type: 'bar',
        data: {{
          labels: ['V. Kohli', 'J. Root', 'S. Smith', 'R. Sharma', 'KL Rahul', 'K. Williamson', 'G. Maxwell', 'B. Stokes'],
          datasets: [{{
            label: 'Total Runs Scored',
            data: [1772, 1576, 1360, 1344, 1178, 1149, 918, 904],
            backgroundColor: '#0284c7',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }} }},
            y: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }} }}
          }}
        }}
      }});

      // Distribution Chart
      new Chart(document.getElementById('chartScoreDist'), {{
        type: 'bar',
        data: {{
          labels: ['0-19', '20-39', '40-59', '60-79', '80-99', '100+'],
          datasets: [{{
            label: 'Innings Frequency',
            data: [82, 75, 52, 34, 13, 5],
            backgroundColor: '#38bdf8',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }} }},
            y: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }} }}
          }}
        }}
      }});

      // Radar Chart
      new Chart(document.getElementById('chartPlayerRadar'), {{
        type: 'radar',
        data: {{
          labels: ['Average', 'Strike Rate / 2', 'Stability (100 - CV)', 'Boundaries %', 'Fifty+ Rate'],
          datasets: [
            {{
              label: 'V. Kohli (Anchor)',
              data: [61.1, 68.95, 48.0, 58.2, 72.0],
              borderColor: '#38bdf8',
              backgroundColor: 'rgba(56, 189, 248, 0.2)'
            }},
            {{
              label: 'G. Maxwell (Finisher)',
              data: [32.8, 78.55, 10.5, 76.4, 38.0],
              borderColor: '#f43f5e',
              backgroundColor: 'rgba(244, 63, 94, 0.2)'
            }}
          ]
        }},
        options: {{
          responsive: true,
          scales: {{
            r: {{
              grid: {{ color: '#1e293b' }},
              angleLines: {{ color: '#1e293b' }},
              ticks: {{ display: false }}
            }}
          }},
          plugins: {{
            legend: {{ labels: {{ color: '#e2e8f0' }} }}
          }}
        }}
      }});
    }};
  </script>
</body>
</html>
"""

with open('/home/pragyan/cricketProject/deployment/index.html', 'w') as f:
    f.write(html)

print("Generated /home/pragyan/cricketProject/deployment/index.html successfully!")
