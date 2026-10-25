# ==============================================================================
# CricketEdge — Visualization Module (ggplot2)
# Implements High-Fidelity Graphs Faithful to Underlying Mathematical Models
# ==============================================================================

suppressPackageStartupMessages(library(ggplot2))

#' Custom High-Contrast Professional Light Theme for CricketEdge
theme_cricketedge <- function(base_size = 12) {
  theme_minimal(base_size = base_size) +
    theme(
      plot.background = element_rect(fill = "transparent", color = NA),
      panel.background = element_rect(fill = "#ffffff", color = "#e2e8f0", linewidth = 0.5),
      panel.grid.major = element_line(color = "#f1f5f9", linewidth = 0.5),
      panel.grid.minor = element_blank(),
      text = element_text(color = "#334155", family = "sans"),
      axis.text = element_text(color = "#64748b", size = 10),
      axis.title = element_text(color = "#0f172a", face = "bold", size = 11),
      plot.title = element_text(color = "#0f172a", face = "bold", size = 13, hjust = 0, margin = margin(b = 4)),
      plot.subtitle = element_text(color = "#64748b", size = 10, hjust = 0, margin = margin(b = 8)),
      plot.caption = element_text(color = "#94a3b8", size = 8.5, hjust = 1, margin = margin(t = 6)),
      legend.background = element_rect(fill = "#ffffff", color = "#e2e8f0", linewidth = 0.5),
      legend.text = element_text(color = "#334155", size = 9.5),
      legend.title = element_text(color = "#0f172a", face = "bold", size = 10),
      legend.key = element_rect(fill = "transparent", color = NA),
      strip.background = element_rect(fill = "#f8fafc", color = "#e2e8f0"),
      strip.text = element_text(color = "#0f172a", face = "bold", size = 10.5),
      plot.margin = margin(t = 10, r = 18, b = 10, l = 10)
    )
}

# Standardized Color Palette
CRICKET_PALETTE <- c(
  cyan = "#38bdf8",
  gold = "#f59e0b",
  emerald = "#10b981",
  coral = "#f43f5e",
  purple = "#a855f7",
  indigo = "#6366f1",
  teal = "#14b8a6",
  amber = "#fbbf24"
)

#' Plot Runs by Player (Bar chart)
plot_runs_by_player <- function(df) {
  if (is.null(df) || nrow(df) == 0) return(NULL)
  
  agg <- aggregate(runs ~ player + team, data = df, sum)
  agg <- agg[order(agg$runs, decreasing = TRUE), ]
  agg$player <- factor(agg$player, levels = rev(agg$player))
  
  max_r <- max(agg$runs, na.rm = TRUE)
  
  ggplot(agg, aes(x = player, y = runs, fill = team)) +
    geom_col(width = 0.68, alpha = 0.92) +
    geom_text(aes(label = format(runs, big.mark = ",")), hjust = -0.12, color = "#0f172a", size = 3.6, fontface = "bold") +
    coord_flip(clip = "off") +
    scale_y_continuous(expand = expansion(mult = c(0, 0.22))) +
    scale_fill_manual(values = c("India" = "#38bdf8", "England" = "#f43f5e", "Australia" = "#fbbf24", "New Zealand" = "#10b981")) +
    labs(
      title = "Cumulative Innings Runs by Batsman",
      subtitle = sprintf("Calculated across %d filtered innings", nrow(df)),
      x = NULL,
      y = "Total Runs",
      fill = "Team"
    ) +
    theme_cricketedge() +
    theme(
      legend.position = "bottom",
      legend.direction = "horizontal",
      legend.margin = margin(t = -5)
    )
}

#' Plot Runs Distribution (Histogram and Density)
plot_runs_distribution <- function(df) {
  if (is.null(df) || nrow(df) == 0) return(NULL)
  
  mean_val <- mean(df$runs, na.rm = TRUE)
  med_val <- median(df$runs, na.rm = TRUE)
  
  ggplot(df, aes(x = runs)) +
    geom_histogram(aes(y = after_stat(density)), binwidth = 10, fill = "#0284c7", color = "#0f172a", alpha = 0.75) +
    geom_density(color = "#f59e0b", linewidth = 1.2) +
    geom_vline(xintercept = mean_val, linetype = "dashed", color = "#10b981", linewidth = 1) +
    geom_vline(xintercept = med_val, linetype = "dotted", color = "#f43f5e", linewidth = 1) +
    labs(
      title = "Score Distribution & Central Tendency",
      subtitle = sprintf("Green Dashed: Mean = %.1f  |  Red Dotted: Median = %.1f", mean_val, med_val),
      x = "Runs Scored in Innings",
      y = "Empirical Density",
      caption = "Histogram with overlaid Gaussian kernel density curve"
    ) +
    theme_cricketedge()
}

