# ==============================================================================
# CricketEdge — Test Suite: Probability Models & Mathematical Properties
# ==============================================================================

suppressPackageStartupMessages({
  library(testthat)
})

source("../R/probability_models.R")

test_that("Binomial probabilities sum to 1 over complete support", {
  n_vals <- c(6, 10, 20)
  p_vals <- c(0.1, 0.25, 0.5, 0.8)
  
  for (n in n_vals) {
    for (p in p_vals) {
      model <- compute_binomial_model(n = n, p = p, k = 1)
      prob_sum <- sum(model$data$probability)
      expect_equal(prob_sum, 1.0, tolerance = 1e-7)
    }
  }
})

test_that("Binomial expected value and variance match theoretical formulas", {
  n <- 6
  p <- 0.3
  model <- compute_binomial_model(n = n, p = p, k = 2)
  
  expected_theor <- n * p
  var_theor <- n * p * (1 - p)
  
  expect_equal(model$expected_value, expected_theor)
  expect_equal(model$variance, var_theor)
  
  # Check against dbinom calculations directly
  x_vals <- model$data$x
  pmf_vals <- model$data$probability
  computed_mean <- sum(x_vals * pmf_vals)
  computed_var <- sum((x_vals - computed_mean)^2 * pmf_vals)
  
  expect_equal(computed_mean, expected_theor, tolerance = 1e-7)
  expect_equal(computed_var, var_theor, tolerance = 1e-7)
})

test_that("Poisson probabilities sum to ~1 over sufficiently large support", {
  lambdas <- c(1.5, 3.0, 7.5)
  for (lam in lambdas) {
    model <- compute_poisson_model(lambda = lam, k = 2)
    prob_sum <- sum(model$data$probability)
    expect_gt(prob_sum, 0.999)
    expect_lte(prob_sum, 1.0001)
  }
})

test_that("Poisson distribution mean and variance equal lambda", {
  lam <- 3.5
  model <- compute_poisson_model(lambda = lam, k = 3)
  expect_equal(model$expected_value, lam)
  expect_equal(model$variance, lam)
  expect_equal(model$sd, sqrt(lam))
})

test_that("Normal distribution probabilities match pnorm() exactly", {
  mu <- 150
  sigma <- 20
  
  # Between 130 and 170
  norm_res <- compute_normal_model(mu = mu, sigma = sigma, lower_val = 130, upper_val = 170, region_type = "between")
  expected_p <- pnorm(170, mean = mu, sd = sigma) - pnorm(130, mean = mu, sd = sigma)
  expect_equal(norm_res$probability, expected_p, tolerance = 1e-7)
  
  # Check standard 1-sigma rule ~ 68.27%
  norm_1sigma <- compute_normal_model(mu = 0, sigma = 1, lower_val = -1, upper_val = 1, region_type = "between")
  expect_equal(norm_1sigma$probability, 0.6826895, tolerance = 1e-5)
})

test_that("Cricket over simulation respects probability bounds and CLT convergence", {
  sim <- simulate_cricket_overs(n_overs = 2000, seed = 42)
  expect_equal(length(sim$over_totals), 2000)
  expect_true(all(sim$over_totals >= 0 & sim$over_totals <= 36))
  
  # Empirical mean should be close to theoretical expectation within standard error
  se_mean <- sim$theor_over_sd / sqrt(2000)
  expect_lt(abs(sim$empirical_mean - sim$theor_over_mean), 3 * se_mean)
})
