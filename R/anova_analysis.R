# ==============================================================================
# CricketEdge — ANOVA & Group Comparison Module
# Implements One-Way ANOVA, Tukey HSD Post-Hoc, and Diagnostic Checks
# ==============================================================================

#' Run One-Way Analysis of Variance (ANOVA) on cricket metrics
#' @param df Cricket data frame
#' @param group_col Categorical group column (e.g. "player", "match_condition", "batting_position")
#' @param val_col Continuous response column (default: "runs")
#' @param alpha Significance level (default: 0.05)
#' @return A structured list of ANOVA table, group stats, diagnostics, post-hoc, and interpretation
run_cricket_anova <- function(df, group_col = "player", val_col = "runs", alpha = 0.05) {
  if (is.null(df) || nrow(df) < 5 || !all(c(group_col, val_col) %in% names(df))) {
    return(list(valid = FALSE, message = "Insufficient data or columns not found."))
  }
  
  sub_df <- df[complete.cases(df[, c(group_col, val_col)]), ]
  sub_df[[group_col]] <- as.factor(sub_df[[group_col]])
  
  # Need at least 2 groups with at least 2 observations each
  group_counts <- table(sub_df[[group_col]])
  valid_groups <- names(group_counts[group_counts >= 2])
  
  if (length(valid_groups) < 2) {
    return(list(valid = FALSE, message = "ANOVA requires at least 2 groups with >= 2 observations each."))
  }
  
  sub_df <- sub_df[sub_df[[group_col]] %in% valid_groups, ]
  sub_df[[group_col]] <- droplevels(sub_df[[group_col]])
  
  k_groups <- length(valid_groups)
  
  # Group summary statistics
  group_stats_list <- lapply(levels(sub_df[[group_col]]), function(grp) {
    vals <- sub_df[[val_col]][sub_df[[group_col]] == grp]
    n <- length(vals)
    m <- mean(vals)
    s <- sd(vals)
    se <- s / sqrt(n)
    ci_mult <- qt(1 - (alpha / 2), df = max(1, n - 1))
    
    data.frame(
      Group = grp,
      N = n,
      Mean = round(m, 2),
      Median = round(median(vals), 2),
      SD = round(s, 2),
      SE = round(se, 2),
      CI_Lower = round(m - ci_mult * se, 2),
      CI_Upper = round(m + ci_mult * se, 2),
      stringsAsFactors = FALSE
    )
  })
  group_stats <- do.call(rbind, group_stats_list)
  
  # Fit ANOVA model using base R aov()
  formula_obj <- as.formula(paste(val_col, "~", group_col))
  fit_aov <- aov(formula_obj, data = sub_df)
  aov_summary <- summary(fit_aov)[[1]]
  
  f_stat <- aov_summary[["F value"]][1]
  p_val <- aov_summary[["Pr(>F)"]][1]
  df_between <- aov_summary[["Df"]][1]
  df_within <- aov_summary[["Df"]][2]
  ss_between <- aov_summary[["Sum Sq"]][1]
  ss_within <- aov_summary[["Sum Sq"]][2]
  ms_between <- aov_summary[["Mean Sq"]][1]
  ms_within <- aov_summary[["Mean Sq"]][2]
  
  # Format ANOVA table as data frame
  anova_table <- data.frame(
    Source = c(group_col, "Residuals (Within Groups)", "Total"),
    Df = c(df_between, df_within, df_between + df_within),
    SumSq = round(c(ss_between, ss_within, ss_between + ss_within), 2),
    MeanSq = c(round(ms_between, 2), round(ms_within, 2), NA),
    FValue = c(round(f_stat, 4), NA, NA),
    PValue = c(p_val, NA, NA),
    stringsAsFactors = FALSE
  )
  
  # Diagnostics
  # 1. Homogeneity of variance (Bartlett's test)
  bartlett_res <- tryCatch({
    bartlett.test(formula_obj, data = sub_df)
  }, error = function(e) NULL)
  
  # 2. Normality of residuals (Shapiro-Wilk test on max 5000 resids)
  resids <- residuals(fit_aov)
  shapiro_res <- tryCatch({
    if (length(resids) >= 3 && length(resids) <= 5000) {
      shapiro.test(resids)
    } else NULL
  }, error = function(e) NULL)
  
  # Post-hoc Tukey HSD test
  tukey_res <- tryCatch({
    thsd <- TukeyHSD(fit_aov, conf.level = 1 - alpha)
    thsd_df <- as.data.frame(thsd[[1]])
    colnames(thsd_df) <- c("Diff", "LowerCI", "UpperCI", "AdjPValue")
    thsd_df$Comparison <- rownames(thsd_df)
    thsd_df$Significant <- thsd_df$AdjPValue < alpha
    thsd_df <- thsd_df[, c("Comparison", "Diff", "LowerCI", "UpperCI", "AdjPValue", "Significant")]
    thsd_df
  }, error = function(e) NULL)
  
  h0_text <- sprintf("H₀: All group population means are equal (μ₁ = μ₂ = ... = μ_%d).", k_groups)
  h1_text <- "H₁: At least one group mean differs significantly from the others."
  
  dec_reject <- (!is.na(p_val) && p_val < alpha)
  decision_text <- if (dec_reject) sprintf("Reject H₀ at α = %.2f", alpha) else sprintf("Fail to Reject H₀ at α = %.2f", alpha)
  
  explanation <- if (dec_reject) {
    sprintf("The ANOVA test yields F(%d, %d) = %.4f with p-value = %.4g (< %.2f). There is a statistically significant difference in mean %s across %s groups.",
            df_between, df_within, f_stat, p_val, alpha, val_col, group_col)
  } else {
    sprintf("The ANOVA test yields F(%d, %d) = %.4f with p-value = %.4g (≥ %.2f). We fail to reject H₀; no statistically significant difference in mean %s was detected across %s groups.",
            df_between, df_within, f_stat, p_val, alpha, val_col, group_col)
  }
  
  assumptions_text <- paste(
    "ASSUMPTION DIAGNOSTICS & LIMITATIONS:",
    sprintf("- Homogeneity of Variance (Bartlett's Test): K² = %.2f, p = %.4g (%s)",
            ifelse(is.null(bartlett_res), NA, bartlett_res$statistic),
            ifelse(is.null(bartlett_res), NA, bartlett_res$p.value),
            ifelse(!is.null(bartlett_res) && bartlett_res$p.value > 0.05, "Variances appear homogeneous", "Potential variance heterogeneity")),
    sprintf("- Normality of Residuals (Shapiro-Wilk): W = %.4f, p = %.4g (%s)",
            ifelse(is.null(shapiro_res), NA, shapiro_res$statistic),
            ifelse(is.null(shapiro_res), NA, shapiro_res$p.value),
            ifelse(!is.null(shapiro_res) && shapiro_res$p.value > 0.05, "Residuals are approximately normal", "Residuals deviate from normality (common in skewed cricket scores)")),
    "- Independence Limitation: Innings from the same tournament or match share pitch and environmental conditions, so observations may exhibit clustered variance.",
    sep = "\n"
  )
  
  list(
    valid = TRUE,
    group_col = group_col,
    val_col = val_col,
    k_groups = k_groups,
    anova_table = anova_table,
    group_stats = group_stats,
    f_stat = f_stat,
    p_val = p_val,
    h0 = h0_text,
    h1 = h1_text,
    decision = decision_text,
    explanation = explanation,
    tukey = tukey_res,
    diagnostics_text = assumptions_text,
    residuals = resids,
    model = fit_aov
  )
}
