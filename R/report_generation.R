# ==============================================================================
# CricketEdge — Report Generation Module
# Generates comprehensive, downloadable HTML and Markdown statistical reports
# ==============================================================================

#' Generate comprehensive HTML report string summarizing active analyses
#' @param active_mode Data mode ("Sample Synthetic" or "Uploaded Real CSV")
#' @param df Active filtered data frame
#' @param overall_metrics Metrics from compute_overall_metrics()
#' @param player_metrics Metrics from compute_player_metrics()
#' @param reg_res Output from fit_simple_regression() or fit_multiple_regression()
#' @param binom_res Output from compute_binomial_model()
#' @param pois_res Output from compute_poisson_model()
#' @param norm_res Output from compute_normal_model()
#' @param sim_res Output from simulate_cricket_overs()
#' @param hyp_res Output from hypothesis testing
#' @param cs_res Output from chi-square analysis
#' @param anova_res Output from run_cricket_anova()
#' @return A character string of complete HTML report document
generate_statistical_report_html <- function(
    active_mode = "Sample Synthetic",
    df = NULL,
    overall_metrics = NULL,
    player_metrics = NULL,
    reg_res = NULL,
    binom_res = NULL,
    pois_res = NULL,
    norm_res = NULL,
    sim_res = NULL,
    hyp_res = NULL,
    cs_res = NULL,
    anova_res = NULL
) {
  timestamp_str <- format(Sys.time(), "%Y-%m-%d %H:%M:%S %Z")
  n_records <- if (!is.null(df)) nrow(df) else 0
  
  # Format Player table rows
  player_rows_html <- ""
  if (!is.null(player_metrics) && nrow(player_metrics) > 0) {
    p_subset <- head(player_metrics, 10)
    for (i in seq_len(nrow(p_subset))) {
      r <- p_subset[i, ]
      player_rows_html <- paste0(
        player_rows_html,
        sprintf("<tr><td>%s</td><td>%s</td><td>%d</td><td>%d</td><td>%.1f</td><td>%.1f</td><td>%.1f</td><td>%s</td><td>%.1f</td><td>%.1f%%</td><td>%.1f</td></tr>",
                r$Player, r$Team, r$Innings, r$TotalRuns, r$MeanRuns, r$MedianRuns, r$SD, r$BattingAverage, r$StrikeRate, r$BoundaryPct, ifelse(is.na(r$CV_Pct), 0, r$CV_Pct))
      )
    }
  }
  
  # Regression Section
  reg_html <- "<p><em>No regression model evaluated.</em></p>"
  if (!is.null(reg_res) && isTRUE(reg_res$valid)) {
    coef_rows <- ""
    for (nm in rownames(reg_res$coefficients)) {
      cf <- reg_res$coefficients[nm, ]
      coef_rows <- paste0(
        coef_rows,
        sprintf("<tr><td><strong>%s</strong></td><td>%.4f</td><td>%.4f</td><td>%.3f</td><td>%.4g</td><td>%s</td></tr>",
                nm, cf$Estimate, cf$StdError, cf$tValue, cf$pValue, cf$Significance)
      )
    }
    
    reg_html <- sprintf(
      "<div>
        <p><strong>Fitted Equation:</strong> <code>%s</code></p>
        <p><strong>Coefficient of Determination (R²):</strong> %.4f | <strong>Adjusted R²:</strong> %.4f</p>
        <p><strong>Residual Std Error:</strong> %.2f on %d degrees of freedom</p>
        <p><strong>Model F-Statistic:</strong> %.2f (p-value: %.4g)</p>
        <table class='report-table'>
          <thead><tr><th>Term</th><th>Estimate</th><th>Std Error</th><th>t value</th><th>Pr(&gt;|t|)</th><th>Sig</th></tr></thead>
          <tbody>%s</tbody>
        </table>
        <p class='note'>%s</p>
      </div>",
      reg_res$equation, reg_res$r_squared, reg_res$adj_r_squared,
      reg_res$residual_se, reg_res$df[2], reg_res$f_statistic, reg_res$f_p_value,
      coef_rows, ifelse(!is.null(reg_res$notes), reg_res$notes, reg_res$interpretation)
    )
  }
  
  # Probability Section
  prob_html <- sprintf(
    "<ul>
      <li><strong>Binomial Distribution B(n = %d, p = %.2f):</strong> Exact P(X = %d) = <code>%.4f</code>, Cumulative P(X &le; %d) = <code>%.4f</code>, Expected Value = <code>%.2f</code>, Variance = <code>%.2f</code></li>
      <li><strong>Poisson Distribution Pois(&lambda; = %.2f):</strong> Exact P(X = %d) = <code>%.4f</code>, P(X &gt; %d) = <code>%.4f</code>, Expected Value = <code>%.2f</code>, Variance = <code>%.2f</code></li>
      <li><strong>Normal Distribution N(&mu; = %.1f, &sigma; = %.1f):</strong> Interval P(%.1f &le; X &le; %.1f) = <code>%.4f</code></li>
      <li><strong>Over Scoring Simulation (%d Overs):</strong> Empirical Mean = <code>%.2f</code> (Theor: <code>%.2f</code>), SD = <code>%.2f</code> (Theor: <code>%.2f</code>), P(Score &ge; %d) = <code>%.3f</code></li>
    </ul>",
    ifelse(!is.null(binom_res), binom_res$n, 6),
    ifelse(!is.null(binom_res), binom_res$p, 0.25),
    ifelse(!is.null(binom_res), binom_res$k, 2),
    ifelse(!is.null(binom_res), binom_res$prob_exact, 0),
    ifelse(!is.null(binom_res), binom_res$k, 2),
    ifelse(!is.null(binom_res), binom_res$prob_at_most, 0),
    ifelse(!is.null(binom_res), binom_res$expected_value, 0),
    ifelse(!is.null(binom_res), binom_res$variance, 0),
    ifelse(!is.null(pois_res), pois_res$lambda, 2.5),
    ifelse(!is.null(pois_res), pois_res$k, 3),
    ifelse(!is.null(pois_res), pois_res$prob_exact, 0),
    ifelse(!is.null(pois_res), pois_res$k, 3),
    ifelse(!is.null(pois_res), pois_res$prob_exceeds, 0),
    ifelse(!is.null(pois_res), pois_res$expected_value, 0),
    ifelse(!is.null(pois_res), pois_res$variance, 0),
    ifelse(!is.null(norm_res), norm_res$mu, 160),
    ifelse(!is.null(norm_res), norm_res$sd, 25),
    ifelse(!is.null(norm_res), norm_res$lower_val, 140),
    ifelse(!is.null(norm_res), norm_res$upper_val, 180),
    ifelse(!is.null(norm_res), norm_res$probability, 0),
    ifelse(!is.null(sim_res), sim_res$n_overs, 500),
    ifelse(!is.null(sim_res), sim_res$empirical_mean, 0),
    ifelse(!is.null(sim_res), sim_res$theor_over_mean, 0),
    ifelse(!is.null(sim_res), sim_res$empirical_sd, 0),
    ifelse(!is.null(sim_res), sim_res$theor_over_sd, 0),
    ifelse(!is.null(sim_res), sim_res$target_over_runs, 10),
    ifelse(!is.null(sim_res), sim_res$prob_reach_target, 0)
  )
  
  # Hypothesis Testing Section
  hyp_html <- "<p><em>No hypothesis test evaluated.</em></p>"
  if (!is.null(hyp_res) && isTRUE(hyp_res$valid)) {
    hyp_html <- sprintf(
      "<div>
        <p><strong>Test Executed:</strong> %s</p>
        <p><strong>Null Hypothesis:</strong> <code>%s</code></p>
        <p><strong>Alternative Hypothesis:</strong> <code>%s</code></p>
        <p><strong>Test Statistic:</strong> <code>%.4f</code> (df = %s) | <strong>p-value:</strong> <code>%.4g</code></p>
        <p><strong>Decision:</strong> <span class='badge'>%s</span></p>
        <p><strong>Statistical Interpretation:</strong> %s</p>
      </div>",
      hyp_res$test_name, hyp_res$h0, hyp_res$h1, hyp_res$statistic,
      ifelse(!is.null(hyp_res$df), as.character(hyp_res$df), "N/A"),
      hyp_res$p_value, hyp_res$decision, hyp_res$explanation
    )
  }
  
  # Chi-Square Section
  cs_html <- "<p><em>No chi-square analysis evaluated.</em></p>"
  if (!is.null(cs_res) && isTRUE(cs_res$valid)) {
    cs_html <- sprintf(
      "<div>
        <p><strong>Test Executed:</strong> %s</p>
        <p><strong>Null Hypothesis:</strong> <code>%s</code></p>
        <p><strong>Chi-Square Statistic (&chi;²):</strong> <code>%.4f</code> (df = %d) | <strong>p-value:</strong> <code>%.4g</code></p>
        <p><strong>Decision:</strong> <span class='badge'>%s</span></p>
        <p>%s</p>
        <p class='warning'>%s</p>
      </div>",
      cs_res$test_name, cs_res$h0, cs_res$statistic, cs_res$df, cs_res$p_value,
      cs_res$decision, cs_res$explanation,
      ifelse(length(cs_res$assumption_warning) > 0, cs_res$assumption_warning, "")
    )
  }
  
  # ANOVA Section
  anova_html <- "<p><em>No ANOVA test evaluated.</em></p>"
  if (!is.null(anova_res) && isTRUE(anova_res$valid)) {
    anova_tbl_rows <- ""
    for (i in seq_len(nrow(anova_res$anova_table))) {
      at <- anova_res$anova_table[i, ]
      anova_tbl_rows <- paste0(
        anova_tbl_rows,
        sprintf("<tr><td>%s</td><td>%d</td><td>%.2f</td><td>%s</td><td>%s</td><td>%s</td></tr>",
                at$Source, at$Df, at$SumSq,
                ifelse(is.na(at$MeanSq), "-", sprintf("%.2f", at$MeanSq)),
                ifelse(is.na(at$FValue), "-", sprintf("%.4f", at$FValue)),
                ifelse(is.na(at$PValue), "-", sprintf("%.4g", at$PValue)))
      )
    }
    
    anova_html <- sprintf(
      "<div>
        <p><strong>Factor Tested:</strong> %s on %s</p>
        <p><strong>F-Statistic:</strong> F(%d, %d) = <code>%.4f</code> | <strong>p-value:</strong> <code>%.4g</code></p>
        <p><strong>Decision:</strong> <span class='badge'>%s</span></p>
        <p><strong>Conclusion:</strong> %s</p>
        <table class='report-table'>
          <thead><tr><th>Source of Variation</th><th>Df</th><th>Sum Sq</th><th>Mean Sq</th><th>F Value</th><th>Pr(&gt;F)</th></tr></thead>
          <tbody>%s</tbody>
        </table>
        <p class='note'>%s</p>
      </div>",
      anova_res$group_col, anova_res$val_col,
      anova_res$anova_table$Df[1], anova_res$anova_table$Df[2],
      anova_res$f_stat, anova_res$p_val, anova_res$decision, anova_res$explanation,
      anova_tbl_rows, anova_res$diagnostics_text
    )
  }
  
  # Assemble final HTML
  sprintf(
    "<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'/>
<title>CricketEdge — Statistical Cricket Performance Report</title>
<style>
  body { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; background: #0f172a; color: #f8fafc; line-height: 1.6; margin: 0; padding: 30px; }
  .container { max-width: 1050px; margin: 0 auto; background: #1e293b; padding: 40px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
  h1 { color: #38bdf8; font-size: 28px; border-bottom: 2px solid #334155; padding-bottom: 12px; margin-top: 0; }
  h2 { color: #f59e0b; font-size: 20px; border-bottom: 1px solid #334155; padding-bottom: 6px; margin-top: 30px; }
  .meta-bar { background: #0f172a; padding: 12px 18px; border-radius: 6px; font-size: 13px; color: #94a3b8; margin-bottom: 25px; }
  .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }
  .kpi-card { background: #0f172a; padding: 15px; border-radius: 8px; border-left: 4px solid #38bdf8; text-align: center; }
  .kpi-val { font-size: 24px; font-weight: bold; color: #f8fafc; }
  .kpi-lbl { font-size: 12px; color: #94a3b8; text-transform: uppercase; margin-top: 4px; }
  .report-table { width: 100%%; border-collapse: collapse; margin: 15px 0; font-size: 13px; }
  .report-table th, .report-table td { padding: 8px 12px; text-align: left; border-bottom: 1px solid #334155; }
  .report-table th { background: #0f172a; color: #38bdf8; font-weight: 600; }
  .badge { background: #10b981; color: #0f172a; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; }
  .note { font-size: 12px; color: #94a3b8; background: #0f172a; padding: 10px 14px; border-radius: 6px; margin-top: 10px; }
  .warning { color: #f43f5e; font-size: 12px; font-weight: 600; }
  code { background: #0f172a; color: #f59e0b; padding: 2px 6px; border-radius: 4px; font-family: monospace; }
</style>
</head>
<body>
<div class='container'>
  <h1>🏏 CricketEdge — Statistical Performance Report</h1>
  <div class='meta-bar'>
    <span><strong>Active Mode:</strong> %s</span> &nbsp;|&nbsp;
    <span><strong>Innings Sampled:</strong> %d</span> &nbsp;|&nbsp;
    <span><strong>Generated At:</strong> %s</span>
  </div>

  <h2>1. Overall Descriptive Metrics</h2>
  <div class='kpi-grid'>
    <div class='kpi-card'><div class='kpi-val'>%s</div><div class='kpi-lbl'>Total Runs</div></div>
    <div class='kpi-card'><div class='kpi-val'>%.1f</div><div class='kpi-lbl'>Mean Runs / Inn</div></div>
    <div class='kpi-card'><div class='kpi-val'>%.1f</div><div class='kpi-lbl'>Overall Strike Rate</div></div>
    <div class='kpi-card'><div class='kpi-val'>%s</div><div class='kpi-lbl'>Overall Batting Avg</div></div>
  </div>

  <h2>2. Batsman Performance Comparison</h2>
  <table class='report-table'>
    <thead><tr><th>Player</th><th>Team</th><th>Innings</th><th>Runs</th><th>Mean</th><th>Median</th><th>SD</th><th>Avg</th><th>SR</th><th>Boundary %%</th><th>CV (%%)</th></tr></thead>
    <tbody>%s</tbody>
  </table>

  <h2>3. Correlation &amp; Regression Analysis</h2>
  %s

  <h2>4. Theoretical Probability &amp; Simulation Models</h2>
  %s

  <h2>5. Inferential Hypothesis Testing</h2>
  %s

  <h2>6. Chi-Square Test of Association</h2>
  %s

  <h2>7. One-Way Analysis of Variance (ANOVA)</h2>
  %s

  <h2>8. Statistical Assumptions &amp; Methodological Limitations</h2>
  <div class='note'>
    <p><strong>Cricket Analytics Domain Considerations:</strong></p>
    <ul>
      <li><strong>Linear Regression Accounting Decomposition:</strong> Regressing runs against boundaries (4s and 6s) constitutes an arithmetic breakdown rather than causal attribution, as boundary runs form an exact constituent part of total runs.</li>
      <li><strong>Clustered Independence:</strong> Matches played on identical pitches or in tournament series share pitch deterioration, weather, and ball conditions, which can introduce intra-match correlation.</li>
      <li><strong>Sample Truncation &amp; Not Outs:</strong> Batting averages are computed as Runs / Dismissals. In cases with 0 dismissals, average is undefined and represented cleanly.</li>
      <li><strong>Simulation Simplifications:</strong> The ball simulation adopts an independent multinomial distribution across balls without dynamic game-state adjustments (e.g. required run rate pressure).</li>
    </ul>
  </div>
</div>
</body>
</html>",
    active_mode, n_records, timestamp_str,
    ifelse(!is.null(overall_metrics), format(overall_metrics$total_runs, big.mark = ","), "0"),
    ifelse(!is.null(overall_metrics), overall_metrics$mean_runs, 0),
    ifelse(!is.null(overall_metrics), overall_metrics$overall_strike_rate, 0),
    ifelse(!is.null(overall_metrics), as.character(overall_metrics$batting_average), "0"),
    player_rows_html,
    reg_html,
    prob_html,
    hyp_html,
    cs_html,
    anova_html
  )
}
