# ==============================================================================
# CricketEdge — Probability Models & Simulation Module
# Implements Binomial, Poisson, Normal distributions and Cricket Over Simulator
# ==============================================================================

#' Compute Binomial Distribution table and theoretical properties
#' @param n Number of trials (e.g. balls in an over = 6, or overs in a spell = 4)
#' @param p Success probability per trial (0 <= p <= 1)
#' @param k Optional target value of interest
#' @return A list of mathematical metrics and data frame of pmf values
compute_binomial_model <- function(n = 6, p = 0.25, k = 2) {
  n <- as.integer(max(1, n))
  p <- max(0, min(1, as.numeric(p)))
  k <- as.integer(max(0, min(n, k)))
  
  support <- 0:n
  # R standard dbinom and pbinom
  pmf <- dbinom(support, size = n, prob = p)
  cmf <- pbinom(support, size = n, prob = p)
  
  df_dist <- data.frame(
    x = support,
    probability = pmf,
    cumulative = cmf,
    is_target = (support == k)
  )
  
  # Exact theoretical properties
  exp_val <- n * p
  var_val <- n * p * (1 - p)
  sd_val <- sqrt(var_val)
  
  prob_exact <- dbinom(k, size = n, prob = p)
  prob_at_most <- pbinom(k, size = n, prob = p)
  prob_at_least <- 1 - pbinom(k - 1, size = n, prob = p)
  
  list(
    distribution = "Binomial",
    n = n,
    p = p,
    k = k,
    expected_value = exp_val,
    variance = var_val,
    sd = sd_val,
    prob_exact = prob_exact,
    prob_at_most = prob_at_most,
    prob_at_least = prob_at_least,
    data = df_dist
  )
}

#' Compute Poisson Distribution table and theoretical properties
#' @param lambda Rate parameter (lambda > 0)
#' @param k Optional event count of interest
#' @param max_x Maximum support value for plotting
#' @return A list of mathematical metrics and data frame of pmf values
compute_poisson_model <- function(lambda = 2.5, k = 3, max_x = NULL) {
  lambda <- max(0.01, as.numeric(lambda))
  k <- as.integer(max(0, k))
  
  if (is.null(max_x)) {
    max_x <- as.integer(max(15, ceiling(lambda + 4 * sqrt(lambda))))
  }
  
  support <- 0:max_x
  # R standard dpois and ppois
  pmf <- dpois(support, lambda = lambda)
  cmf <- ppois(support, lambda = lambda)
  
  df_dist <- data.frame(
    x = support,
    probability = pmf,
    cumulative = cmf,
    is_target = (support == k)
  )
  
  exp_val <- lambda
  var_val <- lambda
  sd_val <- sqrt(lambda)
  
  prob_exact <- dpois(k, lambda = lambda)
  prob_at_most <- ppois(k, lambda = lambda)
  prob_exceeds <- ppois(k, lambda = lambda, lower.tail = FALSE)
  
  list(
    distribution = "Poisson",
    lambda = lambda,
    k = k,
    expected_value = exp_val,
    variance = var_val,
    sd = sd_val,
    prob_exact = prob_exact,
    prob_at_most = prob_at_most,
    prob_exceeds = prob_exceeds,
    data = df_dist
  )
}

#' Compute Normal Distribution density and interval probabilities
#' @param mu Mean parameter
#' @param sigma Standard deviation parameter (sigma > 0)
#' @param lower_val Lower bound for probability region
#' @param upper_val Upper bound for probability region
#' @param region_type "between", "below", or "above"
#' @return A list of continuous density data and calculated probabilities
compute_normal_model <- function(mu = 160, sigma = 25, lower_val = 140, upper_val = 180, region_type = "between") {
  mu <- as.numeric(mu)
  sigma <- max(0.001, as.numeric(sigma))
  lower_val <- as.numeric(lower_val)
  upper_val <- as.numeric(upper_val)
  
  # Ensure lower <= upper
  if (lower_val > upper_val) {
    tmp <- lower_val
    lower_val <- upper_val
    upper_val <- tmp
  }
  
  # Support bounds for visualization: mu +/- 3.8 * sigma
  x_seq <- seq(mu - 3.8 * sigma, mu + 3.8 * sigma, length.out = 300)
  density_vals <- dnorm(x_seq, mean = mu, sd = sigma)
  
  # Calculate exact theoretical probabilities using pnorm()
  prob_val <- switch(
    region_type,
    "below" = pnorm(upper_val, mean = mu, sd = sigma),
    "above" = pnorm(lower_val, mean = mu, sd = sigma, lower.tail = FALSE),
    "between" = pnorm(upper_val, mean = mu, sd = sigma) - pnorm(lower_val, mean = mu, sd = sigma)
  )
  
  # Shaded interval subset
  shade_mask <- switch(
    region_type,
    "below" = (x_seq <= upper_val),
    "above" = (x_seq >= lower_val),
    "between" = (x_seq >= lower_val & x_seq <= upper_val)
  )
  
  df_curve <- data.frame(x = x_seq, density = density_vals)
  df_shade <- data.frame(x = x_seq[shade_mask], density = density_vals[shade_mask])
  
  list(
    distribution = "Normal",
    mu = mu,
    sigma = sigma,
    lower_val = lower_val,
    upper_val = upper_val,
    region_type = region_type,
    probability = prob_val,
    expected_value = mu,
    variance = sigma^2,
    sd = sigma,
    curve_data = df_curve,
    shade_data = df_shade
  )
}