#' Plot Player Comparison Boxplots
plot_player_comparison_boxplots <- function(df, selected_players) {
  if (is.null(df) || nrow(df) == 0) return(NULL)
  sub_df <- df[df$player %in% selected_players, , drop = FALSE]
  if (nrow(sub_df) == 0) return(NULL)
  
  ggplot(sub_df, aes(x = player, y = runs, fill = player)) +
    geom_boxplot(alpha = 0.45, outlier.color = "#f43f5e", outlier.size = 2.2, color = "#94a3b8", width = 0.55) +
    geom_jitter(width = 0.16, alpha = 0.6, size = 1.8, color = "#f8fafc") +
    stat_summary(fun = mean, geom = "point", shape = 18, size = 4.2, color = "#f59e0b") +
    scale_fill_brewer(palette = "Set2") +
    labs(
      title = "Innings Score Spread by Selected Batsmen",
      subtitle = "Boxplots (Median & IQR) with Jittered Innings and Mean (Gold Diamond)",
      x = NULL,
      y = "Runs per Innings"
    ) +
    theme_cricketedge() +
    theme(legend.position = "none")
}

#' Plot Scatter: Runs vs Balls Faced
plot_runs_vs_balls_scatter <- function(df, selected_players = NULL) {
  if (is.null(df) || nrow(df) == 0) return(NULL)
  plot_df <- if (!is.null(selected_players) && length(selected_players) > 0) {
    df[df$player %in% selected_players, , drop = FALSE]
  } else df
  
  ggplot(plot_df, aes(x = balls_faced, y = runs, color = player)) +
    geom_point(alpha = 0.75, size = 2.4) +
    geom_smooth(method = "lm", formula = y ~ x, se = FALSE, color = "#f59e0b", linetype = "dashed", linewidth = 0.8) +
    scale_color_brewer(palette = "Set2") +
    labs(
      title = "Scoring Acceleration: Runs vs Balls Faced",
      subtitle = sprintf("Sample size: %d innings | Gold dashed: Overall linear trend", nrow(plot_df)),
      x = "Balls Faced",
      y = "Runs Scored",
      color = "Player"
    ) +
    theme_cricketedge() +
    theme(legend.position = "bottom")
}

#' Plot Simple Linear Regression with Fitted Line and Diagnostics
plot_simple_regression <- function(reg_result) {
  if (!reg_result$valid) return(NULL)
  diag <- reg_result$diagnostics
  
  ggplot(diag, aes(x = observed_x, y = observed_y)) +
    geom_point(color = "#38bdf8", alpha = 0.65, size = 2.3) +
    geom_line(aes(y = fitted), color = "#f59e0b", linewidth = 1.3) +
    labs(
      title = "Fitted Simple Linear Regression",
      subtitle = sprintf("Model: %s  |  R² = %.4f", reg_result$equation, reg_result$r_squared),
      x = "Predictor Variable",
      y = "Observed Runs",
      caption = "Points = Observed Innings | Gold Line = lm() Fitted Values"
    ) +
    theme_cricketedge()
}

#' Plot Regression Residuals vs Fitted
plot_regression_residuals <- function(reg_result) {
  if (!reg_result$valid) return(NULL)
  diag <- reg_result$diagnostics
  
  ggplot(diag, aes(x = fitted, y = residuals)) +
    geom_hline(yintercept = 0, linetype = "dashed", color = "#f43f5e", linewidth = 1) +
    geom_point(color = "#38bdf8", alpha = 0.7, size = 2.3) +
    geom_smooth(method = "loess", formula = y ~ x, color = "#10b981", se = FALSE, linewidth = 0.9) +
    labs(
      title = "Residual Diagnostics: Residuals vs Fitted Values",
      subtitle = "Checking for constant variance and non-linearity (Residual = Observed - Fitted)",
      x = "Fitted Values (Predicted Runs)",
      y = "Residuals",
      caption = "Red line: Zero error baseline | Green curve: Loess trend"
    ) +
    theme_cricketedge()
}

