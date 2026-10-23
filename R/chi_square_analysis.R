# ==============================================================================
# CricketEdge — Chi-Square Analysis Module
# Implements Goodness-of-Fit and Independence Tests with Assumption Validation
# ==============================================================================

#' Chi-Square Goodness-of-Fit Test
#' @param observed_counts Named or unnamed vector of observed frequency counts
#' @param expected_probs Vector of hypothesized probabilities (must sum to 1)
#' @param category_names Optional vector of category labels
#' @param alpha Significance level (default: 0.05)
#' @return A structured list of test results, contingency comparison table, and diagnostics
run_chi_square_gof <- function(observed_counts, expected_probs = NULL, category_names = NULL, alpha = 0.05) {
  observed_counts <- as.numeric(observed_counts)
  k <- length(observed_counts)
  
  if (k < 2) {
    return(list(valid = FALSE, message = "Goodness-of-fit test requires at least 2 categories."))
  }
  
  total_obs <- sum(observed_counts)
  if (total_obs <= 0) {
    return(list(valid = FALSE, message = "Total observed counts must be positive."))
  }
  
  # Default to equal / uniform distribution if expected_probs is NULL
  if (is.null(expected_probs)) {
    expected_probs <- rep(1 / k, k)
    prob_rationale <- "Null hypothesis specifies equal/uniform distribution across all categories."
  } else {
    expected_probs <- as.numeric(expected_probs)
    if (length(expected_probs) != k || any(expected_probs < 0) || sum(expected_probs) <= 0) {
      return(list(valid = FALSE, message = "Expected probabilities must match category length and be positive."))
    }
    expected_probs <- expected_probs / sum(expected_probs) # normalize strictly
    prob_rationale <- "Null hypothesis specifies user-defined theoretical benchmark distribution."
  }
  
  # Base R chisq.test
  cs <- chisq.test(x = observed_counts, p = expected_probs)
  
  exp_counts <- cs$expected
  std_resids <- cs$stdres
  
  # Cochran's rule check: all expected counts >= 1, no more than 20% < 5
  low_exp_count <- sum(exp_counts < 5)
  min_exp_count <- min(exp_counts)
  pct_low <- (low_exp_count / k) * 100
  
  assumption_warning <- character()
  if (min_exp_count < 1) {
    assumption_warning <- "WARNING: Minimum expected count < 1. Chi-square approximation is unreliable."
  } else if (pct_low > 20) {
    assumption_warning <- sprintf("WARNING: %.1f%% of cells have expected count < 5 (Cochran recommends <= 20%%). Interpret p-value with caution.", pct_low)
  }
  
  if (is.null(category_names)) {
    category_names <- names(observed_counts)
    if (is.null(category_names)) category_names <- paste("Category", 1:k)
  }
  
  table_df <- data.frame(
    Category = category_names,
    Observed = observed_counts,
    ExpectedProb = round(expected_probs, 4),
    ExpectedCount = round(exp_counts, 2),
    Difference = round(observed_counts - exp_counts, 2),
    ChiSquareContrib = round(((observed_counts - exp_counts)^2) / exp_counts, 4),
    StdResidual = round(std_resids, 3),
    stringsAsFactors = FALSE
  )
  
  h0_text <- paste("H₀: The observed distribution matches the expected distribution.", prob_rationale)
  h1_text <- "H₁: The observed distribution significantly departs from the expected distribution."
  
  dec_reject <- (cs$p.value < alpha)
  decision_text <- if (dec_reject) sprintf("Reject H₀ at α = %.2f", alpha) else sprintf("Fail to Reject H₀ at α = %.2f", alpha)
  
  explanation <- if (dec_reject) {
    sprintf("The test yields χ² = %.4f (df = %d, p = %.4g). Because p < %.2f, we reject H₀; the categorical counts deviate significantly from the expected distribution.",
            cs$statistic, cs$parameter, cs$p.value, alpha)
  } else {
    sprintf("The test yields χ² = %.4f (df = %d, p = %.4g). Because p ≥ %.2f, there is insufficient evidence to reject H₀; counts conform reasonably to the expected distribution.",
            cs$statistic, cs$parameter, cs$p.value, alpha)
  }
  
  list(
    valid = TRUE,
    test_name = "Chi-Square Goodness-of-Fit Test",
    statistic = round(as.numeric(cs$statistic), 4),
    df = as.numeric(cs$parameter),
    p_value = cs$p.value,
    alpha = alpha,
    decision = decision_text,
    explanation = explanation,
    h0 = h0_text,
    h1 = h1_text,
    table = table_df,
    assumption_warning = assumption_warning
  )
}

