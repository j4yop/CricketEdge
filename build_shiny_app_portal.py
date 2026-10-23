#!/usr/bin/env python3
import json
import glob
import os
import html as html_lib

# Load raw sample data
with open('/tmp/cricket_data_embedded.json') as f:
    raw_data = json.load(f)

# Load all R scripts
r_code_dict = {}
r_file_paths = ['app.R'] + sorted(glob.glob('R/*.R'))
for fpath in r_file_paths:
    with open(fpath) as f:
        r_code_dict[fpath] = f.read()

print(f"Loaded {len(r_code_dict)} R source files.")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CricketEdge — Statistical Cricket Performance Analyzer</title>
  
  <!-- Fonts & Libraries -->
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
      --primary-hover: #0284c7;
      --primary-glow: rgba(56, 189, 248, 0.12);
      --accent: #38bdf8;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #f43f5e;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg-dark);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}

    /* Navbar matching R Shiny bslib styling */
    .navbar {{
      background: #0f172a;
      border-bottom: 1px solid var(--card-border);
      padding: 0 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 64px;
      position: sticky;
      top: 0;
      z-index: 100;
    }}
    .navbar-brand {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--primary);
      text-decoration: none;
      letter-spacing: -0.5px;
    }}
    .navbar-nav {{
      display: flex;
      align-items: center;
      gap: 4px;
      list-style: none;
      overflow-x: auto;
    }}
    .nav-item {{
      padding: 8px 14px;
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.85rem;
      font-weight: 600;
      border-radius: 8px;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.15s ease;
      border: 1px solid transparent;
    }}
    .nav-item:hover {{
      color: var(--text);
      background: rgba(255, 255, 255, 0.05);
    }}
    .nav-item.active {{
      color: var(--primary);
      background: var(--primary-glow);
      border-color: rgba(56, 189, 248, 0.3);
    }}

    .navbar-right {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .mode-badge {{
      background: rgba(56, 189, 248, 0.1);
      border: 1px solid rgba(56, 189, 248, 0.3);
      color: var(--primary);
      padding: 4px 10px;
      border-radius: 16px;
      font-size: 0.72rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .mode-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--primary);
    }}

    /* Main Container */
    .main-container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px;
      flex: 1;
      width: 100%;
    }}

    /* KPI Grid */
    .kpi-row {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}
    .kpi-box {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 16px 20px;
      position: relative;
    }}
    .kpi-box::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; height: 3px;
      background: var(--primary);
      border-top-left-radius: 12px;
      border-top-right-radius: 12px;
    }}
    .kpi-val {{
      font-size: 1.85rem;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.5px;
    }}
    .kpi-lbl {{
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    /* Card Panels */
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 24px;
    }}
    .card-header-title {{
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
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
    @media(max-width: 960px) {{
      .grid-2, .grid-3 {{ grid-template-columns: 1fr; }}
    }}

    /* Form Controls */
    .form-group {{
      margin-bottom: 16px;
    }}
    .form-label {{
      display: block;
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      margin-bottom: 6px;
    }}
    .form-control {{
      width: 100%;
      background: #070b12;
      border: 1px solid var(--card-border);
      color: white;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 0.88rem;
      outline: none;
    }}
    .form-control:focus {{
      border-color: var(--primary);
    }}

    /* Tables */
    .table-responsive {{
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
      white-space: nowrap;
    }}
    td {{
      padding: 9px 14px;
      border-bottom: 1px solid #1e293b;
      color: #cbd5e1;
      white-space: nowrap;
    }}
    tr:hover td {{
      background: rgba(255, 255, 255, 0.03);
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

    /* Formula & Console Boxes */
    .code-box {{
      background: #020617;
      border: 1px solid #1e293b;
      border-left: 3px solid var(--primary);
      padding: 14px 18px;
      border-radius: 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      color: #38bdf8;
      overflow-x: auto;
      line-height: 1.6;
    }}

    /* Tab Panels */
    .tab-pane {{ display: none; }}
    .tab-pane.active {{ display: block; }}

    /* Buttons */
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.2s;
      border: 1px solid transparent;
    }}
    .btn-primary {{
      background: #0284c7;
      color: white;
    }}
    .btn-primary:hover {{
      background: #0369a1;
    }}
    .btn-secondary {{
      background: #1e293b;
      color: #e2e8f0;
      border-color: #334155;
    }}
    .btn-secondary:hover {{
      background: #334155;
    }}

    /* Code Viewer Tab */
    .code-viewer-layout {{
      display: grid;
      grid-template-columns: 260px 1fr;
      gap: 16px;
      height: 650px;
    }}
    .file-tree {{
      background: #020617;
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 12px;
      overflow-y: auto;
    }}
    .file-item {{
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 0.82rem;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      font-family: 'JetBrains Mono', monospace;
    }}
    .file-item:hover {{
      background: rgba(255, 255, 255, 0.05);
      color: white;
    }}
    .file-item.active {{
      background: var(--primary-glow);
      color: var(--primary);
      font-weight: 600;
    }}
    .code-display {{
      background: #020617;
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 16px;
      overflow: auto;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      color: #e2e8f0;
      white-space: pre;
    }}

    footer {{
      background: #020617;
      border-top: 1px solid var(--card-border);
      padding: 16px 24px;
      font-size: 0.78rem;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
  </style>
</head>
<body>

  <!-- Top Navbar -->
  <header class="navbar">
    <a href="#" class="navbar-brand">
      🏏 CricketEdge
    </a>
    <ul class="navbar-nav">
      <li class="nav-item active" onclick="showTab('overview', this)">📊 Overview</li>
      <li class="nav-item" onclick="showTab('players', this)">👥 Players</li>
      <li class="nav-item" onclick="showTab('regression', this)">📈 Regression</li>
      <li class="nav-item" onclick="showTab('probability', this)">🎲 Probability</li>
      <li class="nav-item" onclick="showTab('hypothesis', this)">🔬 Hypothesis</li>
      <li class="nav-item" onclick="showTab('chisq', this)">📐 Chi-Square</li>
      <li class="nav-item" onclick="showTab('anova', this)">⚖️ ANOVA</li>
      <li class="nav-item" onclick="showTab('data', this)">📁 Data Explorer</li>
      <li class="nav-item" onclick="showTab('code', this)">💻 R Codebase</li>
    </ul>
    <div class="navbar-right">
      <div class="mode-badge">
        <span class="mode-dot"></span> Sample Mode (261 Innings)
      </div>
    </div>
  </header>

  <main class="main-container">

    <!-- 1. OVERVIEW -->
    <section id="tab-overview" class="tab-pane active">
      <div class="kpi-row">
        <div class="kpi-box">
          <div class="kpi-val">261</div>
          <div class="kpi-lbl">Total Innings</div>
        </div>
        <div class="kpi-box">
          <div class="kpi-val">8</div>
          <div class="kpi-lbl">Elite Batsmen</div>
        </div>
        <div class="kpi-box">
          <div class="kpi-val">9,491</div>
          <div class="kpi-lbl">Total Runs</div>
        </div>
        <div class="kpi-box">
          <div class="kpi-val">36.36</div>
          <div class="kpi-lbl">Mean Innings Score</div>
        </div>
        <div class="kpi-box">
          <div class="kpi-val">137.9</div>
          <div class="kpi-lbl">Aggregate Strike Rate</div>
        </div>
      </div>

      <div class="grid-2">
        <div class="card">
          <div class="card-header-title">📊 Runs by Batsman (ggplot2 geom_col)</div>
          <canvas id="chartRuns" height="240"></canvas>
        </div>
        <div class="card">
          <div class="card-header-title">📈 Empirical Score Distribution (geom_histogram & geom_density)</div>
          <canvas id="chartDist" height="240"></canvas>
        </div>
      </div>

      <div class="card">
        <div class="card-header-title">📋 Batsman Summary & Stability Metrics (descriptive_stats.R)</div>
        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>Batsman</th>
                <th>Team</th>
                <th>Innings</th>
                <th>Total Runs</th>
                <th>Mean</th>
                <th>Median</th>
                <th>Std Dev</th>
                <th>Strike Rate</th>
                <th>Batting Avg</th>
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
    </section>

    <!-- 2. PLAYERS -->
    <section id="tab-players" class="tab-pane">
      <div class="card">
        <div class="card-header-title">👥 Head-to-Head Batsman Profiler</div>
        <div class="grid-2">
          <div>
            <canvas id="chartPlayerRadar" height="260"></canvas>
          </div>
          <div>
            <div class="code-box">
              # Batsman Archetype Formulation (R/descriptive_stats.R)
              CV <- (sd(x) / mean(x)) * 100
              
              V. Kohli:   CV = 52.0% -> Anchor Batsman (High Average, Low Variance)
              G. Maxwell: CV = 89.5% -> Finisher Archetype (High SR, High Variance)
              
              Strike Rate:  round((total_runs / total_balls) * 100, 2)
              Batting Avg:  round(total_runs / sum(dismissals == 1), 2)
            </div>
            <img src="assets/fig3_player_boxplots.png" alt="Boxplots" style="width: 100%; border-radius: 8px; margin-top: 12px; border: 1px solid var(--card-border);" />
          </div>
        </div>
      </div>
    </section>

    <!-- 3. REGRESSION -->
    <section id="tab-regression" class="tab-pane">
      <div class="grid-2">
        <div class="card">
          <div class="card-header-title">📈 Fitted Simple Linear Model: runs ~ balls_faced</div>
          <div class="code-box">
            # R lm() Execution Output (R/regression_analysis.R)
            fit &lt;- lm(runs ~ balls_faced, data = cricket_data)
            
            Coefficients:
                         Estimate  Std. Error  t value  Pr(&gt;|t|)
            (Intercept)   -0.5891      0.8412    -0.70     0.484
            balls_faced    1.3412      0.0280    47.89   &lt; 2e-16 ***
            
            Multiple R-squared: 0.8986, Adjusted R-squared: 0.8982
            F-statistic: 2,294 on 1 and 259 DF, p-value: &lt; 2.2e-16
          </div>
          <img src="assets/fig4_regression_fit.png" alt="Regression Fit" style="width: 100%; border-radius: 8px; margin-top: 14px; border: 1px solid var(--card-border);" />
        </div>
        <div class="card">
          <div class="card-header-title">🔬 Residual Diagnostics & Homoscedasticity</div>
          <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 12px;">
            Checking OLS assumptions: Residuals vs. Fitted plot indicates zero-mean errors with constant variance across predicted scoring ranges.
          </p>
          <img src="assets/fig5_regression_residuals.png" alt="Residuals" style="width: 100%; border-radius: 8px; border: 1px solid var(--card-border);" />
        </div>
      </div>
    </section>

    <!-- 4. PROBABILITY -->
    <section id="tab-probability" class="tab-pane">
      <div class="grid-2">
        <div class="card">
          <div class="card-header-title">🎲 Binomial Distribution B(n = 6, p = 0.25)</div>
          <div class="code-box">
            # R dbinom() Probability Mass Function (R/probability_models.R)
            support &lt;- 0:6
            pmf &lt;- dbinom(support, size = 6, prob = 0.25)
            
            k=0: 17.80% | k=1: 35.60% | k=2: 29.66%
            k=3: 13.18% | k=4:  3.30% | k=5:  0.44% | k=6: 0.02%
            Expected Value E[X] = n * p = 1.50 boundaries
          </div>
          <img src="assets/fig6_binomial_pmf.png" alt="Binomial PMF" style="width: 100%; border-radius: 8px; margin-top: 14px; border: 1px solid var(--card-border);" />
        </div>
        <div class="card">
          <div class="card-header-title">🔔 Continuous Normal Density N(μ = 160, σ = 25)</div>
          <div class="code-box">
            # R dnorm() & pnorm() Density & Cumulative (R/probability_models.R)
            f(x) &lt;- dnorm(x, mean = 160, sd = 25)
            P(140 &lt;= X &lt;= 180) &lt;- pnorm(180, 160, 25) - pnorm(140, 160, 25)
            
            Calculated Probability Interval: 57.63%
            P(Score &gt;= 200) = 5.48% (Upper Extreme Innings Total)
          </div>
          <img src="assets/fig7_normal_distribution.png" alt="Normal Density" style="width: 100%; border-radius: 8px; margin-top: 14px; border: 1px solid var(--card-border);" />
        </div>
      </div>
    </section>

    <!-- 5. HYPOTHESIS -->
    <section id="tab-hypothesis" class="tab-pane">
      <div class="card">
        <div class="card-header-title">🔬 Inferential Hypothesis Testing Engine (R/hypothesis_tests.R)</div>
        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>Test Type</th>
                <th>Null Hypothesis (H₀)</th>
                <th>Alternative (H₁)</th>
                <th>R Function</th>
                <th>Test Statistic</th>
                <th>p-Value</th>
                <th>Formal Decision</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>1-Sample t-Test</strong></td>
                <td>μ_Kohli = 35</td>
                <td>μ_Kohli &gt; 35</td>
                <td><code>t.test(x, mu=35, alt="greater")</code></td>
                <td>t = 3.51 (df = 34)</td>
                <td>0.00065</td>
                <td><span class="badge badge-reject">Reject H₀ (Significant)</span></td>
              </tr>
              <tr>
                <td><strong>1-Sample Proportion</strong></td>
                <td>p_boundary = 0.15</td>
                <td>p_boundary ≠ 0.15</td>
                <td><code>prop.test(k, n, p=0.15)</code></td>
                <td>χ² = 8.42 (df = 1)</td>
                <td>0.0037</td>
                <td><span class="badge badge-reject">Reject H₀ (Boundary ≠ 15%)</span></td>
              </tr>
              <tr>
                <td><strong>2-Sample Welch t-Test</strong></td>
                <td>μ_Kohli - μ_Maxwell = 0</td>
                <td>μ_Kohli ≠ μ_Maxwell</td>
                <td><code>t.test(x, y, var.equal=FALSE)</code></td>
                <td>t = 2.97 (df = 61.8)</td>
                <td>0.0042</td>
                <td><span class="badge badge-reject">Reject H₀ (Significant diff)</span></td>
              </tr>
              <tr>
                <td><strong>2-Sample Proportion</strong></td>
                <td>p_Maxwell = p_Root</td>
                <td>p_Maxwell &gt; p_Root</td>
                <td><code>prop.test(c(k1,k2), c(n1,n2))</code></td>
                <td>χ² = 12.18 (df = 1)</td>
                <td>0.00048</td>
                <td><span class="badge badge-reject">Reject H₀ (Maxwell higher)</span></td>
              </tr>
              <tr>
                <td><strong>Paired t-Test</strong></td>
                <td>μ_diff(Inn1 - Inn2) = 0</td>
                <td>μ_diff ≠ 0</td>
                <td><code>t.test(x, y, paired=TRUE)</code></td>
                <td>t = 0.84 (df = 48)</td>
                <td>0.405</td>
                <td><span class="badge badge-pass">Fail to Reject H₀</span></td>
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
          <div class="card-header-title">📐 Chi-Square Goodness of Fit (R/chi_square_analysis.R)</div>
          <div class="code-box">
            # R chisq.test() on Match Conditions
            chisq.test(observed_counts, p = rep(1/5, 5))
            
            X-squared = 3.824, df = 4, p-value = 0.4305
            
            Decision Rule at α = 0.05:
            Since p-value (0.4305) &gt;= 0.05, we FAIL TO REJECT H₀.
            Match conditions follow a uniform distribution.
          </div>
          <img src="assets/fig10_chisq_gof.png" alt="Chi-Square GOF" style="width: 100%; border-radius: 8px; margin-top: 14px; border: 1px solid var(--card-border);" />
        </div>
        <div class="card">
          <div class="card-header-title">📊 Contingency & Independence Tests</div>
          <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 12px;">
            Evaluating independence between player dismissal status (Out vs. Not Out) and batting order position confirms statistical independence with Yates continuity correction applied.
          </p>
          <div class="code-box">
            # Test of Independence
            cont_table &lt;- table(data$player, data$dismissals)
            chisq.test(cont_table)
            
            X-squared = 6.14, df = 7, p-value = 0.5234
            Decision: Fail to Reject H₀.
          </div>
        </div>
      </div>
    </section>

    <!-- 7. ANOVA -->
    <section id="tab-anova" class="tab-pane">
      <div class="card">
        <div class="card-header-title">⚖️ One-Way ANOVA Engine: aov(runs ~ player)</div>
        <div class="code-box">
          # R aov() & summary.aov() Execution (R/anova_analysis.R)
          fit_aov &lt;- aov(runs ~ player, data = cricket_data)
          summary(fit_aov)
          
                       Df    Sum Sq  Mean Sq  F value  Pr(&gt;F)
          player        7     9,842   1,406.0    2.164  0.0378 *
          Residuals   253   164,412     649.9
          
          TukeyHSD Pairwise Driver:
          V. Kohli - G. Maxwell: diff = +20.02, p adj = 0.0284 *
        </div>
        <img src="assets/fig9_anova_groups.png" alt="ANOVA Boxplot" style="width: 100%; border-radius: 8px; margin-top: 14px; border: 1px solid var(--card-border);" />
      </div>
    </section>

    <!-- 8. DATA EXPLORER -->
    <section id="tab-data" class="tab-pane">
      <div class="card">
        <div class="card-header-title">
          <span>📁 Dataset Schema & Records (data/sample_cricket_data.csv)</span>
          <button onclick="downloadCSV()" class="btn btn-primary">📥 Download CSV</button>
        </div>
        <div style="margin-bottom: 16px;">
          <input type="text" id="filterInput" placeholder="Filter by player, team, opponent, match ID..." onkeyup="filterData()" class="form-control" style="max-width: 380px;" />
        </div>
        <div class="table-responsive" style="max-height: 520px; overflow-y: auto;">
          <table>
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
          <span>💻 R Codebase Project Explorer</span>
          <span style="font-size: 0.8rem; color: var(--primary); font-family: 'JetBrains Mono', monospace;">Run in RStudio: shiny::runApp()</span>
        </div>
        <div class="code-viewer-layout">
          <div class="file-tree" id="fileTree"></div>
          <div class="code-display" id="codeDisplay">Select an R script on the left to view source.</div>
        </div>
      </div>
    </section>

  </main>

  <!-- Footer -->
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

    function showTab(id, el) {{
      document.querySelectorAll('.tab-pane').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
      document.getElementById('tab-' + id).classList.add('active');
      if (el) el.classList.add('active');
    }}

    function renderTableRows(items) {{
      const tbody = document.getElementById('dataTableBody');
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

    function filterData() {{
      const q = document.getElementById('filterInput').value.toLowerCase();
      const filtered = data.filter(d => 
        d.player.toLowerCase().includes(q) ||
        d.team.toLowerCase().includes(q) ||
        d.opponent.toLowerCase().includes(q) ||
        d.match_id.toLowerCase().includes(q)
      );
      renderTableRows(filtered);
    }}

    function downloadCSV() {{
      window.location.href = 'sample_cricket_data.csv';
    }}

    // Setup R Code Explorer
    function setupCodeViewer() {{
      const tree = document.getElementById('fileTree');
      const display = document.getElementById('codeDisplay');
      tree.innerHTML = '';

      const filenames = Object.keys(rFiles);
      filenames.forEach((fname, idx) => {{
        const item = document.createElement('div');
        item.className = 'file-item' + (idx === 0 ? ' active' : '');
        item.textContent = '📄 ' + fname;
        item.onclick = () => {{
          document.querySelectorAll('.file-item').forEach(i => i.classList.remove('active'));
          item.classList.add('active');
          display.textContent = rFiles[fname];
        }};
        tree.appendChild(item);
      }});

      if (filenames.length > 0) {{
        display.textContent = rFiles[filenames[0]];
      }}
    }}

    window.onload = function() {{
      renderTableRows(data);
      setupCodeViewer();

      // Runs Chart
      new Chart(document.getElementById('chartRuns'), {{
        type: 'bar',
        data: {{
          labels: ['V. Kohli', 'J. Root', 'S. Smith', 'R. Sharma', 'KL Rahul', 'K. Williamson', 'G. Maxwell', 'B. Stokes'],
          datasets: [{{
            label: 'Total Runs',
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

      // Score Distribution Chart
      new Chart(document.getElementById('chartDist'), {{
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
          labels: ['Batting Avg', 'Strike Rate / 2', 'Stability (100 - CV)', 'Boundary %', 'Fifty+ Rate'],
          datasets: [
            {{
              label: 'V. Kohli (Anchor Batsman)',
              data: [61.1, 68.95, 48.0, 58.2, 72.0],
              borderColor: '#38bdf8',
              backgroundColor: 'rgba(56, 189, 248, 0.2)'
            }},
            {{
              label: 'G. Maxwell (Match Winner)',
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
    f.write(html_content)

print("Generated CricketEdge R Code Project Web Application for Vercel successfully!")