#' Plot Binomial Distribution (Discrete Spikes / Lollipop)
plot_binomial_distribution <- function(binom_res) {
  df <- binom_res$data
  
  ggplot(df, aes(x = x, y = probability)) +
    geom_segment(aes(xend = x, y = 0, yend = probability, color = is_target), linewidth = 1.4) +
    geom_point(aes(color = is_target), size = 3.6) +
    scale_color_manual(values = c("FALSE" = "#38bdf8", "TRUE" = "#f59e0b"), guide = "none") +
    scale_x_continuous(breaks = df$x) +
    labs(
      title = sprintf("Binomial Distribution: B(n = %d, p = %.2f)", binom_res$n, binom_res$p),
      subtitle = sprintf("Exact P(X = %d) = %.4f | Cumulative P(X <= %d) = %.4f | E[X] = %.2f",
                         binom_res$k, binom_res$prob_exact, binom_res$k, binom_res$prob_at_most,
                         binom_res$expected_value),
      x = "Values of x (Number of Successes)",
      y = "Probability P(X = x)",
      caption = "R dbinom() mass function | Gold = Selected Target k"
    ) +
    theme_cricketedge()
}

#' Plot Poisson Distribution (Discrete Spikes)
plot_poisson_distribution <- function(pois_res) {
  df <- pois_res$data
  
  ggplot(df, aes(x = x, y = probability)) +
    geom_segment(aes(xend = x, y = 0, yend = probability, color = is_target), linewidth = 1.3) +
    geom_point(aes(color = is_target), size = 3.2) +
    scale_color_manual(values = c("FALSE" = "#10b981", "TRUE" = "#f59e0b"), guide = "none") +
    scale_x_continuous(breaks = seq(0, max(df$x), by = max(1, round(max(df$x)/10)))) +
    labs(
      title = sprintf("Poisson Distribution: Pois(λ = %.2f)", pois_res$lambda),
      subtitle = sprintf("Exact P(X = %d) = %.4f | P(X > %d) = %.4f | E[X] = Var(X) = %.2f",
                         pois_res$k, pois_res$prob_exact, pois_res$k, pois_res$prob_exceeds,
                         pois_res$expected_value),
      x = "Values of x (Event Count)",
      y = "Probability P(X = x)",
      caption = "R dpois() discrete mass function | Gold = Target k"
    ) +
    theme_cricketedge()
}

#' Plot Normal Distribution with Shaded Interval Probability
plot_normal_distribution <- function(norm_res) {
  curve_df <- norm_res$curve_data
  shade_df <- norm_res$shade_data
  
  p <- ggplot(curve_df, aes(x = x, y = density)) +
    geom_line(color = "#38bdf8", linewidth = 1.2)
  
  if (nrow(shade_df) > 0) {
    p <- p + geom_area(data = shade_df, fill = "#f59e0b", alpha = 0.5)
  }
  
  label_region <- switch(
    norm_res$region_type,
    "between" = sprintf("P(%.1f <= X <= %.1f) = %.4f", norm_res$lower_val, norm_res$upper_val, norm_res$probability),
    "below" = sprintf("P(X <= %.1f) = %.4f", norm_res$upper_val, norm_res$probability),
    "above" = sprintf("P(X >= %.1f) = %.4f", norm_res$lower_val, norm_res$probability)
  )
  
  p + geom_vline(xintercept = norm_res$mu, linetype = "dashed", color = "#10b981", linewidth = 0.9) +
    labs(
      title = sprintf("Normal Distribution: N(μ = %.1f, σ = %.1f)", norm_res$mu, norm_res$sd),
      subtitle = sprintf("Theoretical Probability: %s (Calculated via pnorm)", label_region),
      x = "x (Continuous Variable)",
      y = "Probability Density f(x)",
      caption = "Curve = dnorm() | Shaded Area = Cumulative Probability via pnorm()"
    ) +
    theme_cricketedge()
}

