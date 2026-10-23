# ==============================================================================
# CricketEdge — Test Suite: Statistical Calculations, Inference, & Graph Fidelity
# ==============================================================================

suppressPackageStartupMessages({
  library(testthat)
  library(ggplot2)
})

source("../R/data_validation.R")
source("../R/data_loader.R")
source("../R/descriptive_stats.R")
source("../R/regression_analysis.R")
source("../R/probability_models.R")
source("../R/hypothesis_tests.R")
source("../R/chi_square_analysis.R")
source("../R/anova_analysis.R")
source("../R/plots.R")

# Setup validated sample dataset
raw_df <- generate_synthetic_cricket_data(seed = 42, n_matches = 40)
val_res <- validate_cricket_data(raw_df)
df <- val_res$cleaned_data

test_that("Descriptive metrics agree with direct base R calculations", {
  metrics <- compute_overall_metrics(df)
  expect_equal(metrics$total_innings, nrow(df))
  expect_equal(metrics$total_runs, sum(df$runs))
  expect_equal(metrics$mean_runs, round(mean(df$runs), 2))
  expect_equal(metrics$median_runs, round(median(df$runs), 2))
  
  expected_sr <- round((sum(df$runs) / sum(df$balls_faced)) * 100, 2)
  expect_equal(metrics$overall_strike_rate, expected_sr)
})

test_that("Simple regression coefficients and R-squared match lm() directly", {
  reg <- fit_simple_regression(df, response = "runs", predictor = "balls_faced")
  expect_true(reg$valid)
  
  base_lm <- lm(runs ~ balls_faced, data = df)
  base_sum <- summary(base_lm)
  
  expect_equal(unname(coef(reg$model)), unname(coef(base_lm)))
  expect_equal(reg$r_squared, base_sum$r.squared)
  expect_equal(reg$adj_r_squared, base_sum$adj.r.squared)
  expect_equal(reg$residual_se, base_sum$sigma)
})

test_that("Multiple regression coefficients and diagnostics match lm() directly", {
  mult_reg <- fit_multiple_regression(df, response = "runs", predictors = c("balls_faced", "fours", "sixes"))
  expect_true(mult_reg$valid)
  
  base_mult <- lm(runs ~ balls_faced + fours + sixes, data = df)
  base_mult_sum <- summary(base_mult)
  
  expect_equal(unname(coef(mult_reg$model)), unname(coef(base_mult)))
  expect_equal(mult_reg$r_squared, base_mult_sum$r.squared)
})

test_that("One-way ANOVA F-statistic and p-value match aov() directly", {
  aov_res <- run_cricket_anova(df, group_col = "player", val_col = "runs", alpha = 0.05)
  expect_true(aov_res$valid)
  
  base_aov <- aov(runs ~ player, data = df)
  base_summary <- summary(base_aov)[[1]]
  
  expect_equal(aov_res$f_stat, base_summary[["F value"]][1])
  expect_equal(aov_res$p_val, base_summary[["Pr(>F)"]][1])
  expect_equal(aov_res$anova_table$Df[1], base_summary[["Df"]][1])
  expect_equal(aov_res$anova_table$Df[2], base_summary[["Df"]][2])
})

test_that("Hypothesis testing decision logic agrees with p-value and alpha", {
  # Significant test case
  kohli_runs <- df$runs[df$player == "V. Kohli"]
  t_res_sig <- run_one_sample_t_test(kohli_runs, mu0 = 10, alternative = "greater", conf_level = 0.95)
  expect_true(t_res_sig$valid)
  expect_true(t_res_sig$p_value < 0.05)
  expect_true(grepl("Reject H₀", t_res_sig$decision))
  
  # Non-significant test case (test against true sample mean)
  t_res_nonsig <- run_one_sample_t_test(kohli_runs, mu0 = mean(kohli_runs), alternative = "two.sided", conf_level = 0.95)
  expect_true(t_res_nonsig$valid)
  expect_gte(t_res_nonsig$p_value, 0.05)
  expect_true(grepl("Fail to Reject H₀", t_res_nonsig$decision))
})

test_that("Chi-Square Goodness-of-Fit matches chisq.test() directly", {
  obs <- c(30, 45, 25)
  names(obs) <- c("Day", "Day/Night", "Overcast")
  cs_res <- run_chi_square_gof(obs, expected_probs = c(1/3, 1/3, 1/3), alpha = 0.05)
  
  expect_true(cs_res$valid)
  base_cs <- chisq.test(obs, p = c(1/3, 1/3, 1/3))
  expect_equal(cs_res$statistic, round(as.numeric(base_cs$statistic), 4))
  expect_equal(cs_res$p_value, base_cs$p.value)
})

test_that("Plotted probability data strictly match underlying R functions (Graph Fidelity)", {
  # Binomial graph fidelity
  b_mod <- compute_binomial_model(n = 6, p = 0.3, k = 2)
  p_binom <- plot_binomial_distribution(b_mod)
  expect_equal(p_binom$data$probability, dbinom(0:6, size = 6, prob = 0.3))
  
  # Poisson graph fidelity
  p_mod <- compute_poisson_model(lambda = 3.2, k = 3)
  p_pois <- plot_poisson_distribution(p_mod)
  support_p <- p_mod$data$x
  expect_equal(p_pois$data$probability, dpois(support_p, lambda = 3.2))
  
  # Normal graph fidelity
  n_mod <- compute_normal_model(mu = 150, sigma = 20, lower_val = 130, upper_val = 170, region_type = "between")
  p_norm <- plot_normal_distribution(n_mod)
  expect_equal(p_norm$data$density, dnorm(p_norm$data$x, mean = 150, sd = 20))
})

test_that("Filtering data updates both numerical summaries and graph inputs", {
  # Full dataset metrics
  full_metrics <- compute_overall_metrics(df)
  
  # Filter by a single player
  filtered_sub <- df[df$player == "V. Kohli", ]
  sub_metrics <- compute_overall_metrics(filtered_sub)
  
  expect_lt(sub_metrics$total_innings, full_metrics$total_innings)
  expect_equal(sub_metrics$total_innings, nrow(filtered_sub))
  expect_equal(sub_metrics$total_runs, sum(filtered_sub$runs))
  
  # Visualizations generated from filtered data reflect subset sample size
  p_sub <- plot_runs_by_player(filtered_sub)
  expect_equal(nrow(p_sub$data), 1)
  expect_equal(as.character(p_sub$data$player[1]), "V. Kohli")
})

test_that("Visualizations build without throwing errors", {
  p1 <- plot_runs_by_player(df)
  expect_s3_class(p1, "ggplot")
  
  p2 <- plot_runs_distribution(df)
  expect_s3_class(p2, "ggplot")
  
  reg <- fit_simple_regression(df, response = "runs", predictor = "balls_faced")
  p3 <- plot_simple_regression(reg)
  expect_s3_class(p3, "ggplot")
  
  aov_res <- run_cricket_anova(df, group_col = "player", val_col = "runs")
  p4 <- plot_anova_groups(aov_res, df)
  expect_s3_class(p4, "ggplot")
})
