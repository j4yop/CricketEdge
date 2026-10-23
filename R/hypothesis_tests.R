# ==============================================================================
# CricketEdge — Hypothesis Testing Module
# Implements 1-Sample, 2-Sample, Independent, and Paired Statistical Tests
# ==============================================================================

#' Format the statistical decision based on p-value and significance level alpha
#' @param p_val Computed p-value
#' @param alpha Chosen significance level (e.g. 0.05)
#' @return A list with decision string and explanation
format_hypothesis_decision <- function(p_val, alpha = 0.05) {
  if (is.na(p_val)) {
    return(list(
      reject = FALSE,
      decision = "Indeterminate",
      explanation = "Test could not calculate a valid p-value."
    ))
  }
  
  if (p_val < alpha) {
    list(
      reject = TRUE,
      decision = sprintf("Reject H₀ at α = %.2f", alpha),
      explanation = sprintf("Since p-value (%.4g) < α (%.2f), there is statistically significant evidence to reject the null hypothesis in favor of the alternative hypothesis.", p_val, alpha)
    )
  } else {
    list(
      reject = FALSE,
      decision = sprintf("Fail to Reject H₀ at α = %.2f", alpha),
      explanation = sprintf("Since p-value (%.4g) ≥ α (%.2f), there is insufficient sample evidence to reject the null hypothesis. (Note: We do not 'accept' H₀ as proven true; the data simply does not contradict it at this significance level.)", p_val, alpha)
    )
  }
}

#' One-Sample t-Test for Mean Runs
#' @param x Numeric vector of observed values
#' @param mu0 Hypothesized population mean
#' @param alternative "two.sided", "greater", or "less"
#' @param conf_level Confidence level (default: 0.95)
#' @param label Optional variable or player label
#' @return Structured test results list
run_one_sample_t_test <- function(x, mu0 = 35, alternative = "two.sided", conf_level = 0.95, label = "Sample") {
  x <- x[!is.na(x)]
  n <- length(x)
  if (n < 2) {
    return(list(valid = FALSE, message = "One-sample t-test requires at least 2 non-missing observations."))
  }
  
  sample_mean <- mean(x)
  sample_sd <- sd(x)
  
  # Standard R t.test
  tt <- t.test(x, mu = mu0, alternative = alternative, conf.level = conf_level)
  
  alt_symbol <- switch(alternative, "two.sided" = "≠", "greater" = ">", "less" = "<")
  h0_text <- sprintf("H₀: μ = %.2f (The true mean of %s equals %.2f)", mu0, label, mu0)
  h1_text <- sprintf("H₁: μ %s %.2f (The true mean of %s %s %.2f)", alt_symbol, mu0, label, alt_symbol, mu0)
  
  dec <- format_hypothesis_decision(tt$p.value, 1 - conf_level)
  
  list(
    valid = TRUE,
    test_name = "One-Sample t-Test for Population Mean",
    label = label,
    n = n,
    sample_mean = round(sample_mean, 2),
    sample_sd = round(sample_sd, 2),
    mu0 = mu0,
    statistic = round(as.numeric(tt$statistic), 4),
    df = round(as.numeric(tt$parameter), 2),
    p_value = tt$p.value,
    conf_level = conf_level,
    conf_int = c(round(tt$conf.int[1], 2), round(tt$conf.int[2], 2)),
    alternative = alternative,
    h0 = h0_text,
    h1 = h1_text,
    decision = dec$decision,
    explanation = dec$explanation
  )
}

#' One-Sample Test for Proportion
#' @param successes Number of successes
#' @param total Total trials
#' @param p0 Hypothesized proportion (0 < p0 < 1)
#' @param alternative "two.sided", "greater", or "less"
#' @param conf_level Confidence level (default: 0.95)
#' @param label Optional label
#' @return Structured test results list
run_one_sample_prop_test <- function(successes, total, p0 = 0.20, alternative = "two.sided", conf_level = 0.95, label = "Metric") {
  if (total <= 0 || successes < 0 || successes > total) {
    return(list(valid = FALSE, message = "Invalid success count or total trials."))
  }
  
  # Base R prop.test
  pt <- prop.test(x = successes, n = total, p = p0, alternative = alternative, conf.level = conf_level, correct = FALSE)
  sample_prop <- successes / total
  
  alt_symbol <- switch(alternative, "two.sided" = "≠", "greater" = ">", "less" = "<")
  h0_text <- sprintf("H₀: p = %.3f (The true proportion of %s equals %.3f)", p0, label, p0)
  h1_text <- sprintf("H₁: p %s %.3f (The true proportion of %s %s %.3f)", alt_symbol, p0, label, alt_symbol, p0)
  
  dec <- format_hypothesis_decision(pt$p.value, 1 - conf_level)
  
  list(
    valid = TRUE,
    test_name = "One-Sample Test for Population Proportion (Score Test)",
    label = label,
    successes = successes,
    total = total,
    sample_prop = round(sample_prop, 4),
    p0 = p0,
    statistic = round(as.numeric(pt$statistic), 4),
    df = as.numeric(pt$parameter),
    p_value = pt$p.value,
    conf_level = conf_level,
    conf_int = c(round(pt$conf.int[1], 4), round(pt$conf.int[2], 4)),
    alternative = alternative,
    h0 = h0_text,
    h1 = h1_text,
    decision = dec$decision,
    explanation = dec$explanation
  )
}