#' Plot Simulated Cricket Over Scoring Totals
plot_cricket_simulation_totals <- function(sim_res) {
  df <- sim_res$plot_data
  target <- sim_res$target_over_runs
  
  ggplot(df, aes(x = OverScore, y = EmpiricalProb)) +
    geom_col(aes(fill = (OverScore >= target)), width = 0.72, alpha = 0.88) +
    geom_vline(xintercept = sim_res$theor_over_mean, color = "#10b981", linetype = "dashed", linewidth = 1) +
    geom_vline(xintercept = target - 0.5, color = "#f43f5e", linetype = "dotted", linewidth = 1.1) +
    scale_fill_manual(values = c("FALSE" = "#38bdf8", "TRUE" = "#f59e0b"),
                      labels = c(sprintf("< %d runs", target), sprintf(">= %d runs (Target)", target)),
                      name = "Over Outcome") +
    labs(
      title = sprintf("Simulated Over Runs Distribution (%d Overs)", sim_res$n_overs),
      subtitle = sprintf("Empirical Mean: %.2f (Theor: %.2f)  |  P(Score >= %d): %.1f%%",
                         sim_res$empirical_mean, sim_res$theor_over_mean, target, sim_res$prob_reach_target * 100),
      x = "Total Runs in 6-Ball Over",
      y = "Empirical Probability",
      caption = "Dotted Red: Target Cutoff | Green Dashed: Theoretical Over Mean"
    ) +
    theme_cricketedge() +
    theme(legend.position = "bottom")
}

#' Plot Chi-Square Goodness-of-Fit Comparison (Observed vs Expected)
plot_chi_square_gof <- function(gof_res) {
  if (!gof_res$valid) return(NULL)
  tbl <- gof_res$table
  
  plot_df <- rbind(
    data.frame(Category = tbl$Category, Type = "Observed", Count = tbl$Observed),
    data.frame(Category = tbl$Category, Type = "Expected", Count = tbl$ExpectedCount)
  )
  plot_df$Category <- factor(plot_df$Category, levels = tbl$Category)
  
  ggplot(plot_df, aes(x = Category, y = Count, fill = Type)) +
    geom_col(position = position_dodge(width = 0.75), width = 0.65, alpha = 0.9) +
    scale_fill_manual(values = c("Observed" = "#38bdf8", "Expected" = "#f59e0b")) +
    labs(
      title = "Chi-Square Goodness-of-Fit: Observed vs Expected Counts",
      subtitle = sprintf("χ² = %.4f | df = %d | p-value = %.4g (%s)",
                         gof_res$statistic, gof_res$df, gof_res$p_value, gof_res$decision),
      x = "Category",
      y = "Count",
      fill = "Frequency"
    ) +
    theme_cricketedge() +
    theme(legend.position = "bottom")
}

#' Plot Chi-Square Contingency Association (Stacked / Grouped Bar)
plot_chi_square_contingency <- function(ind_res) {
  if (!ind_res$valid) return(NULL)
  df <- ind_res$plot_data
  
  ggplot(df, aes(x = Var1, y = Count, fill = Var2)) +
    geom_col(position = "fill", alpha = 0.9, width = 0.65) +
    scale_y_continuous(labels = scales::percent_format()) +
    scale_fill_brewer(palette = "Set3") +
    labs(
      title = sprintf("Contingency Proportions: %s across %s", ind_res$var2, ind_res$var1),
      subtitle = sprintf("χ² = %.4f | df = %d | p-value = %.4g (%s)",
                         ind_res$statistic, ind_res$df, ind_res$p_value, ind_res$decision),
      x = ind_res$var1,
      y = "Within-Group Proportion",
      fill = ind_res$var2
    ) +
    theme_cricketedge() +
    theme(legend.position = "bottom")
}

#' Plot ANOVA Groups Comparison Boxplots with Overlaid Confidence Means
plot_anova_groups <- function(anova_res, df) {
  if (!anova_res$valid) return(NULL)
  grp_col <- anova_res$group_col
  val_col <- anova_res$val_col
  
  ggplot(df, aes(x = .data[[grp_col]], y = .data[[val_col]], fill = .data[[grp_col]])) +
    geom_boxplot(alpha = 0.45, outlier.color = "#f43f5e", color = "#94a3b8", width = 0.55) +
    geom_jitter(width = 0.15, alpha = 0.5, size = 1.8, color = "#f8fafc") +
    stat_summary(fun = mean, geom = "point", shape = 18, size = 4.5, color = "#f59e0b") +
    stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.22, color = "#f59e0b", linewidth = 1.1) +
    labs(
      title = sprintf("One-Way ANOVA: %s across %s", val_col, grp_col),
      subtitle = sprintf("F(%d, %d) = %.4f | p-value = %.4g (%s)",
                         anova_res$anova_table$Df[1], anova_res$anova_table$Df[2],
                         anova_res$f_stat, anova_res$p_val, anova_res$decision),
      x = grp_col,
      y = val_col,
      caption = "Boxplot: Median & IQR | Gold Diamond & Error Bar: Mean ± SE"
    ) +
    theme_cricketedge() +
    theme(legend.position = "none")
}
