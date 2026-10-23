# ==============================================================================
# CricketEdge — Test Suite: Data Validation & Schema Checks
# ==============================================================================

suppressPackageStartupMessages({
  library(testthat)
})

source("../R/data_validation.R")
source("../R/data_loader.R")

test_that("Synthetic data generation is strictly reproducible with set seed", {
  df1 <- generate_synthetic_cricket_data(seed = 42, n_matches = 10)
  df2 <- generate_synthetic_cricket_data(seed = 42, n_matches = 10)
  expect_identical(df1, df2)
  expect_true(nrow(df1) > 0)
})

test_that("Validation detects missing required columns", {
  incomplete_df <- data.frame(
    match_id = "M101",
    player = "V. Kohli",
    runs = 50
  )
  val_res <- validate_cricket_data(incomplete_df)
  expect_false(val_res$valid)
  expect_true(any(grepl("Missing required columns", val_res$errors)))
})

test_that("Validation handles negative values and invalid bounds", {
  bad_df <- generate_synthetic_cricket_data(seed = 123, n_matches = 2)
  bad_df$runs[1] <- -10
  val_res <- validate_cricket_data(bad_df)
  expect_false(val_res$valid)
  expect_true(any(grepl("Runs cannot be negative", val_res$errors)))
})

test_that("Strike rate calculation safely handles zero balls faced", {
  df_zero_balls <- generate_synthetic_cricket_data(seed = 42, n_matches = 2)
  df_zero_balls$balls_faced[1] <- 0
  df_zero_balls$runs[1] <- 0
  df_zero_balls$fours[1] <- 0
  df_zero_balls$sixes[1] <- 0
  
  val_res <- validate_cricket_data(df_zero_balls)
  expect_true(val_res$valid)
  expect_equal(val_res$cleaned_data$strike_rate[1], 0)
  expect_false(is.nan(val_res$cleaned_data$strike_rate[1]))
  expect_false(is.infinite(val_res$cleaned_data$strike_rate[1]))
})

test_that("Boundary consistency condition is audited and fixed", {
  inconsistent_df <- generate_synthetic_cricket_data(seed = 42, n_matches = 2)
  # 4 * 10 + 6 * 5 = 70 boundary runs, but total runs is set to 20
  inconsistent_df$fours[1] <- 10
  inconsistent_df$sixes[1] <- 5
  inconsistent_df$runs[1] <- 20
  
  val_res <- validate_cricket_data(inconsistent_df)
  expect_true(val_res$valid)
  expect_true(val_res$cleaned_data$runs[1] >= 70)
  expect_true(any(grepl("boundary runs", val_res$warnings)))
})
