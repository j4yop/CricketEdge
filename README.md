# 🏏 CricketEdge — Statistical Cricket Performance Analyzer
### End-to-End RStudio Statistical Computing & Sports Analytics Platform

[![R Version](https://img.shields.io/badge/R-%E2%89%A54.0-blue.svg)](https://www.r-project.org/)
[![Framework](https://img.shields.io/badge/Shiny-1.14+-cyan.svg)](https://shiny.posit.co/)
[![Visuals](https://img.shields.io/badge/ggplot2-3.5+-emerald.svg)](https://ggplot2.tidyverse.org/)
[![Theme](https://img.shields.io/badge/bslib-Dark_Navy-amber.svg)](https://rstudio.github.io/bslib/)
[![Tests](https://img.shields.io/badge/Tests-82%20Passed-brightgreen.svg)]()
[![Deployment](https://img.shields.io/badge/Deployed_App-Vercel-black?logo=vercel&logoColor=white)](https://cricket-edge-analyzer.vercel.app)

> 🚀 **Live Deployed Web Application:** [https://cricket-edge-analyzer.vercel.app](https://cricket-edge-analyzer.vercel.app)

**CricketEdge** is an end-to-end, statistically rigorous sports performance analyzer developed in **R** and **Shiny** for **RStudio**. It bridges university-level statistical theory with modern cricket analytics, allowing users to inspect batting performance, model scoring probabilities, perform inferential hypothesis tests, fit linear regressions, and conduct analysis of variance (ANOVA) with uncompromising graph fidelity.

Every visual plot in CricketEdge is guaranteed to represent the exact mathematical calculations, fitted values, probability densities, and test statistics computed by its underlying base R functions.

---

## 📑 Table of Contents

1. [Project Purpose & Architecture](#1-project-purpose--architecture)
2. [University Syllabus Topics Demonstrated](#2-university-syllabus-topics-demonstrated)
3. [Installation & Setup](#3-installation--setup)
4. [Running the Application](#4-running-the-application)
5. [Data Strategy & Schema](#5-data-strategy--schema)
6. [Statistical Modules & How They Work](#6-statistical-modules--how-they-work)
7. [Graph Fidelity Guarantees](#7-graph-fidelity-guarantees)
8. [Automated Test Suite](#8-automated-test-suite)
9. [Statistical Limitations & Disclaimers](#9-statistical-limitations--disclaimers)
10. [Step-by-Step Professor Demonstration Script](#10-step-by-step-professor-demonstration-script)

---

## 1. Project Purpose & Architecture

CricketEdge was designed to demonstrate applied statistical methodology in RStudio without relying on unnecessary external dependencies, Python runtimes, JavaScript frontends, or opaque machine learning black boxes.

The codebase is strictly modularized to separate data loading, validation, statistical inference, visualization, and Shiny UI:

```
cricketProject/
├── app.R                          # Main Shiny dashboard application (UI + Server)
├── CricketEdge.Rproj              # RStudio Project configuration file
├── requirements.R                 # Automatic dependency verifier and installer
├── README.md                      # Comprehensive technical documentation
├── .gitignore                     # Git ignore rules for RStudio and temporary artifacts
├── data/
│   ├── sample_cricket_data.csv    # 260+ records of reproducible synthetic cricket innings
│   └── cricket_data_template.csv  # Empty CSV template with column headers and sample rows
├── R/
│   ├── data_validation.R          # Schema validation, logical domain constraints, and audit
│   ├── data_loader.R              # Reproducible data generator and CSV loader
│   ├── descriptive_stats.R        # Central tendency, dispersion, tabulations, CV metric
│   ├── regression_analysis.R      # Simple & Multiple linear regression (lm) and diagnostics
│   ├── probability_models.R       # Binomial, Poisson, Normal, and Over simulation engines
│   ├── hypothesis_tests.R         # 1-Sample, 2-Sample, Independent & Paired t-tests & proportions
│   ├── chi_square_analysis.R      # Goodness-of-Fit and Independence contingency tests (chisq.test)
│   ├── anova_analysis.R           # One-Way ANOVA (aov), Tukey HSD post-hoc, and diagnostics
│   ├── plots.R                    # High-fidelity ggplot2 charts in dark-navy sports theme
│   └── report_generation.R        # Dynamic HTML and text report generation engine
├── tests/
│   ├── test_data_validation.R     # Unit tests for schema, zero-balls, and negative bounds
│   ├── test_probability_models.R  # Verification of dbinom, dpois, dnorm, and simulation properties
│   └── test_statistical_results.R # Verification of regression, ANOVA, and hypothesis calculations
└── reports/
    └── .gitkeep                   # Destination directory for exported statistical reports
```

---

## 2. University Syllabus Topics Demonstrated

CricketEdge maps directly to standard R laboratory statistical experiments:

| # | Syllabus Experiment Topic | CricketEdge Implementation & Module |
|---|---------------------------|-------------------------------------|
| **1** | **Data Types, Data Frames, Import/Export** | `R/data_loader.R`, `R/data_validation.R`: CSV import/export, typed columns, derived metrics (`strike_rate`, `boundary_pct`), missing value reports. |
| **2** | **Descriptive Statistics & Tabulations** | `R/descriptive_stats.R`, `Tab 1 (Overview)`: Mean, Median, SD, IQR, tabulations by venue/condition, boxplots, histograms. |
| **3** | **Correlation & Simple Linear Regression** | `R/regression_analysis.R`, `Tab 4`: Pearson $r$ test (`cor.test`), `lm(runs ~ balls_faced)`, slope/intercept interpretation, residuals vs fitted. |
| **4** | **Multiple Regression & Coefficient of Determination** | `R/regression_analysis.R`, `Tab 4`: `lm(runs ~ balls_faced + fours + sixes)`, $R^2$, Adjusted $R^2$, F-test, collinearity explanation. |
| **5** | **Binomial Probability Distribution** | `R/probability_models.R`, `Tab 5`: `dbinom()`, `pbinom()`, `qbinom()`, `rbinom()`, discrete spike plot `plot(x, px, type="h")` semantics. |
| **6** | **Poisson & Normal Distributions** | `R/probability_models.R`, `Tab 5`: `dpois()`, `ppois()`, `dnorm()`, `pnorm()`, shaded integral region, over simulation engine. |
| **7** | **One-Sample Hypothesis Tests** | `R/hypothesis_tests.R`, `Tab 6`: `t.test(x, mu = mu0)` for batsman mean runs, `prop.test()` for boundary rates against benchmark $p_0$. |
| **8** | **Two-Sample Hypothesis Tests** | `R/hypothesis_tests.R`, `Tab 6`: Two-sample mean comparison and two-sample proportion comparison with one-sided and two-sided alternatives. |
| **9** | **Independent and Paired-Sample t-Tests** | `R/hypothesis_tests.R`, `Tab 6`: Independent Welch's vs Student's t-test (`var.equal=TRUE/FALSE`); Paired t-test on 1st vs 2nd innings totals. |
| **10** | **Chi-Square Goodness-of-Fit & Independence** | `R/chi_square_analysis.R`, `Tab 7`: `chisq.test()` Goodness-of-fit against uniform expectations; Test of independence on contingency tables; Cochran's rule check ($E_i < 5$). |
| **11** | **ANOVA & Multiple Comparisons** | `R/anova_analysis.R`, `Tab 8`: One-way ANOVA `aov()`, Bartlett's test for variance homogeneity, Shapiro-Wilk for normality, Tukey HSD post-hoc. |

---

## 3. Installation & Setup

### Prerequisites
- R (Version $\ge 4.0$, tested on R 4.5.2)
- RStudio Desktop (or command-line R)

### Install Required Dependencies
In R or RStudio Console, run:

```r
# Automatic installer and dependency checker:
source("requirements.R")
```

Or install the small, focused set of packages manually from CRAN:

```r
install.packages(c("shiny", "ggplot2", "bslib", "dplyr", "readr", "testthat"))
```

---

## 4. Running the Application

### Option A: From RStudio (Recommended)
1. Double-click `CricketEdge.Rproj` to open the project in RStudio.
2. Open `app.R` in the editor.
3. Click the **Run App** button in the top right corner of the script panel (or press `Ctrl+Shift+Enter`).

### Option B: From the R Console or Terminal
Run:

```r
shiny::runApp()
```

Or from your bash terminal:

```bash
Rscript -e "shiny::runApp(port = 3838, host = '0.0.0.0')"
```

The application will launch and open in your default browser or RStudio Viewer pane.

---

## 5. Data Strategy & Schema

CricketEdge supports two completely separated modes without confusing results:

### A. Sample Data Mode (Deterministic & Offline)
- Contains a reproducible synthetic dataset of over 260 innings across 8 world-class batsmen (*V. Kohli, R. Sharma, J. Root, S. Smith, K. Williamson, B. Stokes, G. Maxwell, KL Rahul*).
- Generated deterministically via `generate_synthetic_cricket_data(seed = 42)` in `R/data_loader.R`.
- Requires zero internet connection.
- Clearly watermarked across the UI as **"Sample Demonstration Data (Synthetic)"**.

### B. Real Data Mode (User Uploaded CSV)
- Upload any custom match dataset via **Data Explorer > Upload Cricket CSV**.
- Validated before ingestion against the documented schema:

| Column | Type | Domain Constraint | Description |
|--------|------|-------------------|-------------|
| `match_id` | Character | Non-empty | Unique match identifier (e.g. `M101`) |
| `date` | Date | `YYYY-MM-DD` | Date of match |
| `player` | Character | Non-empty | Batsman's full name |
| `team` | Character | Non-empty | Batsman's team |
| `opponent` | Character | Non-empty | Opponent team |
| `venue` | Character | Non-empty | Stadium / venue name |
| `innings` | Integer | `1` or `2` | 1 = Batted 1st, 2 = Chased |
| `batting_position` | Integer | `1` to `11` | Batting order position |
| `runs` | Numeric | $\ge 0$ | Runs scored by the batsman |
| `balls_faced` | Numeric | $\ge 0$ | Deliveries faced |
| `fours` | Numeric | $\ge 0$ | Fours hit |
| `sixes` | Numeric | $\ge 0$ | Sixes hit |
| `dismissals` | Numeric | `0` or `1` | 1 = Out, 0 = Not Out |
| `wickets_lost` | Numeric | `0` to `10` | Team wickets down at innings close |
| `innings_total` | Numeric | $\ge 0$ | Total team innings score |
| `overs` | Numeric | $\ge 1$ | Scheduled match overs (e.g. 20) |
| `match_condition` | Character | Categorical | Condition (e.g. `Day`, `Day/Night`, `Overcast`, `Dry/Spin`) |

#### Mathematical Consistency Constraints Enforced
1. **Boundary Lower Bound**: $4 \times \text{fours} + 6 \times \text{sixes} \le \text{runs}$. If violated, a warning is raised and the data is audited.
2. **Safe Strike Rate**: Computed as $\frac{\text{runs}}{\text{balls\_faced}} \times 100$. If `balls_faced == 0`, strike rate is safely set to `0.0` (preventing `NaN` or `Inf` crashes).
3. **Batting Average**: Computed as $\frac{\text{Total Runs}}{\sum \text{dismissals}}$. In instances of 0 dismissals, it is cleanly labeled `"Undef (0 Outs)"` rather than crashing numerical summaries.

---

## 6. Statistical Modules & How They Work

### 1. Overview & Descriptive Statistics
- Computes aggregate metrics ($N$, total runs, mean, median, standard deviation, interquartile range, overall strike rate, boundary %).
- Tabulates scores across match conditions and venues.
- Plots empirical distributions with overlaid mean (dashed green line) and median (dotted red line).

### 2. Player Comparison & Consistency
- Enables multi-batsman side-by-side benchmarking.
- Displays distribution boxplots with overlaid raw jittered observations and diamond mean markers.
- **Consistency Metric**: Formulated using the **Coefficient of Variation**:
  $$\text{CV} = \left(\frac{\text{Standard Deviation}}{\text{Mean Runs}}\right) \times 100$$
  *Interpretation*: Lower CV signifies lower relative dispersion and higher scoring consistency.

### 3. Correlation & Linear Regression
- Fits Simple Linear Regression: $\text{runs} = \beta_0 + \beta_1 \cdot \text{balls\_faced}$.
- Fits Multiple Linear Regression: $\text{runs} = \beta_0 + \beta_1 \cdot \text{balls} + \beta_2 \cdot \text{4s} + \beta_3 \cdot \text{6s}$.
- Displays ANOVA F-test, $R^2$, Adjusted $R^2$, standard errors, and significance codes.
- Diagnostic plot: Residuals ($e_i = y_i - \hat{y}_i$) vs. Fitted values ($\hat{y}_i$) to evaluate homoscedasticity and linearity assumptions.
- Explicitly warns that regressing runs on boundaries reflects an arithmetic decomposition rather than an exogenous causal mechanism.

### 4. Probability Lab
- **Binomial Distribution**: $X \sim B(n, p)$ using `dbinom()`, `pbinom()`, and `rbinom()`. Visualized via discrete spikes matching base R `plot(x, px, type = "h")`.
- **Poisson Distribution**: $X \sim \text{Pois}(\lambda)$ using `dpois()` and `ppois()`. Visualized over discrete integer support with theoretical mean $\lambda$ and variance $\lambda$.
- **Normal Distribution**: $X \sim N(\mu, \sigma)$ using `dnorm()` and `pnorm()`. Renders continuous bell density with exact shaded cumulative probability intervals.
- **Cricket Over Simulator**: Simulates $M$ overs from a transparent categorical ball-by-ball distribution:
  $$\text{Outcomes} \in \{0, 1, 2, 3, 4, 6\} \quad \text{with probabilities } \{p_0, p_1, p_2, p_3, p_4, p_6\}$$
  Computes empirical frequencies vs. theoretical expectation $E[\text{Over}] = 6 \cdot E[\text{Ball}]$ and empirical probability of reaching target runs.

### 5. Inferential Hypothesis Testing
- **1-Sample t-Test**: Tests whether a player's true mean score differs from benchmark $\mu_0$ via `t.test()`.
- **1-Sample Proportion Test**: Tests whether boundary proportion differs from benchmark $p_0$ via `prop.test()`.
- **2-Sample Independent t-Test**: Compares two batsmen or conditions; allows toggling between Welch's t-test (unequal variance) and Student's t-test (`var.equal = TRUE`).
- **Paired t-Test**: Compares 1st Innings vs 2nd Innings totals across identical matches where both innings were played (`t.test(paired = TRUE)`).
- Outputs $H_0$, $H_1$, test statistic, df, p-value, and confidence interval. Decisions strictly avoid writing "accept $H_0$".

### 6. Chi-Square Contingency Analysis
- **Goodness-of-Fit**: Tests whether innings counts across match conditions conform to uniform expectations $\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$.
- **Test of Independence**: Analyzes $r \times c$ contingency tables (e.g. Batsman vs. Score Category: Low / Medium / Fifty / Century).
- Automatically executes **Cochran's Rule Audit**: Alerts the user if any expected cell count $E_i < 1$ or if $> 20\%$ of cells have $E_i < 5$.

### 7. One-Way ANOVA & Group Means
- Fits $F$-test via `aov(runs ~ group)` across batsmen, conditions, or batting positions.
- Generates complete ANOVA source table: Sum of Squares, Mean Squares, $F$-statistic, and $\text{Pr}(>F)$.
- **Diagnostic Checks**: Bartlett's test for variance homogeneity (`bartlett.test`) and Shapiro-Wilk test for residual normality (`shapiro.test`).
- **Post-Hoc Analysis**: Computes Tukey's Honest Significant Difference (`TukeyHSD()`) with family-wise error rate control.

### 8. Dynamic Statistical Report
- Generates a downloadable, self-contained HTML or plain-text statistical report incorporating all currently active calculations, models, and filter parameters.

---

## 7. Graph Fidelity Guarantees

Every visualization in CricketEdge adheres to strict scientific fidelity rules:
1. **Pre-computation in R**: Data is calculated in pure R before rendering.
2. **Exact Fitted Lines**: Regression lines are drawn directly from fitted model predictions `fitted(lm)`, never fabricated.
3. **Exact Probability Densities**: Normal curves use exact `dnorm()` densities; shaded regions match `pnorm()` integrals.
4. **Discrete Semantics**: Binomial and Poisson graphs represent mass functions as discrete impulses/needles, matching base R `type = "h"` conventions.
5. **No Data Distortion**: Axes are never truncated or warped to falsely exaggerate variance.
6. **Dynamic Filter Reactivity**: Every chart automatically updates when filters are modified.

---

## 8. Automated Test Suite

CricketEdge includes an extensive test suite built with `testthat`, covering all 12 validation requirements.

To run the full test suite in RStudio or Terminal:

```r
testthat::test_dir("tests")
```

### Verified Test Results
```
✔ | Context
✔ | data_validation        [13 tests passed]
✔ | probability_models     [30 tests passed]
✔ | statistical_results    [39 tests passed]

══ Results ═════════════════════════════════════════════════════════════════════
Duration: 3.8 s
[ FAIL 0 | WARN 0 | SKIP 0 | PASS 82 ]
```

All 82 assertions verify:
- Binomial and Poisson probabilities sum to $1.00$.
- Theoretical means and variances match $n \cdot p$ and $\lambda$.
- Safe division by zero for strike-rate calculations.
- Exact agreement between CricketEdge outputs and `lm()`, `aov()`, `t.test()`, `prop.test()`, and `chisq.test()`.
- Plotted ggplot data layers match mathematical density vectors.
- Strict determinism of synthetic data generation with `set.seed()`.

---

## 9. Statistical Limitations & Disclaimers

1. **Accounting Decomposition vs. Causality**:
   Regressing runs against boundaries ($4\text{s}$ and $6\text{s}$) produces an extremely high $R^2$. This is an arithmetic accounting identity ($runs = 4 \times 4s + 6 \times 6s + \text{singles}$), not an independent exogenous causal finding.
2. **Clustered Independence in Tournament Play**:
   Observations from consecutive matches at the same stadium may be subject to shared pitch and environmental conditions, violating strict i.i.d. independence.
3. **Simplified Over Simulation**:
   The over scoring simulator treats ball outcomes as independent draws from a multinomial distribution. In actual cricket, deliveries within an over exhibit strategic dependencies based on match state, bowler tactics, and pitch wear.

---

## 10. Step-by-Step Professor Demonstration Script

When presenting CricketEdge to your university professor or evaluation committee, follow this recommended 5-minute walkthrough:

```
Step 1: Introduction & Data Integrity (Tab 1: Overview)
- Open the application. Highlight the active "Sample Demonstration Data" badge.
- Point to the KPI cards: Sample size (261 innings), total aggregate runs, mean runs, and overall strike rate.
- Show the filter panel: Select "V. Kohli" and "R. Sharma", and demonstrate how both the KPI numbers and plots update instantly.
- Click "Reset All Filters".

Step 2: Schema & Validation (Tab 2: Data Explorer)
- Switch to Tab 2. Point out the Schema Reference table and Missing Values Audit.
- Explain the domain constraints: Non-negative runs, boundary consistency check, and safe handling of zero balls faced.

Step 3: Player Comparison & Consistency (Tab 3: Player Comparison)
- Compare "V. Kohli", "R. Sharma", "J. Root", and "G. Maxwell".
- Show the boxplot with jittered innings observations and mean diamonds.
- Explain the Consistency Metric (CV %): "Notice that lower CV values reflect lower relative variance, indicating a more consistent scoring anchor, while higher CV indicates an aggressive, high-variance match-winner."

Step 4: Linear Modeling & Diagnostics (Tab 4: Correlation & Regression)
- Select Simple Linear Regression (Runs ~ Balls Faced).
- Point out the fitted equation, t-statistic, and p-value.
- Switch to Multiple Regression (Runs ~ Balls + 4s + 6s) and explain the high R²:
  "Professor, notice that R² jumps to >0.90 because boundaries directly constitute runs. In our code, we explicitly document this as an accounting decomposition rather than false causality."

Step 5: Probability Distributions & Simulation (Tab 5: Probability Lab)
- Binomial Tab: Demonstrate n = 6 balls, p = 0.25, showing the discrete spike plot matching base R dbinom().
- Normal Tab: Change the interval bounds to demonstrate real-time pnorm() area calculation.
- Cricket Simulator: Click "Rerun Simulation" to show empirical over totals converging toward the theoretical normal profile (CLT).

Step 6: Inferential Testing & ANOVA (Tabs 6, 7, 8)
- Tab 6: Run a Two-Sample Welch's t-test comparing V. Kohli vs G. Maxwell. Highlight that the app states "Fail to Reject H₀" or "Reject H₀" rather than naively "accepting" the null.
- Tab 7: Show Chi-Square Goodness-of-Fit and the automated Cochran's Rule audit.
- Tab 8: Run One-Way ANOVA across Batsmen. Show the F-statistic, Bartlett's test for homogeneity of variance, and Tukey's HSD post-hoc table.

Step 7: Statistical Report Export (Tab 9: Report)
- Click "Download HTML Report". Open the generated document to demonstrate the automated summary containing all computed statistics, tables, and methodology notes.
```