#' Chi-Square Test of Independence for Two Categorical Variables
#' @param df Cricket data frame
#' @param var1 Column name for first categorical variable (e.g. "player" or "match_condition")
#' @param var2 Column name for second categorical variable (e.g. "score_category" or "dismissals")
#' @param alpha Significance level (default: 0.05)
#' @return A structured list of test results, contingency matrix, expected matrix, and warnings
run_chi_square_independence <- function(df, var1, var2, alpha = 0.05) {
  if (is.null(df) || nrow(df) == 0 || !all(c(var1, var2) %in% names(df))) {
    return(list(valid = FALSE, message = "Specified variables not found in dataset."))
  }
  
  sub_df <- df[complete.cases(df[, c(var1, var2)]), ]
  if (nrow(sub_df) < 5) {
    return(list(valid = FALSE, message = "Insufficient data points for chi-square test."))
  }
  
  contingency_tbl <- table(sub_df[[var1]], sub_df[[var2]])
  
  # Check dimensions: must be at least 2x2
  if (nrow(contingency_tbl) < 2 || ncol(contingency_tbl) < 2) {
    return(list(valid = FALSE, message = "Variables must contain at least 2 distinct levels."))
  }
  
  # Base R chisq.test
  cs <- suppressWarnings(chisq.test(contingency_tbl))
  
  exp_mat <- cs$expected
  min_exp <- min(exp_mat)
  pct_low <- (sum(exp_mat < 5) / length(exp_mat)) * 100
  
  assumption_warning <- character()
  if (min_exp < 1) {
    assumption_warning <- "WARNING: Minimum expected cell count < 1. Chi-square approximation is questionable."
  } else if (pct_low > 20) {
    assumption_warning <- sprintf("WARNING: %.1f%% of contingency cells have expected counts < 5. Cochran's recommendation (<= 20%%) is exceeded.", pct_low)
  }
  
  # Format contingency tables as readable data frames
  obs_df <- as.data.frame.matrix(contingency_tbl)
  obs_df$Total <- rowSums(obs_df)
  obs_df <- rbind(obs_df, Total = colSums(obs_df))
  
  exp_df <- as.data.frame.matrix(round(exp_mat, 2))
  
  h0_text <- sprintf("H₀: %s and %s are independent (no association).", var1, var2)
  h1_text <- sprintf("H₁: %s and %s are dependent (significant association exists).", var1, var2)
  
  dec_reject <- (cs$p.value < alpha)
  decision_text <- if (dec_reject) sprintf("Reject H₀ at α = %.2f", alpha) else sprintf("Fail to Reject H₀ at α = %.2f", alpha)
  
  explanation <- if (dec_reject) {
    sprintf("With χ² = %.4f (df = %d, p = %.4g) < %.2f, we reject H₀. There is a statistically significant association between %s and %s.",
            cs$statistic, cs$parameter, cs$p.value, alpha, var1, var2)
  } else {
    sprintf("With χ² = %.4f (df = %d, p = %.4g) ≥ %.2f, we fail to reject H₀. No statistically significant association between %s and %s is detected at this significance level.",
            cs$statistic, cs$parameter, cs$p.value, alpha, var1, var2)
  }
  
  # Data for stacked bar visualization
  long_df <- as.data.frame(contingency_tbl)
  colnames(long_df) <- c("Var1", "Var2", "Count")
  
  list(
    valid = TRUE,
    test_name = "Chi-Square Test of Independence",
    var1 = var1,
    var2 = var2,
    statistic = round(as.numeric(cs$statistic), 4),
    df = as.numeric(cs$parameter),
    p_value = cs$p.value,
    alpha = alpha,
    decision = decision_text,
    explanation = explanation,
    h0 = h0_text,
    h1 = h1_text,
    observed_table = obs_df,
    expected_table = exp_df,
    plot_data = long_df,
    assumption_warning = assumption_warning
  )
}