#' Two-Sample Independent t-Test for Means
#' @param x Numeric vector for group 1
#' @param y Numeric vector for group 2
#' @param label1 Label for group 1
#' @param label2 Label for group 2
#' @param var_equal Logical indicating whether to assume equal variance (Student's vs Welch's)
#' @param alternative "two.sided", "greater", or "less"
#' @param conf_level Confidence level (default: 0.95)
#' @return Structured test results list
run_two_sample_t_test <- function(x, y, label1 = "Group 1", label2 = "Group 2", var_equal = FALSE,
                                  alternative = "two.sided", conf_level = 0.95) {
  x <- x[!is.na(x)]
  y <- y[!is.na(y)]
  
  if (length(x) < 2 || length(y) < 2) {
    return(list(valid = FALSE, message = "Both groups must have at least 2 non-missing observations."))
  }
  
  # Standard R t.test
  tt <- t.test(x, y, var.equal = var_equal, alternative = alternative, conf.level = conf_level)
  
  mean1 <- mean(x)
  mean2 <- mean(y)
  sd1 <- sd(x)
  sd2 <- sd(y)
  
  alt_symbol <- switch(alternative, "two.sided" = "≠", "greater" = ">", "less" = "<")
  h0_text <- sprintf("H₀: μ₁ - μ₂ = 0 (Mean %s equals Mean %s)", label1, label2)
  h1_text <- sprintf("H₁: μ₁ %s μ₂ (Mean %s %s Mean %s)", alt_symbol, label1, alt_symbol, label2)
  
  dec <- format_hypothesis_decision(tt$p.value, 1 - conf_level)
  test_type <- ifelse(var_equal, "Two-Sample Independent Student's t-Test (Equal Variance Assumed)",
                             "Two-Sample Welch's t-Test (Unequal Variance Robust)")
  
  list(
    valid = TRUE,
    test_name = test_type,
    label1 = label1,
    label2 = label2,
    n1 = length(x),
    n2 = length(y),
    mean1 = round(mean1, 2),
    mean2 = round(mean2, 2),
    sd1 = round(sd1, 2),
    sd2 = round(sd2, 2),
    mean_diff = round(mean1 - mean2, 2),
    statistic = round(as.numeric(tt$statistic), 4),
    df = round(as.numeric(tt$parameter), 2),
    p_value = tt$p.value,
    conf_level = conf_level,
    conf_int = c(round(tt$conf.int[1], 2), round(tt$conf.int[2], 2)),
    alternative = alternative,
    var_equal = var_equal,
    h0 = h0_text,
    h1 = h1_text,
    decision = dec$decision,
    explanation = dec$explanation
  )
}

