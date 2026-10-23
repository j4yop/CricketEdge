# ==============================================================================
# CricketEdge — Regression Analysis Module
# Implements Simple and Multiple Linear Regression with Model Diagnostics
# ==============================================================================

#' Fit Simple Linear Regression model using base R lm()
#' @param df Cricket data frame
#' @param response Response variable name (default: "runs")
#' @param predictor Predictor variable name (default: "balls_faced")
#' @return A list containing model, summary, metrics, equation, and diagnostics
fit_simple_regression <- function(df, response = "runs", predictor = "balls_faced") {
  if (is.null(df) || nrow(df) < 3) {
    return(list(valid = FALSE, message = "Insufficient data points to fit regression (requires >= 3 observations)."))
  }
  
  if (!all(c(response, predictor) %in% names(df))) {
    return(list(valid = FALSE, message = sprintf("Columns '%s' and '%s' must exist in dataset.", response, predictor)))
  }
  
  sub_df <- df[complete.cases(df[, c(response, predictor)]), ]
  if (nrow(sub_df) < 3) {
    return(list(valid = FALSE, message = "Insufficient complete observations."))
  }
  
  # Correlation test
  cor_res <- cor.test(sub_df[[predictor]], sub_df[[response]], method = "pearson")
  
  # Fit linear model
  formula_obj <- as.formula(paste(response, "~", predictor))
  fit <- lm(formula_obj, data = sub_df)
  fit_sum <- summary(fit)
  
  # Coefficients table
  coef_df <- as.data.frame(fit_sum$coefficients)
  colnames(coef_df) <- c("Estimate", "StdError", "tValue", "pValue")
  coef_df$Significance <- cut(
    coef_df$pValue,
    breaks = c(-Inf, 0.001, 0.01, 0.05, 0.1, Inf),
    labels = c("***", "**", "*", ".", "ns")
  )
  
  b0 <- coef(fit)[1]
  b1 <- coef(fit)[2]
  sign_str <- ifelse(b1 >= 0, "+", "-")
  equation <- sprintf("%s = %.3f %s %.3f * %s", response, b0, sign_str, abs(b1), predictor)
  
  # Overall F-test p-value
  f_stat <- fit_sum$fstatistic
  f_p_val <- if (!is.null(f_stat)) {
    pf(f_stat[1], f_stat[2], f_stat[3], lower.tail = FALSE)
  } else NA_real_
  
  # Diagnostic vectors
  diag_df <- data.frame(
    observed_x = sub_df[[predictor]],
    observed_y = sub_df[[response]],
    fitted = fitted(fit),
    residuals = residuals(fit),
    std_residuals = rstandard(fit)
  )
  
  # Plain-English interpretation
  interpretation <- sprintf(
    "Linear regression shows that for each additional %s, %s changes by an estimated %.2f units (t = %.2f, p = %.4g). The model explains %.1f%% of the variance in %s (R² = %.4f). Note: This reflects statistical association, not necessarily direct causality.",
    predictor, response, b1, coef_df$tValue[2], coef_df$pValue[2], fit_sum$r.squared * 100, response, fit_sum$r.squared
  )
  
  list(
    valid = TRUE,
    model = fit,
    formula = formula_obj,
    equation = equation,
    coefficients = coef_df,
    r_squared = fit_sum$r.squared,
    adj_r_squared = fit_sum$adj.r.squared,
    residual_se = fit_sum$sigma,
    f_statistic = if (!is.null(f_stat)) as.numeric(f_stat[1]) else NA_real_,
    f_p_value = f_p_val,
    df = fit_sum$df,
    correlation = cor_res$estimate,
    cor_p_value = cor_res$p.value,
    cor_conf_int = cor_res$conf.int,
    diagnostics = diag_df,
    interpretation = interpretation
  )
}

#' Fit Multiple Linear Regression model
#' @param df Cricket data frame
#' @param response Response variable (default: "runs")
#' @param predictors Character vector of predictors (default: c("balls_faced", "fours", "sixes"))
#' @return A list containing model, summary, metrics, and diagnostics
fit_multiple_regression <- function(df, response = "runs", predictors = c("balls_faced", "fours", "sixes")) {
  if (is.null(df) || nrow(df) <= length(predictors) + 2) {
    return(list(valid = FALSE, message = "Insufficient data points for the number of predictors."))
  }
  
  needed_cols <- c(response, predictors)
  if (!all(needed_cols %in% names(df))) {
    return(list(valid = FALSE, message = "Specified response or predictors not found in data."))
  }
  
  sub_df <- df[complete.cases(df[, needed_cols]), ]
  if (nrow(sub_df) <= length(predictors) + 2) {
    return(list(valid = FALSE, message = "Insufficient complete observations."))
  }
  
  form_str <- paste(response, "~", paste(predictors, collapse = " + "))
  formula_obj <- as.formula(form_str)
  
  fit <- lm(formula_obj, data = sub_df)
  fit_sum <- summary(fit)
  
  # Coefficients table
  coef_df <- as.data.frame(fit_sum$coefficients)
  colnames(coef_df) <- c("Estimate", "StdError", "tValue", "pValue")
  coef_df$Significance <- cut(
    coef_df$pValue,
    breaks = c(-Inf, 0.001, 0.01, 0.05, 0.1, Inf),
    labels = c("***", "**", "*", ".", "ns")
  )
  
  # Build readable equation string
  coefs <- coef(fit)
  terms <- paste(sapply(names(coefs)[-1], function(nm) {
    val <- coefs[nm]
    sprintf("%s %.3f * %s", ifelse(val >= 0, "+", "-"), abs(val), nm)
  }), collapse = " ")
  equation <- sprintf("%s = %.3f %s", response, coefs[1], terms)
  
  # F-statistic p-value
  f_stat <- fit_sum$fstatistic
  f_p_val <- if (!is.null(f_stat)) {
    pf(f_stat[1], f_stat[2], f_stat[3], lower.tail = FALSE)
  } else NA_real_
  
  diag_df <- data.frame(
    observed_y = sub_df[[response]],
    fitted = fitted(fit),
    residuals = residuals(fit),
    std_residuals = rstandard(fit)
  )
  
  # Limitations note
  notes <- "CRITICAL STATISTICAL NOTE: Total runs are directly constructed from boundaries (4*fours + 6*sixes) and running singles/twos. High R² when including fours and sixes represents mathematical decomposition rather than independent exogenous causal relationships."
  
  list(
    valid = TRUE,
    model = fit,
    formula = formula_obj,
    equation = equation,
    coefficients = coef_df,
    r_squared = fit_sum$r.squared,
    adj_r_squared = fit_sum$adj.r.squared,
    residual_se = fit_sum$sigma,
    f_statistic = if (!is.null(f_stat)) as.numeric(f_stat[1]) else NA_real_,
    f_p_value = f_p_val,
    df = fit_sum$df,
    diagnostics = diag_df,
    notes = notes
  )
}