#' Simulate Cricket Over Scoring using a transparent discrete categorical ball model
#' @param n_overs Number of overs to simulate (e.g. 500)
#' @param probs Named or ordered vector of probabilities for outcomes c(0, 1, 2, 3, 4, 6)
#' @param target_over_runs Target runs in an over to evaluate reach probability
#' @param seed Optional random seed for reproducibility
#' @return A list of simulation outputs, empirical frequencies, and theoretical comparisons
simulate_cricket_overs <- function(n_overs = 500, probs = c(0.35, 0.35, 0.10, 0.02, 0.12, 0.06),
                                   target_over_runs = 10, seed = 42) {
  if (!is.null(seed)) set.seed(seed)
  n_overs <- as.integer(max(10, min(10000, n_overs)))
  
  outcomes <- c(0, 1, 2, 3, 4, 6)
  
  # Normalize probabilities to strictly sum to 1
  probs <- as.numeric(probs)
  if (length(probs) != 6 || any(probs < 0) || sum(probs) == 0) {
    probs <- c(0.35, 0.35, 0.10, 0.02, 0.12, 0.06)
  }
  probs <- probs / sum(probs)
  
  # Theoretical single ball metrics
  theor_ball_mean <- sum(outcomes * probs)
  theor_ball_var <- sum((outcomes - theor_ball_mean)^2 * probs)
  
  # Theoretical 6-ball over metrics (by linearity of expectation for independent balls)
  theor_over_mean <- 6 * theor_ball_mean
  theor_over_var <- 6 * theor_ball_var
  theor_over_sd <- sqrt(theor_over_var)
  
  # Simulate 6 * n_overs balls
  total_balls <- 6 * n_overs
  sim_balls <- sample(outcomes, size = total_balls, replace = TRUE, prob = probs)
  
  # Reshape into matrix: 6 rows (balls), n_overs columns
  ball_matrix <- matrix(sim_balls, nrow = 6, ncol = n_overs)
  over_totals <- colSums(ball_matrix)
  
  # Empirical simulation statistics
  emp_mean <- mean(over_totals)
  emp_median <- median(over_totals)
  emp_sd <- sd(over_totals)
  emp_iqr <- IQR(over_totals)
  
  # Reach target probability
  prob_reach_target <- mean(over_totals >= target_over_runs)
  
  # Frequency distribution data frame
  tbl <- table(factor(over_totals, levels = 0:36))
  df_sim <- data.frame(
    OverScore = 0:36,
    Count = as.integer(tbl),
    EmpiricalProb = as.numeric(tbl) / n_overs
  )
  # Filter only scores up to maximum observed + 2 for clean plotting
  max_obs <- max(over_totals, target_over_runs)
  df_sim_plot <- df_sim[df_sim$OverScore <= min(36, max_obs + 2), ]
  
  assumptions_text <- paste(
    "SIMULATION ASSUMPTIONS & METHODOLOGY:",
    "1. Each ball outcome is drawn independently from discrete support {0, 1, 2, 3, 4, 6} runs.",
    "2. Probabilities are strictly non-negative and normalized to sum to 1.00.",
    "3. Extras (wides, no-balls, leg-byes) and early over termination due to all-out are excluded for statistical tractability.",
    "4. By the Central Limit Theorem, the distribution of 6-ball sum approaches a bell-shaped profile as trials increase, but remains bounded within [0, 36].",
    sep = "\n"
  )
  
  list(
    n_overs = n_overs,
    outcomes = outcomes,
    probs = probs,
    target_over_runs = target_over_runs,
    theor_over_mean = theor_over_mean,
    theor_over_sd = theor_over_sd,
    theor_over_var = theor_over_var,
    empirical_mean = emp_mean,
    empirical_median = emp_median,
    empirical_sd = emp_sd,
    empirical_iqr = emp_iqr,
    prob_reach_target = prob_reach_target,
    over_totals = over_totals,
    plot_data = df_sim_plot,
    assumptions = assumptions_text
  )
}