#' Two-Sample Test for Comparing Proportions
#' @param s1 Successes in group 1
#' @param n1 Trials in group 1
#' @param s2 Successes in group 2
#' @param n2 Trials in group 2
#' @param label1 Label for group 1
#' @param label2 Label for group 2
#' @param alternative "two.sided", "greater", or "less"
#' @param conf_level Confidence level (default: 0.95)
#' @return Structured test results list
run_two_sample_prop_test <- function(s1, n1, s2, n2, label1 = "Group 1", label2 = "Group 2",
                                     alternative = "two.sided", conf_level = 0.95) {
  if (n1 <= 0 || n2 <= 0 || s1 < 0 || s2 < 0 || s1 > n1 || s2 > n2) {
    return(list(valid = FALSE, message = "Invalid trial or success counts."))
  }
  
  pt <- prop.test(c(s1, s2), c(n1, n2), alternative = alternative, conf.level = conf_level, correct = FALSE)
  p1 <- s1 / n1
  p2 <- s2 / n2
  
  alt_symbol <- switch(alternative, "two.sided" = "≠", "greater" = ">", "less" = "<")
  h0_text <- sprintf("H₀: p₁ - p₂ = 0 (Proportion %s equals Proportion %s)", label1, label2)
  h1_text <- sprintf("H₁: p₁ %s p₂ (Proportion %s %s Proportion %s)", alt_symbol, label1, alt_symbol, label2)
  
  dec <- format_hypothesis_decision(pt$p.value, 1 - conf_level)
  
  list(
    valid = TRUE,
    test_name = "Two-Sample Test for Comparing Proportions (Chi-Square / Normal Approximation)",
    label1 = label1,
    label2 = label2,
    s1 = s1, n1 = n1, p1 = round(p1, 4),
    s2 = s2, n2 = n2, p2 = round(p2, 4),
    prop_diff = round(p1 - p2, 4),
    statistic = round(as.numeric(pt$statistic), 4),
    df = as.numeric(pt$parameter),
    p_value = pt$p.value,
    conf_level = conf_level,
    conf_int = c(round(pt$conf.int[1], 4), round(pt$conf.int[2], 4)),
    alternative = alternative,
    h0 = h0_text,
    h1 = h1_text,
    decision = dec$decision,
    explanation = dec$explanation
  )
}

#' Paired t-Test for Genuinely Paired Observations
#' (e.g., Comparing Match Innings 1 vs Innings 2 Totals across identical matches)
#' @param df Cricket dataset containing match pairs
#' @param match_col Match identifier column (default: "match_id")
#' @param innings_col Column identifying innings 1 vs 2
#' @param val_col Numeric value column to compare (e.g. "innings_total")
#' @param alternative "two.sided", "greater", or "less"
#' @param conf_level Confidence level (default: 0.95)
#' @return Structured test results list
run_paired_t_test <- function(df, match_col = "match_id", innings_col = "innings",
                              val_col = "innings_total", alternative = "two.sided", conf_level = 0.95) {
  if (is.null(df) || nrow(df) == 0) {
    return(list(valid = FALSE, message = "Dataset is empty."))
  }
  
  # Extract distinct match innings records
  match_innings <- unique(df[, c(match_col, innings_col, val_col)])
  match_innings <- match_innings[complete.cases(match_innings), ]
  
  inn1 <- match_innings[match_innings[[innings_col]] == 1, ]
  inn2 <- match_innings[match_innings[[innings_col]] == 2, ]
  
  # Find intersecting matches that have both innings
  common_matches <- intersect(inn1[[match_col]], inn2[[match_col]])
  if (length(common_matches) < 3) {
    return(list(valid = FALSE, message = "Paired t-test requires at least 3 matches with both 1st and 2nd innings recorded."))
  }
  
  paired_data <- merge(
    inn1[inn1[[match_col]] %in% common_matches, c(match_col, val_col)],
    inn2[inn2[[match_col]] %in% common_matches, c(match_col, val_col)],
    by = match_col,
    suffixes = c("_inn1", "_inn2")
  )
  
  # Deduplicate in case of multiple rows per match
  paired_data <- paired_data[!duplicated(paired_data[[match_col]]), ]
  
  x <- paired_data[[paste0(val_col, "_inn1")]]
  y <- paired_data[[paste0(val_col, "_inn2")]]
  
  diffs <- x - y
  tt <- t.test(x, y, paired = TRUE, alternative = alternative, conf.level = conf_level)
  
  alt_symbol <- switch(alternative, "two.sided" = "≠", "greater" = ">", "less" = "<")
  h0_text <- "H₀: μ_diff = 0 (Mean difference between 1st and 2nd innings totals is zero)"
  h1_text <- sprintf("H₁: μ_diff %s 0 (Mean difference between 1st and 2nd innings totals %s 0)", alt_symbol, alt_symbol)
  
  dec <- format_hypothesis_decision(tt$p.value, 1 - conf_level)
  
  list(
    valid = TRUE,
    test_name = "Paired-Sample t-Test (1st Innings vs 2nd Innings Totals)",
    n_pairs = length(diffs),
    mean_inn1 = round(mean(x), 2),
    mean_inn2 = round(mean(y), 2),
    mean_diff = round(mean(diffs), 2),
    sd_diff = round(sd(diffs), 2),
    statistic = round(as.numeric(tt$statistic), 4),
    df = as.numeric(tt$parameter),
    p_value = tt$p.value,
    conf_level = conf_level,
    conf_int = c(round(tt$conf.int[1], 2), round(tt$conf.int[2], 2)),
    alternative = alternative,
    h0 = h0_text,
    h1 = h1_text,
    decision = dec$decision,
    explanation = dec$explanation
  )
}
