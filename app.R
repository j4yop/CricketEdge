# ==============================================================================
# CricketEdge — Statistical Cricket Performance Analyzer
# Interactive Shiny Web Application (Polished Modern UI)
# ==============================================================================

suppressPackageStartupMessages({
  library(shiny)
  library(bslib)
  library(ggplot2)
})

# Source modular analytical backends
source("R/data_validation.R")
source("R/data_loader.R")
source("R/descriptive_stats.R")
source("R/regression_analysis.R")
source("R/probability_models.R")
source("R/hypothesis_tests.R")
source("R/chi_square_analysis.R")
source("R/anova_analysis.R")
source("R/plots.R")
source("R/report_generation.R")

# Ensure sample files exist on disk
if (!file.exists("data/sample_cricket_data.csv")) {
  create_sample_csv_files("data")
}

# ------------------------------------------------------------------------------
# THEME & MODERN CSS STYLING
# ------------------------------------------------------------------------------
app_theme <- bs_theme(
  version = 5,
  bg = "#f8fafc",
  fg = "#0f172a",
  primary = "#0284c7",
  secondary = "#64748b",
  success = "#059669",
  warning = "#d97706",
  danger = "#e11d48"
)

custom_css <- "
  /* Global Modern Slim Scrollbars */
  ::-webkit-scrollbar {
    width: 6px;
    height: 6px;
  }
  ::-webkit-scrollbar-track {
    background: transparent;
  }
  ::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 9999px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
  }
  * {
    scrollbar-width: thin;
    scrollbar-color: #cbd5e1 transparent;
  }

  /* Global Layout & Fonts */
  body {
    background-color: #f8fafc !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif !important;
    color: #334155 !important;
    overflow-x: hidden;
  }
  
  /* Navbar Enhancements - Light Athletic Header */
  .navbar {
    background: #ffffff !important;
    border-bottom: 1px solid #e2e8f0 !important;
    padding: 0.4rem 1.4rem !important;
    box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.04) !important;
  }
  .navbar-brand {
    font-size: 1.18rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.4px !important;
    color: #0f172a !important;
    padding-right: 15px !important;
  }
  .navbar-nav {
    display: flex !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    gap: 3px !important;
  }
  .nav-item .nav-link {
    font-size: 0.83rem !important;
    font-weight: 600 !important;
    padding: 0.45rem 0.75rem !important;
    border-radius: 7px !important;
    color: #64748b !important;
    white-space: nowrap !important;
    transition: all 0.15s ease-in-out !important;
    border: 1px solid transparent !important;
  }
  .nav-item .nav-link:hover {
    color: #0f172a !important;
    background: #f1f5f9 !important;
  }
  .nav-item .nav-link.active {
    color: #0284c7 !important;
    background: #f0f9ff !important;
    border: 1px solid #bae6fd !important;
    box-shadow: none !important;
  }

  /* Sleek Modern Light Cards */
  .card-box {
    background: #ffffff !important;
    border-radius: 10px !important;
    padding: 20px !important;
    border: 1px solid #e2e8f0 !important;
    margin-bottom: 20px !important;
    box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.03) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
  }
  .card-box:hover {
    border-color: #cbd5e1 !important;
    box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.05) !important;
  }
  .card-header-title {
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
    margin-bottom: 12px !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
  }
  
  /* Filter Sidebar */
  .filter-panel {
    background: #ffffff !important;
    border-radius: 10px !important;
    padding: 18px !important;
    border: 1px solid #e2e8f0 !important;
    margin-bottom: 20px !important;
    box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.03) !important;
  }

  /* KPI Cards with Refined Light Elevation */
  .kpi-card {
    background: #ffffff !important;
    border-radius: 10px !important;
    padding: 16px 18px !important;
    border: 1px solid #e2e8f0 !important;
    border-top: 3px solid #0284c7 !important;
    margin-bottom: 18px !important;
    box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.03) !important;
    position: relative !important;
    overflow: hidden !important;
    transition: transform 0.15s ease !important;
  }
  .kpi-card:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.05) !important;
  }
  .kpi-card.emerald { border-top-color: #059669 !important; }
  .kpi-card.amber { border-top-color: #d97706 !important; }
  .kpi-card.rose { border-top-color: #e11d48 !important; }
  .kpi-num {
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    line-height: 1.2 !important;
    letter-spacing: -0.5px !important;
    font-feature-settings: 'tnum' 1 !important;
  }
  .kpi-label {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    color: #64748b !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    margin-top: 4px !important;
  }
  
  /* Badges & Indicators */
  .mode-indicator {
    padding: 6px 14px !important;
    border-radius: 20px !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    margin-bottom: 16px !important;
  }
  .mode-sample {
    background: #f0f9ff !important;
    border: 1px solid #bae6fd !important;
    color: #0284c7 !important;
  }
  .mode-real {
    background: #ecfdf5 !important;
    border: 1px solid #a7f3d0 !important;
    color: #059669 !important;
  }
  .stat-badge {
    background: #ecfdf5 !important;
    color: #059669 !important;
    border: 1px solid #a7f3d0 !important;
    font-weight: 700 !important;
    padding: 4px 10px !important;
    border-radius: 6px !important;
    font-size: 0.78rem !important;
    display: inline-block !important;
  }
  .stat-badge-danger {
    background: #fff1f2 !important;
    color: #e11d48 !important;
    border: 1px solid #fecdd3 !important;
    font-weight: 700 !important;
    padding: 4px 10px !important;
    border-radius: 6px !important;
    font-size: 0.78rem !important;
    display: inline-block !important;
  }

  /* Math & Formula Boxes */
  .math-formula {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-left: 4px solid #0284c7 !important;
    border-radius: 7px !important;
    padding: 10px 14px !important;
    font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    font-size: 0.81rem !important;
    color: #0f172a !important;
    margin: 10px 0 !important;
    line-height: 1.5 !important;
  }

  /* High Quality Tables with NO Awkward Text Wrapping */
  .table-responsive-custom {
    max-height: 480px !important;
    overflow-x: auto !important;
    overflow-y: auto !important;
    border-radius: 8px !important;
    border: 1px solid #e2e8f0 !important;
    background: #ffffff !important;
  }
  .table-responsive-custom::-webkit-scrollbar {
    width: 6px !important;
    height: 6px !important;
  }
  .table-responsive-custom::-webkit-scrollbar-thumb {
    background: #cbd5e1 !important;
    border-radius: 3px !important;
  }
  .table-responsive-custom table {
    margin-bottom: 0 !important;
    width: 100% !important;
  }
  .table {
    color: #334155 !important;
    font-size: 0.84rem !important;
  }
  .table thead th {
    background-color: #f8fafc !important;
    color: #475569 !important;
    font-weight: 700 !important;
    font-size: 0.74rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    border-bottom: 1px solid #e2e8f0 !important;
    white-space: nowrap !important;
    padding: 10px 12px !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 2 !important;
  }
  .table tbody td {
    border-bottom: 1px solid #f1f5f9 !important;
    white-space: nowrap !important;
    padding: 9px 12px !important;
    vertical-align: middle !important;
    background: #ffffff !important;
  }
  .table tbody tr:hover td {
    background-color: #f8fafc !important;
  }

  /* Form Controls & Inputs */
  .form-control, .selectize-input {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 7px !important;
    font-size: 0.85rem !important;
    transition: all 0.15s ease !important;
  }
  .form-control:focus, .selectize-input.focus {
    border-color: #0284c7 !important;
    box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.12) !important;
  }
  .selectize-dropdown {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    color: #0f172a !important;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.08) !important;
  }
  .selectize-dropdown .option {
    color: #334155 !important;
    padding: 8px 12px !important;
  }
  .selectize-dropdown .active {
    background-color: #f0f9ff !important;
    color: #0284c7 !important;
  }
  .selectize-control.multi .selectize-input > div {
    background: #0f172a !important;
    color: #ffffff !important;
    border-radius: 4px !important;
    padding: 2px 7px !important;
  }
  
  /* Tactile Buttons */
  .btn-primary {
    background: #0f172a !important;
    border: 1px solid #0f172a !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border-radius: 7px !important;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.08) !important;
    transition: all 0.15s ease !important;
  }
  .btn-primary:hover {
    background: #1e293b !important;
    border-color: #1e293b !important;
    transform: translateY(-1px) !important;
  }
  .btn-secondary {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    color: #334155 !important;
    font-weight: 600 !important;
    border-radius: 7px !important;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04) !important;
    transition: all 0.15s ease !important;
  }
  .btn-secondary:hover {
    background: #f8fafc !important;
    border-color: #94a3b8 !important;
    color: #0f172a !important;
  }
  .btn-outline-secondary {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    color: #475569 !important;
    border-radius: 7px !important;
  }
  .btn-outline-secondary:hover {
    background: #f8fafc !important;
    color: #0f172a !important;
    border-color: #94a3b8 !important;
  }
"

# ------------------------------------------------------------------------------
# UI DEFINITION
# ------------------------------------------------------------------------------
ui <- navbarPage(
  title = span("🏏 CricketEdge", style = "font-weight: 800; color: #38bdf8; font-size: 1.25rem; letter-spacing: -0.5px;"),
  theme = app_theme,
  header = tags$head(tags$style(HTML(custom_css))),
  
  # ----------------------------------------------------------------------------
  # TAB 1: OVERVIEW
  # ----------------------------------------------------------------------------
  tabPanel(
    "📊 Overview",
    fluidRow(
      column(12, uiOutput("active_mode_banner"))
    ),
    fluidRow(
      # Filters Sidebar
      column(
        3,
        div(
          class = "filter-panel",
          div(class = "card-header-title", "⚡ Dataset Filters"),
          p("Dynamic multi-parameter filtering applied across all analytical tabs.", style = "font-size: 11.5px; color: #94a3b8; margin-bottom: 12px;"),
          uiOutput("filter_player_ui"),
          uiOutput("filter_condition_ui"),
          uiOutput("filter_innings_ui"),
          actionButton("reset_filters", "↺ Reset All Filters", class = "btn-secondary btn-sm w-100", style = "margin-top: 10px;")
        )
      ),
      # Main Visualizations & KPIs
      column(
        9,
        fluidRow(
          column(3, div(class = "kpi-card", div(class = "kpi-num", textOutput("kpi_innings")), div(class = "kpi-label", "Innings Sampled"))),
          column(3, div(class = "kpi-card emerald", div(class = "kpi-num", textOutput("kpi_runs")), div(class = "kpi-label", "Aggregate Runs"))),
          column(3, div(class = "kpi-card amber", div(class = "kpi-num", textOutput("kpi_mean_runs")), div(class = "kpi-label", "Mean Runs / Inn"))),
          column(3, div(class = "kpi-card rose", div(class = "kpi-num", textOutput("kpi_strike_rate")), div(class = "kpi-label", "Overall Strike Rate")))
        ),
        fluidRow(
          column(
            6,
            div(
              class = "card-box",
              plotOutput("plot_overview_players", height = "350px")
            )
          ),
          column(
            6,
            div(
              class = "card-box",
              plotOutput("plot_overview_dist", height = "350px")
            )
          )
        ),
        fluidRow(
          column(
            12,
            div(
              class = "card-box",
              div(class = "card-header-title", "📋 Batsman Performance Breakdown"),
              div(class = "table-responsive-custom", tableOutput("table_overview_players"))
            )
          )
        )
      )
    )
  ),
  
  # ----------------------------------------------------------------------------
  # TAB 2: DATA EXPLORER
  # ----------------------------------------------------------------------------
  tabPanel(
    "📁 Data",
    fluidRow(
      column(
        4,
        div(
          class = "card-box",
          div(class = "card-header-title", "📂 Data Ingestion Mode"),
          radioButtons(
            "data_source_mode",
            label = NULL,
            choices = c("Sample Demonstration Data (Synthetic)" = "sample", "User Uploaded CSV (Real Data Mode)" = "upload"),
            selected = "sample"
          ),
          conditionalPanel(
            condition = "input.data_source_mode == 'upload'",
            fileInput("user_csv_file", "Upload CSV Dataset:", accept = c(".csv", "text/csv")),
            p("Must match required 17-column schema.", style = "font-size: 11px; color: #94a3b8;")
          ),
          hr(style = "border-color: rgba(255,255,255,0.08);"),
          div(class = "card-header-title", "💾 Export & Template"),
          downloadButton("download_cleaned_data", "Download Cleaned CSV", class = "btn-primary btn-sm mb-2 w-100"),
          downloadButton("download_csv_template", "Download CSV Template", class = "btn-outline-secondary btn-sm w-100")
        ),
        div(
          class = "card-box",
          div(class = "card-header-title", "🛡️ Validation & Constraints"),
          uiOutput("validation_status_ui"),
          hr(style = "border-color: rgba(255,255,255,0.08);"),
          h6("Missing Values Audit", style = "color: #94a3b8; font-size: 11px; text-transform: uppercase; font-weight: 700;"),
          div(class = "table-responsive-custom", style = "max-height: 220px;", tableOutput("missing_values_table"))
        )
      ),
      column(
        8,
        div(
          class = "card-box",
          div(
            style = "display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;",
            div(class = "card-header-title", style = "margin-bottom: 0;", "🔍 Dataset Preview"),
            uiOutput("dataset_dimensions_ui")
          ),
          div(class = "table-responsive-custom", tableOutput("data_preview_table"))
        ),
        div(
          class = "card-box",
          div(class = "card-header-title", "📖 Schema Reference & Domain Rules"),
          div(class = "table-responsive-custom", style = "max-height: 300px;", tableOutput("schema_table"))
        )
      )
    )
  ),
  
  # ----------------------------------------------------------------------------
  # TAB 3: PLAYER COMPARISON
  # ----------------------------------------------------------------------------
  tabPanel(
    "👥 Players",
    fluidRow(
      column(
        4,
        div(
          class = "card-box",
          div(class = "card-header-title", "⚙️ Comparison Parameters"),
          uiOutput("compare_players_picker_ui"),
          selectInput(
            "compare_metric_choice",
            "Benchmarking Metric:",
            choices = c(
              "Batting Average" = "BattingAverageNum",
              "Strike Rate" = "StrikeRate",
              "Total Runs" = "TotalRuns",
              "Mean Runs" = "MeanRuns",
              "Boundary Percentage (%)" = "BoundaryPct",
              "Consistency Metric (CV %)" = "CV_Pct"
            ),
            selected = "BattingAverageNum"
          ),
          div(
            class = "math-formula",
            "Consistency Metric = CV = (SD / Mean) × 100\nLower CV signifies greater scoring stability."
          ),
          p(
            "Note: Cricket scoring is multidimensional. Avoid ranking players universally superior based on a single metric.",
            style = "font-size: 11.5px; color: #94a3b8;"
          )
        )
      ),
      column(
        8,
        div(
          class = "card-box",
          plotOutput("plot_player_boxplots", height = "360px")
        )
      )
    ),
    fluidRow(
      column(
        6,
        div(
          class = "card-box",
          plotOutput("plot_player_bars", height = "320px")
        )
      ),
      column(
        6,
        div(
          class = "card-box",
          plotOutput("plot_player_scatter", height = "320px")
        )
      )
    ),
    fluidRow(
      column(
        12,
        div(
          class = "card-box",
          div(class = "card-header-title", "📊 Comprehensive Player Comparison Matrix"),
          div(class = "table-responsive-custom", tableOutput("table_player_comparison"))
        )
      )
    )
  ),
  
  # ----------------------------------------------------------------------------
  # TAB 4: CORRELATION & REGRESSION
  # ----------------------------------------------------------------------------
  tabPanel(
    "📈 Regression",
    fluidRow(
      column(
        4,
        div(
          class = "card-box",
          div(class = "card-header-title", "⚙️ Model Specification"),
          radioButtons(
            "reg_model_type",
            "Linear Model Formulation:",
            choices = c("Simple Linear (Runs ~ Balls Faced)" = "simple",
                        "Multiple Linear (Runs ~ Balls + 4s + 6s)" = "multiple"),
            selected = "simple"
          ),
          conditionalPanel(
            condition = "input.reg_model_type == 'simple'",
            selectInput("simple_reg_predictor", "Predictor Variable (X):",
                        choices = c("Balls Faced" = "balls_faced", "Fours" = "fours", "Sixes" = "sixes", "Batting Position" = "batting_position"),
                        selected = "balls_faced")
          ),
          hr(style = "border-color: rgba(255,255,255,0.08);"),
          h6("Fitted Model Equation", style = "color: #f59e0b; font-size: 11px; text-transform: uppercase; font-weight: 700;"),
          uiOutput("reg_equation_ui"),
          hr(style = "border-color: rgba(255,255,255,0.08);"),
          h6("Goodness of Fit Diagnostics", style = "color: #38bdf8; font-size: 11px; text-transform: uppercase; font-weight: 700;"),
          uiOutput("reg_metrics_ui"),
          div(
            class = "math-formula",
            "R² = 1 - (SS_res / SS_tot)\nF = MS_reg / MS_res"
          )
        )
      ),
      column(
        8,
        div(
          class = "card-box",
          plotOutput("plot_regression_fit", height = "330px")
        ),
        div(
          class = "card-box",
          plotOutput("plot_regression_resids", height = "280px")
        )
      )
    ),
    fluidRow(
      column(
        12,
        div(
          class = "card-box",
          div(class = "card-header-title", "📐 Parameter Estimates & Statistical Interpretation"),
          div(class = "table-responsive-custom", tableOutput("table_regression_coefs")),
          uiOutput("reg_interpretation_ui")
        )
      )
    )
  ),
  
  # ----------------------------------------------------------------------------
  # TAB 5: PROBABILITY LAB
  # ----------------------------------------------------------------------------
  tabPanel(
    "🎲 Probability",
    tabsetPanel(
      # Binomial
      tabPanel(
        "Binomial B(n, p)",
        br(),
        fluidRow(
          column(
            4,
            div(
              class = "card-box",
              div(class = "card-header-title", "Binomial Parameters"),
              p("Models discrete successes in n independent Bernoulli trials (e.g. boundary occurrence in an over).", style = "font-size: 11.5px; color: #94a3b8;"),
              sliderInput("binom_n", "Number of Trials (n balls):", min = 1, max = 30, value = 6, step = 1),
              sliderInput("binom_p", "Success Probability (p):", min = 0.01, max = 0.99, value = 0.25, step = 0.01),
              numericInput("binom_k", "Target Value (k):", value = 2, min = 0, max = 30, step = 1),
              div(
                class = "math-formula",
                "P(X = k) = (n choose k) * p^k * (1-p)^(n-k)\nE[X] = n*p | Var(X) = n*p*(1-p)"
              ),
              uiOutput("binom_metrics_ui")
            )
          ),
          column(
            8,
            div(
              class = "card-box",
              plotOutput("plot_binom", height = "400px")
            )
          )
        )
      ),
      # Poisson
      tabPanel(
        "Poisson Pois(λ)",
        br(),
        fluidRow(
          column(
            4,
            div(
              class = "card-box",
              div(class = "card-header-title", "Poisson Parameters"),
              p("Models event counts over a fixed interval (e.g. wickets or sixes per match).", style = "font-size: 11.5px; color: #94a3b8;"),
              sliderInput("pois_lambda", "Rate Parameter (λ):", min = 0.2, max = 15, value = 2.5, step = 0.1),
              numericInput("pois_k", "Target Count (k):", value = 3, min = 0, max = 30, step = 1),
              div(
                class = "math-formula",
                "P(X = k) = (λ^k * e^(-λ)) / k!\nE[X] = Var(X) = λ"
              ),
              uiOutput("pois_metrics_ui")
            )
          ),
          column(
            8,
            div(
              class = "card-box",
              plotOutput("plot_pois", height = "400px")
            )
          )
        )
      ),
      # Normal
      tabPanel(
        "Normal N(μ, σ)",
        br(),
        fluidRow(
          column(
            4,
            div(
              class = "card-box",
              div(class = "card-header-title", "Normal Parameters"),
              p("Continuous density with shaded probability integration.", style = "font-size: 11.5px; color: #94a3b8;"),
              numericInput("norm_mu", "Mean (μ):", value = 160, step = 5),
              numericInput("norm_sigma", "Standard Deviation (σ):", value = 25, min = 1, step = 2),
              radioButtons("norm_region_type", "Interval Type:",
                           choices = c("Between [a, b]" = "between", "Below b (X ≤ b)" = "below", "Above a (X ≥ a)" = "above"),
                           selected = "between"),
              fluidRow(
                column(6, numericInput("norm_a", "Bound a:", value = 140, step = 5)),
                column(6, numericInput("norm_b", "Bound b:", value = 180, step = 5))
              ),
              div(
                class = "math-formula",
                "Calculated theoretically via pnorm()"
              ),
              uiOutput("norm_metrics_ui")
            )
          ),
          column(
            8,
            div(
              class = "card-box",
              plotOutput("plot_norm", height = "400px")
            )
          )
        )
      ),
      # Cricket Simulator
      tabPanel(
        "Over Simulator",
        br(),
        fluidRow(
          column(
            4,
            div(
              class = "card-box",
              div(class = "card-header-title", "Simulation Engine"),
              p("Simulates 6-ball overs from discrete outcome probabilities.", style = "font-size: 11.5px; color: #94a3b8;"),
              sliderInput("sim_n_overs", "Simulated Overs:", min = 100, max = 5000, value = 1000, step = 100),
              numericInput("sim_target", "Target Over Runs:", value = 10, min = 0, max = 36, step = 1),
              h6("Ball Outcome Probabilities (Sum = 1.0):", style = "color: #f59e0b; margin-top: 12px; font-size: 11px; text-transform: uppercase; font-weight: 700;"),
              fluidRow(
                column(4, numericInput("p_dot", "0 runs:", value = 0.35, min = 0, max = 1, step = 0.05)),
                column(4, numericInput("p_one", "1 run:", value = 0.35, min = 0, max = 1, step = 0.05)),
                column(4, numericInput("p_two", "2 runs:", value = 0.10, min = 0, max = 1, step = 0.02))
              ),
              fluidRow(
                column(4, numericInput("p_three", "3 runs:", value = 0.02, min = 0, max = 1, step = 0.01)),
                column(4, numericInput("p_four", "4 runs:", value = 0.12, min = 0, max = 1, step = 0.02)),
                column(4, numericInput("p_six", "6 runs:", value = 0.06, min = 0, max = 1, step = 0.01))
              ),
              actionButton("run_sim_btn", "⚡ Rerun Simulation", class = "btn-primary btn-sm w-100", style = "margin-top: 10px;"),
              hr(style = "border-color: rgba(255,255,255,0.08);"),
              uiOutput("sim_metrics_ui")
            )
          ),
          column(
            8,
            div(
              class = "card-box",
              plotOutput("plot_sim_totals", height = "360px"),
              div(
                class = "math-formula",
                style = "margin-top: 12px; font-size: 11px;",
                uiOutput("sim_assumptions_ui")
              )
            )
          )
        )
      )
    )
  ),
  
  # ----------------------------------------------------------------------------
  # TAB 6: HYPOTHESIS TESTING
  # ----------------------------------------------------------------------------
  tabPanel(
    "🔬 Testing",
    fluidRow(
      column(
        4,
        div(
          class = "card-box",
          div(class = "card-header-title", "⚙️ Test Configuration"),
          selectInput(
            "hyp_test_type",
            "Statistical Test:",
            choices = c(
              "One-Sample t-Test for Mean (Runs vs Benchmark)" = "one_sample_t",
              "One-Sample Proportion Test (Boundary Rate vs Benchmark)" = "one_sample_prop",
              "Two-Sample Independent t-Test (Comparing 2 Batsmen)" = "two_sample_t",
              "Two-Sample Proportion Test (Comparing 2 Batsmen Boundaries)" = "two_sample_prop",
              "Paired-Sample t-Test (1st Innings vs 2nd Innings Totals)" = "paired_t"
            )
          ),
          conditionalPanel(
            condition = "input.hyp_test_type == 'one_sample_t'",
            uiOutput("hyp_one_sample_player_ui"),
            numericInput("hyp_mu0", "Hypothesized Mean (μ₀):", value = 35, step = 1)
          ),
          conditionalPanel(
            condition = "input.hyp_test_type == 'one_sample_prop'",
            uiOutput("hyp_one_prop_player_ui"),
            numericInput("hyp_p0", "Hypothesized Proportion (p₀):", value = 0.20, min = 0.01, max = 0.99, step = 0.05)
          ),
          conditionalPanel(
            condition = "input.hyp_test_type == 'two_sample_t'",
            uiOutput("hyp_two_sample_p1_ui"),
            uiOutput("hyp_two_sample_p2_ui"),
            checkboxInput("hyp_var_equal", "Assume Equal Variance (Student's vs Welch's)", value = FALSE)
          ),
          conditionalPanel(
            condition = "input.hyp_test_type == 'two_sample_prop'",
            uiOutput("hyp_two_prop_p1_ui"),
            uiOutput("hyp_two_prop_p2_ui")
          ),
          selectInput("hyp_alpha", "Significance Level (α):", choices = c("0.01" = 0.01, "0.05" = 0.05, "0.10" = 0.10), selected = "0.05"),
          radioButtons("hyp_alternative", "Alternative Hypothesis (H₁):",
                       choices = c("Two-Sided (≠)" = "two.sided", "Greater (>)" = "greater", "Less (<)" = "less"),
                       selected = "two.sided")
        )
      ),
      column(
        8,
        div(
          class = "card-box",
          div(class = "card-header-title", "📋 Inferential Decision & Test Output"),
          uiOutput("hyp_results_card_ui"),
          hr(style = "border-color: rgba(255,255,255,0.08);"),
          h6("Statistical Interpretation", style = "color: #f59e0b; font-size: 11px; text-transform: uppercase; font-weight: 700;"),
          uiOutput("hyp_interpretation_ui")
        )
      )
    )
  ),
  
  # ----------------------------------------------------------------------------
  # TAB 7: CHI-SQUARE ANALYSIS
  # ----------------------------------------------------------------------------
  tabPanel(
    "📐 Chi-Square",
    fluidRow(
      column(
        4,
        div(
          class = "card-box",
          div(class = "card-header-title", "⚙️ Chi-Square Mode"),
          radioButtons(
            "cs_mode",
            label = NULL,
            choices = c("Goodness-of-Fit Test" = "gof", "Test of Independence (Contingency)" = "independence"),
            selected = "gof"
          ),
          conditionalPanel(
            condition = "input.cs_mode == 'gof'",
            selectInput("cs_gof_variable", "Categorical Factor:",
                        choices = c("Match Condition" = "match_condition", "Score Category" = "score_category", "Venue" = "venue"),
                        selected = "match_condition")
          ),
          conditionalPanel(
            condition = "input.cs_mode == 'independence'",
            selectInput("cs_ind_var1", "Factor 1:",
                        choices = c("Player" = "player", "Team" = "team", "Match Condition" = "match_condition"),
                        selected = "player"),
            selectInput("cs_ind_var2", "Factor 2:",
                        choices = c("Score Category" = "score_category", "Dismissal Status" = "dismissals", "Innings" = "innings"),
                        selected = "score_category")
          ),
          selectInput("cs_alpha", "Significance Level (α):", choices = c("0.01" = 0.01, "0.05" = 0.05, "0.10" = 0.10), selected = "0.05"),
          div(
            class = "math-formula",
            "χ² = Σ [ (O_i - E_i)² / E_i ]\ndf = (r - 1) * (c - 1)"
          )
        )
      ),
      column(
        8,
        div(
          class = "card-box",
          plotOutput("plot_chisq", height = "340px")
        ),
        div(
          class = "card-box",
          div(class = "card-header-title", "📋 Contingency Results & Cochran Audit"),
          uiOutput("chisq_decision_ui"),
          hr(style = "border-color: rgba(255,255,255,0.08);"),
          div(class = "table-responsive-custom", tableOutput("table_chisq_details"))
        )
      )
    )
  ),
  
  # ----------------------------------------------------------------------------
  # TAB 8: ANOVA & CONSISTENCY
  # ----------------------------------------------------------------------------
  tabPanel(
    "⚖️ ANOVA",
    fluidRow(
      column(
        4,
        div(
          class = "card-box",
          div(class = "card-header-title", "⚙️ One-Way ANOVA Setup"),
          selectInput(
            "anova_group_var",
            "Grouping Factor (X):",
            choices = c("Player" = "player", "Match Condition" = "match_condition", "Batting Position" = "batting_position"),
            selected = "player"
          ),
          selectInput(
            "anova_val_var",
            "Continuous Response (Y):",
            choices = c("Runs Scored" = "runs", "Strike Rate" = "strike_rate", "Balls Faced" = "balls_faced"),
            selected = "runs"
          ),
          selectInput("anova_alpha", "Significance Level (α):", choices = c("0.01" = 0.01, "0.05" = 0.05, "0.10" = 0.10), selected = "0.05"),
          div(
            class = "math-formula",
            "F = MS_between / MS_within\nMS = SS / df"
          ),
          hr(style = "border-color: rgba(255,255,255,0.08);"),
          uiOutput("anova_decision_badge_ui")
        )
      ),
      column(
        8,
        div(
          class = "card-box",
          plotOutput("plot_anova", height = "360px")
        )
      )
    ),
    fluidRow(
      column(
        6,
        div(
          class = "card-box",
          div(class = "card-header-title", "📊 ANOVA Source Table"),
          div(class = "table-responsive-custom", tableOutput("table_anova_table"))
        )
      ),
      column(
        6,
        div(
          class = "card-box",
          div(class = "card-header-title", "📈 Group Moments (Mean, SE, 95% CI)"),
          div(class = "table-responsive-custom", tableOutput("table_anova_group_stats"))
        )
      )
    ),
    fluidRow(
      column(
        12,
        div(
          class = "card-box",
          div(class = "card-header-title", "🔬 Tukey HSD Post-Hoc Comparisons"),
          div(class = "table-responsive-custom", tableOutput("table_anova_tukey")),
          hr(style = "border-color: rgba(255,255,255,0.08);"),
          uiOutput("anova_diagnostics_ui")
        )
      )
    )
  ),
  
  # ----------------------------------------------------------------------------
  # TAB 9: REPORT
  # ----------------------------------------------------------------------------
  tabPanel(
    "📄 Report",
    fluidRow(
      column(
        3,
        div(
          class = "card-box",
          div(class = "card-header-title", "📥 Export Report"),
          p("Generates an exhaustive academic report capturing all active filters and fitted statistical models.", style = "font-size: 11.5px; color: #94a3b8;"),
          downloadButton("download_html_report", "Download HTML Report", class = "btn-primary w-100 mb-2"),
          downloadButton("download_txt_report", "Download Text Summary", class = "btn-outline-secondary w-100")
        )
      ),
      column(
        9,
        div(
          class = "card-box",
          div(class = "card-header-title", "📑 Live Report Preview"),
          uiOutput("report_preview_ui")
        )
      )
    )
  )
)

# ------------------------------------------------------------------------------
# SERVER LOGIC
# ------------------------------------------------------------------------------
server <- function(input, output, session) {
  
  # Initialize reactive data store directly with sample dataset
  initial_sample <- load_sample_data("data/sample_cricket_data.csv")
  data_store <- reactiveValues(
    mode = "sample",
    raw_df = initial_sample$cleaned_data,
    clean_df = initial_sample$cleaned_data,
    validation = initial_sample
  )
  
  # Handle Mode Switch and File Upload
  observeEvent(input$data_source_mode, {
    if (input$data_source_mode == "sample") {
      data_store$mode <- "sample"
      sample_res <- load_sample_data("data/sample_cricket_data.csv")
      data_store$raw_df <- sample_res$cleaned_data
      data_store$clean_df <- sample_res$cleaned_data
      data_store$validation <- sample_res
    } else {
      data_store$mode <- "upload"
    }
  })
  
  observeEvent(input$user_csv_file, {
    req(input$user_csv_file)
    res <- load_user_csv(input$user_csv_file$datapath)
    data_store$validation <- res
    if (res$valid) {
      data_store$raw_df <- res$cleaned_data
      data_store$clean_df <- res$cleaned_data
    }
  })
  
  # Active Mode Banner
  output$active_mode_banner <- renderUI({
    if (data_store$mode == "sample") {
      div(
        class = "mode-indicator mode-sample",
        "📊 ACTIVE DATA MODE: Reproducible Demonstration Dataset (Synthetic Cricket Batting Records)"
      )
    } else {
      div(
        class = "mode-indicator mode-real",
        "📂 ACTIVE DATA MODE: Real Data Mode (User Uploaded CSV Dataset)"
      )
    }
  })
  
  # Global Dynamic Filter Inputs
  output$filter_player_ui <- renderUI({
    req(data_store$clean_df)
    players <- sort(unique(data_store$clean_df$player))
    selectizeInput("filter_players", "Batsmen:", choices = players, selected = NULL, multiple = TRUE,
                   options = list(placeholder = "All Batsmen"))
  })
  
  output$filter_condition_ui <- renderUI({
    req(data_store$clean_df)
    conds <- sort(unique(data_store$clean_df$match_condition))
    selectizeInput("filter_conditions", "Condition:", choices = conds, selected = NULL, multiple = TRUE,
                   options = list(placeholder = "All Conditions"))
  })
  
  output$filter_innings_ui <- renderUI({
    req(data_store$clean_df)
    checkboxGroupInput("filter_innings", "Innings:", choices = c("1st Innings" = 1, "2nd Innings" = 2),
                       selected = c(1, 2))
  })
  
  observeEvent(input$reset_filters, {
    req(data_store$clean_df)
    updateSelectizeInput(session, "filter_players", selected = character(0))
    updateSelectizeInput(session, "filter_conditions", selected = character(0))
    updateCheckboxGroupInput(session, "filter_innings", selected = c(1, 2))
  })
  
  # Filtered Data Reactive
  filtered_data <- reactive({
    req(data_store$clean_df)
    df <- data_store$clean_df
    
    if (!is.null(input$filter_players) && length(input$filter_players) > 0) {
      df <- df[df$player %in% input$filter_players, , drop = FALSE]
    }
    if (!is.null(input$filter_conditions) && length(input$filter_conditions) > 0) {
      df <- df[df$match_condition %in% input$filter_conditions, , drop = FALSE]
    }
    if (!is.null(input$filter_innings) && length(input$filter_innings) > 0) {
      df <- df[df$innings %in% as.numeric(input$filter_innings), , drop = FALSE]
    }
    df
  })
  
  # OVERVIEW TAB OUTPUTS
  overview_metrics <- reactive({
    compute_overall_metrics(filtered_data())
  })
  
  output$kpi_innings <- renderText({
    format(overview_metrics()$total_innings, big.mark = ",")
  })
  
  output$kpi_runs <- renderText({
    format(overview_metrics()$total_runs, big.mark = ",")
  })
  
  output$kpi_mean_runs <- renderText({
    sprintf("%.1f", overview_metrics()$mean_runs)
  })
  
  output$kpi_strike_rate <- renderText({
    sprintf("%.1f", overview_metrics()$overall_strike_rate)
  })
  
  output$plot_overview_players <- renderPlot({
    req(filtered_data())
    plot_runs_by_player(filtered_data())
  }, bg = "transparent")
  
  output$plot_overview_dist <- renderPlot({
    req(filtered_data())
    plot_runs_distribution(filtered_data())
  }, bg = "transparent")
  
  output$table_overview_players <- renderTable({
    req(filtered_data())
    p_df <- compute_player_metrics(filtered_data())
    if (nrow(p_df) == 0) return(NULL)
    p_df[, c("Player", "Team", "Innings", "TotalRuns", "MeanRuns", "MedianRuns", "SD", "BattingAverage", "StrikeRate", "BoundaryPct", "CV_Pct")]
  }, digits = 1, striped = TRUE, hover = TRUE, bordered = TRUE)
  
  # DATA EXPLORER TAB OUTPUTS
  output$validation_status_ui <- renderUI({
    v <- data_store$validation
    if (is.null(v)) return(NULL)
    if (v$valid) {
      tagList(
        div(class = "stat-badge", "✓ Schema & Constraints Validated"),
        if (length(v$warnings) > 0) {
          tagList(
            br(), br(),
            p("Data Adjustments & Audits:", style = "color: #f59e0b; font-size: 11px; font-weight: bold;"),
            tags$ul(lapply(v$warnings, function(w) tags$li(style = "color: #fbbf24; font-size: 11px;", w)))
          )
        }
      )
    } else {
      tagList(
        div(class = "stat-badge-danger", "✗ Validation Failed"),
        tags$ul(lapply(v$errors, function(e) tags$li(style = "color: #f43f5e; font-size: 11px;", e)))
      )
    }
  })
  
  output$missing_values_table <- renderTable({
    req(data_store$validation)
    data_store$validation$missing_report
  }, striped = TRUE, hover = TRUE)
  
  output$dataset_dimensions_ui <- renderUI({
    req(filtered_data())
    span(
      sprintf("%d Rows × %d Columns", nrow(filtered_data()), ncol(filtered_data())),
      style = "font-weight: 700; color: #38bdf8; font-size: 0.85rem; background: rgba(56,189,248,0.1); padding: 4px 10px; border-radius: 6px;"
    )
  })
  
  output$data_preview_table <- renderTable({
    req(filtered_data())
    head(filtered_data(), 10)
  }, striped = TRUE, hover = TRUE, bordered = TRUE)
  
  output$schema_table <- renderTable({
    data.frame(
      Column = REQUIRED_COLUMNS,
      Description = COLUMN_DESCRIPTIONS[REQUIRED_COLUMNS],
      stringsAsFactors = FALSE
    )
  }, striped = TRUE, hover = TRUE)
  
  # Download Handlers
  output$download_cleaned_data <- downloadHandler(
    filename = function() { paste0("CricketEdge_Cleaned_Data_", Sys.Date(), ".csv") },
    content = function(file) {
      write.csv(filtered_data(), file, row.names = FALSE)
    }
  )
  
  output$download_csv_template <- downloadHandler(
    filename = function() { "cricket_data_template.csv" },
    content = function(file) {
      file.copy("data/cricket_data_template.csv", file)
    }
  )
  
  # PLAYER COMPARISON TAB OUTPUTS
  output$compare_players_picker_ui <- renderUI({
    req(data_store$clean_df)
    players <- sort(unique(data_store$clean_df$player))
    default_selected <- head(players, min(4, length(players)))
    selectizeInput("compare_selected_players", "Select Batsmen:",
                   choices = players, selected = default_selected, multiple = TRUE)
  })
  
  compared_player_stats <- reactive({
    req(filtered_data(), input$compare_selected_players)
    compute_player_metrics(filtered_data(), input$compare_selected_players)
  })
  
  output$plot_player_boxplots <- renderPlot({
    req(filtered_data(), input$compare_selected_players)
    plot_player_comparison_boxplots(filtered_data(), input$compare_selected_players)
  }, bg = "transparent")
  
  output$plot_player_bars <- renderPlot({
    p_df <- compared_player_stats()
    req(nrow(p_df) > 0, input$compare_metric_choice)
    
    metric <- input$compare_metric_choice
    metric_label <- names(which(c(
      "BattingAverageNum" = "Batting Average",
      "StrikeRate" = "Strike Rate",
      "TotalRuns" = "Total Runs",
      "MeanRuns" = "Mean Runs",
      "BoundaryPct" = "Boundary Percentage (%)",
      "CV_Pct" = "Consistency Metric (CV %)"
    ) == metric))
    
    p_df$PlotVal <- p_df[[metric]]
    
    ggplot(p_df, aes(x = reorder(Player, -PlotVal), y = PlotVal, fill = Player)) +
      geom_col(width = 0.62, alpha = 0.92) +
      geom_text(aes(label = round(PlotVal, 1)), vjust = -0.4, color = "#f8fafc", fontface = "bold", size = 3.8) +
      scale_fill_brewer(palette = "Set2") +
      scale_y_continuous(expand = expansion(mult = c(0, 0.16))) +
      labs(
        title = sprintf("Batsman Comparison by %s", metric_label),
        x = NULL,
        y = metric_label
      ) +
      theme_cricketedge() +
      theme(legend.position = "none")
  }, bg = "transparent")
  
  output$plot_player_scatter <- renderPlot({
    req(filtered_data(), input$compare_selected_players)
    plot_runs_vs_balls_scatter(filtered_data(), input$compare_selected_players)
  }, bg = "transparent")
  
  output$table_player_comparison <- renderTable({
    p_df <- compared_player_stats()
    req(nrow(p_df) > 0)
    p_df[, c("Player", "Team", "Innings", "TotalRuns", "MeanRuns", "MedianRuns", "SD", "BattingAverage", "StrikeRate", "Fours", "Sixes", "BoundaryPct", "CV_Pct")]
  }, digits = 1, striped = TRUE, hover = TRUE, bordered = TRUE)
  
  # CORRELATION & REGRESSION TAB OUTPUTS
  reg_result <- reactive({
    req(filtered_data())
    df <- filtered_data()
    if (input$reg_model_type == "simple") {
      fit_simple_regression(df, response = "runs", predictor = input$simple_reg_predictor)
    } else {
      fit_multiple_regression(df, response = "runs", predictors = c("balls_faced", "fours", "sixes"))
    }
  })
  
  output$reg_equation_ui <- renderUI({
    res <- reg_result()
    if (!res$valid) {
      p(res$message, style = "color: #f43f5e;")
    } else {
      div(class = "math-formula", res$equation)
    }
  })
  
  output$reg_metrics_ui <- renderUI({
    res <- reg_result()
    if (!res$valid) return(NULL)
    tagList(
      p(HTML(sprintf("<strong>R² (Coeff of Determination):</strong> <span style='color: #f59e0b;'>%.4f</span>", res$r_squared))),
      p(HTML(sprintf("<strong>Adjusted R²:</strong> %.4f", res$adj_r_squared))),
      p(HTML(sprintf("<strong>Residual Std Error:</strong> %.2f on %d DF", res$residual_se, res$df[2]))),
      p(HTML(sprintf("<strong>Overall F-Statistic:</strong> %.2f (p = %.4g)", res$f_statistic, res$f_p_value)))
    )
  })
  
  output$plot_regression_fit <- renderPlot({
    res <- reg_result()
    req(res$valid)
    if (input$reg_model_type == "simple") {
      plot_simple_regression(res)
    } else {
      diag <- res$diagnostics
      ggplot(diag, aes(x = fitted, y = observed_y)) +
        geom_point(color = "#38bdf8", alpha = 0.65, size = 2.4) +
        geom_abline(intercept = 0, slope = 1, color = "#f59e0b", linewidth = 1.2, linetype = "dashed") +
        labs(
          title = "Multiple Regression: Observed vs Fitted Model Values",
          subtitle = sprintf("R² = %.4f | Formula: %s", res$r_squared, res$equation),
          x = "Fitted (Predicted) Runs",
          y = "Observed Runs",
          caption = "Dashed Gold Line: Perfect agreement (y = y_hat)"
        ) +
        theme_cricketedge()
    }
  }, bg = "transparent")
  
  output$plot_regression_resids <- renderPlot({
    res <- reg_result()
    req(res$valid)
    plot_regression_residuals(res)
  }, bg = "transparent")
  
  output$table_regression_coefs <- renderTable({
    res <- reg_result()
    req(res$valid)
    df <- res$coefficients
    df$Variable <- rownames(df)
    df[, c("Variable", "Estimate", "StdError", "tValue", "pValue", "Significance")]
  }, digits = 4, striped = TRUE, hover = TRUE)
  
  output$reg_interpretation_ui <- renderUI({
    res <- reg_result()
    req(res$valid)
    note <- if (!is.null(res$notes)) res$notes else res$interpretation
    p(note, style = "color: #94a3b8; font-size: 12.5px; margin-top: 10px; line-height: 1.6;")
  })
  
  # PROBABILITY LAB TAB OUTPUTS
  binom_res <- reactive({
    compute_binomial_model(n = input$binom_n, p = input$binom_p, k = input$binom_k)
  })
  
  output$binom_metrics_ui <- renderUI({
    b <- binom_res()
    tagList(
      p(HTML(sprintf("<strong>Exact P(X = %d):</strong> <span style='color: #f59e0b;'>%.4f</span>", b$k, b$prob_exact))),
      p(HTML(sprintf("<strong>Cumulative P(X ≤ %d):</strong> %.4f", b$k, b$prob_at_most))),
      p(HTML(sprintf("<strong>Exceedance P(X ≥ %d):</strong> %.4f", b$k, b$prob_at_least))),
      p(HTML(sprintf("<strong>Expected Value E[X]:</strong> %.2f", b$expected_value))),
      p(HTML(sprintf("<strong>Variance Var(X):</strong> %.2f (SD = %.2f)", b$variance, b$sd)))
    )
  })
  
  output$plot_binom <- renderPlot({
    plot_binomial_distribution(binom_res())
  }, bg = "transparent")
  
  pois_res <- reactive({
    compute_poisson_model(lambda = input$pois_lambda, k = input$pois_k)
  })
  
  output$pois_metrics_ui <- renderUI({
    p_res <- pois_res()
    tagList(
      p(HTML(sprintf("<strong>Exact P(X = %d):</strong> <span style='color: #f59e0b;'>%.4f</span>", p_res$k, p_res$prob_exact))),
      p(HTML(sprintf("<strong>Cumulative P(X ≤ %d):</strong> %.4f", p_res$k, p_res$prob_at_most))),
      p(HTML(sprintf("<strong>Exceedance P(X > %d):</strong> %.4f", p_res$k, p_res$prob_exceeds))),
      p(HTML(sprintf("<strong>Expected Value E[X]:</strong> %.2f", p_res$expected_value))),
      p(HTML(sprintf("<strong>Variance Var(X):</strong> %.2f", p_res$variance)))
    )
  })
  
  output$plot_pois <- renderPlot({
    plot_poisson_distribution(pois_res())
  }, bg = "transparent")
  
  norm_res <- reactive({
    compute_normal_model(
      mu = input$norm_mu,
      sigma = input$norm_sigma,
      lower_val = input$norm_a,
      upper_val = input$norm_b,
      region_type = input$norm_region_type
    )
  })
  
  output$norm_metrics_ui <- renderUI({
    nr <- norm_res()
    lbl <- switch(
      nr$region_type,
      "between" = sprintf("P(%.1f ≤ X ≤ %.1f)", nr$lower_val, nr$upper_val),
      "below" = sprintf("P(X ≤ %.1f)", nr$upper_val),
      "above" = sprintf("P(X ≥ %.1f)", nr$lower_val)
    )
    tagList(
      p(HTML(sprintf("<strong>Calculated Probability %s:</strong> <span style='color: #f59e0b; font-size: 16px;'>%.4f</span>", lbl, nr$probability))),
      p(HTML(sprintf("<strong>Expected Value μ:</strong> %.2f", nr$expected_value))),
      p(HTML(sprintf("<strong>Standard Deviation σ:</strong> %.2f", nr$sd)))
    )
  })
  
  output$plot_norm <- renderPlot({
    plot_normal_distribution(norm_res())
  }, bg = "transparent")
  
  sim_res <- reactiveVal(simulate_cricket_overs(n_overs = 1000, seed = 42))
  
  observeEvent(input$run_sim_btn, {
    probs_vec <- c(input$p_dot, input$p_one, input$p_two, input$p_three, input$p_four, input$p_six)
    sim_res(simulate_cricket_overs(
      n_overs = input$sim_n_overs,
      probs = probs_vec,
      target_over_runs = input$sim_target,
      seed = sample(1:100000, 1)
    ))
  })
  
  output$sim_metrics_ui <- renderUI({
    s <- sim_res()
    tagList(
      p(HTML(sprintf("<strong>Simulated Mean Over:</strong> <span style='color: #f59e0b;'>%.2f runs</span> (Theor: %.2f)", s$empirical_mean, s$theor_over_mean))),
      p(HTML(sprintf("<strong>Median:</strong> %.1f | <strong>SD:</strong> %.2f (Theor: %.2f)", s$empirical_median, s$empirical_sd, s$theor_over_sd))),
      p(HTML(sprintf("<strong>P(Score ≥ %d runs):</strong> <span style='color: #10b981; font-weight: bold;'>%.3f (%.1f%%)</span>",
                     s$target_over_runs, s$prob_reach_target, s$prob_reach_target * 100)))
    )
  })
  
  output$plot_sim_totals <- renderPlot({
    plot_cricket_simulation_totals(sim_res())
  }, bg = "transparent")
  
  output$sim_assumptions_ui <- renderUI({
    pre(sim_res()$assumptions, style = "color: #94a3b8; font-size: 10.5px; margin: 0; background: transparent; border: none;")
  })
  
  # HYPOTHESIS TESTING TAB OUTPUTS
  output$hyp_one_sample_player_ui <- renderUI({
    req(data_store$clean_df)
    selectInput("hyp_one_player", "Batsman:", choices = sort(unique(data_store$clean_df$player)))
  })
  
  output$hyp_one_prop_player_ui <- renderUI({
    req(data_store$clean_df)
    selectInput("hyp_one_prop_player", "Batsman:", choices = sort(unique(data_store$clean_df$player)))
  })
  
  output$hyp_two_sample_p1_ui <- renderUI({
    req(data_store$clean_df)
    players <- sort(unique(data_store$clean_df$player))
    selectInput("hyp_two_p1", "Batsman 1:", choices = players, selected = players[1])
  })
  
  output$hyp_two_sample_p2_ui <- renderUI({
    req(data_store$clean_df)
    players <- sort(unique(data_store$clean_df$player))
    default_p2 <- if (length(players) >= 2) players[2] else players[1]
    selectInput("hyp_two_p2", "Batsman 2:", choices = players, selected = default_p2)
  })
  
  output$hyp_two_prop_p1_ui <- renderUI({
    req(data_store$clean_df)
    players <- sort(unique(data_store$clean_df$player))
    selectInput("hyp_two_prop_p1", "Batsman 1:", choices = players, selected = players[1])
  })
  
  output$hyp_two_prop_p2_ui <- renderUI({
    req(data_store$clean_df)
    players <- sort(unique(data_store$clean_df$player))
    default_p2 <- if (length(players) >= 2) players[2] else players[1]
    selectInput("hyp_two_prop_p2", "Batsman 2:", choices = players, selected = default_p2)
  })
  
  hyp_test_result <- reactive({
    req(filtered_data())
    df <- filtered_data()
    alpha_val <- as.numeric(input$hyp_alpha)
    alt <- input$hyp_alternative
    ttype <- input$hyp_test_type
    
    if (ttype == "one_sample_t") {
      req(input$hyp_one_player)
      x <- df$runs[df$player == input$hyp_one_player]
      run_one_sample_t_test(x, mu0 = input$hyp_mu0, alternative = alt, conf_level = 1 - alpha_val, label = input$hyp_one_player)
    } else if (ttype == "one_sample_prop") {
      req(input$hyp_one_prop_player)
      sub_p <- df[df$player == input$hyp_one_prop_player, ]
      tot_balls <- sum(sub_p$balls_faced, na.rm = TRUE)
      boundaries <- sum(sub_p$fours + sub_p$sixes, na.rm = TRUE)
      run_one_sample_prop_test(boundaries, tot_balls, p0 = input$hyp_p0, alternative = alt, conf_level = 1 - alpha_val, label = paste(input$hyp_one_prop_player, "Boundary Rate"))
    } else if (ttype == "two_sample_t") {
      req(input$hyp_two_p1, input$hyp_two_p2)
      x <- df$runs[df$player == input$hyp_two_p1]
      y <- df$runs[df$player == input$hyp_two_p2]
      run_two_sample_t_test(x, y, label1 = input$hyp_two_p1, label2 = input$hyp_two_p2, var_equal = input$hyp_var_equal, alternative = alt, conf_level = 1 - alpha_val)
    } else if (ttype == "two_sample_prop") {
      req(input$hyp_two_prop_p1, input$hyp_two_prop_p2)
      sub1 <- df[df$player == input$hyp_two_prop_p1, ]
      sub2 <- df[df$player == input$hyp_two_prop_p2, ]
      s1 <- sum(sub1$fours + sub1$sixes, na.rm = TRUE)
      n1 <- sum(sub1$balls_faced, na.rm = TRUE)
      s2 <- sum(sub2$fours + sub2$sixes, na.rm = TRUE)
      n2 <- sum(sub2$balls_faced, na.rm = TRUE)
      run_two_sample_prop_test(s1, n1, s2, n2, label1 = input$hyp_two_prop_p1, label2 = input$hyp_two_prop_p2, alternative = alt, conf_level = 1 - alpha_val)
    } else if (ttype == "paired_t") {
      run_paired_t_test(df, match_col = "match_id", innings_col = "innings", val_col = "innings_total", alternative = alt, conf_level = 1 - alpha_val)
    }
  })
  
  output$hyp_results_card_ui <- renderUI({
    res <- hyp_test_result()
    if (!res$valid) {
      return(p(res$message, style = "color: #f43f5e;"))
    }
    
    badge_class <- if (grepl("Reject H₀", res$decision)) "stat-badge" else "stat-badge-danger"
    tagList(
      div(class = badge_class, res$decision),
      br(), br(),
      p(HTML(sprintf("<strong>Test:</strong> %s", res$test_name))),
      p(HTML(sprintf("<strong>Null Hypothesis:</strong> <code>%s</code>", res$h0))),
      p(HTML(sprintf("<strong>Alternative Hypothesis:</strong> <code>%s</code>", res$h1))),
      fluidRow(
        column(4, p(HTML(sprintf("<strong>Test Statistic:</strong> %.4f", res$statistic)))),
        column(4, p(HTML(sprintf("<strong>Degrees of Freedom:</strong> %s", ifelse(!is.null(res$df), as.character(res$df), "N/A"))))),
        column(4, p(HTML(sprintf("<strong>Calculated p-value:</strong> <span style='color: #f59e0b; font-weight: bold;'>%.4g</span>", res$p_value))))
      ),
      if (!is.null(res$conf_int)) {
        p(HTML(sprintf("<strong>%.0f%% Confidence Interval:</strong> [%.2f, %.2f]", res$conf_level * 100, res$conf_int[1], res$conf_int[2])))
      }
    )
  })
  
  output$hyp_interpretation_ui <- renderUI({
    res <- hyp_test_result()
    req(res$valid)
    p(res$explanation, style = "color: #94a3b8; font-size: 12.5px; line-height: 1.6;")
  })
  
  # CHI-SQUARE TAB OUTPUTS
  cs_result <- reactive({
    req(filtered_data())
    df <- filtered_data()
    alpha_val <- as.numeric(input$cs_alpha)
    
    if (input$cs_mode == "gof") {
      counts <- table(df[[input$cs_gof_variable]])
      run_chi_square_gof(counts, alpha = alpha_val)
    } else {
      run_chi_square_independence(df, var1 = input$cs_ind_var1, var2 = input$cs_ind_var2, alpha = alpha_val)
    }
  })
  
  output$plot_chisq <- renderPlot({
    res <- cs_result()
    req(res$valid)
    if (input$cs_mode == "gof") {
      plot_chi_square_gof(res)
    } else {
      plot_chi_square_contingency(res)
    }
  }, bg = "transparent")
  
  output$chisq_decision_ui <- renderUI({
    res <- cs_result()
    if (!res$valid) return(p(res$message, style = "color: #f43f5e;"))
    
    badge_class <- if (grepl("Reject H₀", res$decision)) "stat-badge" else "stat-badge-danger"
    tagList(
      div(class = badge_class, res$decision),
      p(HTML(sprintf("<strong>Statistic χ²:</strong> %.4f | <strong>df:</strong> %d | <strong>p-value:</strong> %.4g",
                     res$statistic, res$df, res$p_value)), style = "margin-top: 10px;"),
      p(res$explanation, style = "font-size: 12.5px; color: #94a3b8;"),
      if (length(res$assumption_warning) > 0) {
        p(res$assumption_warning, style = "color: #f43f5e; font-size: 11.5px; font-weight: bold;")
      }
    )
  })
  
  output$table_chisq_details <- renderTable({
    res <- cs_result()
    req(res$valid)
    if (input$cs_mode == "gof") {
      res$table
    } else {
      res$observed_table
    }
  }, striped = TRUE, hover = TRUE, bordered = TRUE)
  
  # ANOVA TAB OUTPUTS
  anova_result <- reactive({
    req(filtered_data())
    df <- filtered_data()
    alpha_val <- as.numeric(input$anova_alpha)
    run_cricket_anova(df, group_col = input$anova_group_var, val_col = input$anova_val_var, alpha = alpha_val)
  })
  
  output$anova_decision_badge_ui <- renderUI({
    res <- anova_result()
    if (!res$valid) return(p(res$message, style = "color: #f43f5e;"))
    
    badge_class <- if (grepl("Reject H₀", res$decision)) "stat-badge" else "stat-badge-danger"
    tagList(
      div(class = badge_class, res$decision),
      br(), br(),
      p(HTML(sprintf("<strong>F-Statistic:</strong> F(%d, %d) = %.4f",
                     res$anova_table$Df[1], res$anova_table$Df[2], res$f_stat))),
      p(HTML(sprintf("<strong>Pr(>F):</strong> <span style='color: #f59e0b; font-weight: bold;'>%.4g</span>", res$p_val))),
      p(res$explanation, style = "font-size: 12px; color: #94a3b8;")
    )
  })
  
  output$plot_anova <- renderPlot({
    res <- anova_result()
    req(res$valid, filtered_data())
    plot_anova_groups(res, filtered_data())
  }, bg = "transparent")
  
  output$table_anova_table <- renderTable({
    res <- anova_result()
    req(res$valid)
    res$anova_table
  }, striped = TRUE, hover = TRUE)
  
  output$table_anova_group_stats <- renderTable({
    res <- anova_result()
    req(res$valid)
    res$group_stats
  }, striped = TRUE, hover = TRUE)
  
  output$table_anova_tukey <- renderTable({
    res <- anova_result()
    req(res$valid)
    if (is.null(res$tukey)) return(data.frame(Message = "Tukey HSD not applicable."))
    head(res$tukey, 10)
  }, striped = TRUE, hover = TRUE)
  
  output$anova_diagnostics_ui <- renderUI({
    res <- anova_result()
    req(res$valid)
    pre(res$diagnostics_text, style = "color: #94a3b8; font-size: 11px; background: #090e17; padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);")
  })
  
  # REPORT TAB OUTPUTS
  report_html_content <- reactive({
    generate_statistical_report_html(
      active_mode = ifelse(data_store$mode == "sample", "Sample Synthetic Data Mode", "Uploaded Real Data Mode"),
      df = filtered_data(),
      overall_metrics = overview_metrics(),
      player_metrics = compute_player_metrics(filtered_data()),
      reg_res = reg_result(),
      binom_res = binom_res(),
      pois_res = pois_res(),
      norm_res = norm_res(),
      sim_res = sim_res(),
      hyp_res = hyp_test_result(),
      cs_res = cs_result(),
      anova_res = anova_result()
    )
  })
  
  output$report_preview_ui <- renderUI({
    HTML(report_html_content())
  })
  
  output$download_html_report <- downloadHandler(
    filename = function() { paste0("CricketEdge_Report_", Sys.Date(), ".html") },
    content = function(file) {
      writeLines(report_html_content(), file)
    }
  )
  
  output$download_txt_report <- downloadHandler(
    filename = function() { paste0("CricketEdge_Summary_", Sys.Date(), ".txt") },
    content = function(file) {
      ov <- overview_metrics()
      lines <- c(
        "============================================================",
        "CRICKETEDGE — STATISTICAL PERFORMANCE SUMMARY",
        "============================================================",
        sprintf("Generated: %s", Sys.time()),
        sprintf("Data Mode: %s", ifelse(data_store$mode == "sample", "Sample Synthetic", "User Uploaded CSV")),
        sprintf("Total Innings Sampled: %d", ov$total_innings),
        sprintf("Total Aggregate Runs: %d", ov$total_runs),
        sprintf("Mean Runs per Innings: %.2f", ov$mean_runs),
        sprintf("Overall Strike Rate: %.2f", ov$overall_strike_rate),
        sprintf("Overall Batting Average: %s", as.character(ov$batting_average)),
        "============================================================"
      )
      writeLines(lines, file)
    }
  )
}

# ------------------------------------------------------------------------------
# LAUNCH APPLICATION
# ------------------------------------------------------------------------------
shinyApp(ui = ui, server = server)
