# ==============================================================================
# CricketEdge — Data Validation Module
# Validates schema, constraints, data types, and missing values for cricket data
# ==============================================================================

REQUIRED_COLUMNS <- c(
  "match_id", "date", "player", "team", "opponent", "venue",
  "innings", "batting_position", "runs", "balls_faced",
  "fours", "sixes", "dismissals", "wickets_lost",
  "innings_total", "overs", "match_condition"
)

COLUMN_DESCRIPTIONS <- c(
  match_id = "Unique match identifier (e.g. M101)",
  date = "Date of match (YYYY-MM-DD)",
  player = "Player name (e.g. V. Kohli)",
  team = "Player's team name",
  opponent = "Opponent team name",
  venue = "Match venue/stadium name",
  innings = "Innings number (1 = batting first, 2 = chasing)",
  batting_position = "Batting order position (1 to 11)",
  runs = "Individual runs scored by the batsman (>= 0)",
  balls_faced = "Number of deliveries faced (>= 0)",
  fours = "Number of 4s hit (>= 0)",
  sixes = "Number of 6s hit (>= 0)",
  dismissals = "Dismissal indicator (1 = Out, 0 = Not Out)",
  wickets_lost = "Total team wickets lost in the innings (0 to 10)",
  innings_total = "Team's cumulative innings total runs",
  overs = "Total scheduled overs for the match (e.g. 20 or 50)",
  match_condition = "Pitch and playing condition (e.g. Day, Day/Night, Overcast, Dry/Spin, Pace-friendly)"
)

#' Validate a cricket data frame against schema and logical domain constraints
#' @param df A data frame to validate
#' @return A list with valid (logical), errors (character vector), warnings (character vector),
#'         missing_report (data frame), and cleaned_data (data frame)
validate_cricket_data <- function(df) {
  errors <- character()
  warnings <- character()
  
  if (is.null(df) || !is.data.frame(df) || nrow(df) == 0) {
    return(list(
      valid = FALSE,
      errors = "Dataset is empty, NULL, or not a valid data frame.",
      warnings = character(),
      missing_report = data.frame(),
      cleaned_data = NULL
    ))
  }
  
  # 1. Schema check
  missing_cols <- setdiff(REQUIRED_COLUMNS, names(df))
  if (length(missing_cols) > 0) {
    errors <- c(errors, paste0("Missing required columns: ", paste(missing_cols, collapse = ", ")))
    return(list(
      valid = FALSE,
      errors = errors,
      warnings = warnings,
      missing_report = data.frame(Column = names(df), MissingCount = sapply(df, function(x) sum(is.na(x)))),
      cleaned_data = NULL
    ))
  }
  
  # 2. Missing Value Report
  missing_counts <- sapply(df[REQUIRED_COLUMNS], function(x) sum(is.na(x)))
  missing_pct <- round((missing_counts / nrow(df)) * 100, 2)
  missing_report <- data.frame(
    Column = REQUIRED_COLUMNS,
    MissingCount = as.integer(missing_counts),
    MissingPct = missing_pct,
    stringsAsFactors = FALSE
  )
  
  # Work on a copy
  clean_df <- df
  
  # Coerce numeric columns safely
  numeric_cols <- c("runs", "balls_faced", "fours", "sixes", "dismissals", 
                    "batting_position", "innings", "wickets_lost", "innings_total", "overs")
  
  for (col in numeric_cols) {
    if (!is.numeric(clean_df[[col]])) {
      num_vals <- suppressWarnings(as.numeric(clean_df[[col]]))
      if (all(is.na(num_vals) & !is.na(clean_df[[col]]))) {
        errors <- c(errors, sprintf("Column '%s' cannot be converted to numeric values.", col))
      } else {
        clean_df[[col]] <- num_vals
        warnings <- c(warnings, sprintf("Column '%s' was coerced to numeric.", col))
      }
    }
  }
  
  if (length(errors) > 0) {
    return(list(
      valid = FALSE,
      errors = errors,
      warnings = warnings,
      missing_report = missing_report,
      cleaned_data = NULL
    ))
  }
  
  # Character columns
  char_cols <- c("match_id", "player", "team", "opponent", "venue", "match_condition")
  for (col in char_cols) {
    clean_df[[col]] <- as.character(clean_df[[col]])
    if (any(is.na(clean_df[[col]]) | trimws(clean_df[[col]]) == "")) {
      warnings <- c(warnings, sprintf("Column '%s' contains empty or NA strings.", col))
    }
  }
  
  # Logical Domain Checks
  # A. Negative values check
  if (any(clean_df$runs < 0, na.rm = TRUE)) {
    errors <- c(errors, "Runs cannot be negative.")
  }
  if (any(clean_df$balls_faced < 0, na.rm = TRUE)) {
    errors <- c(errors, "Balls faced cannot be negative.")
  }
  if (any(clean_df$fours < 0, na.rm = TRUE) || any(clean_df$sixes < 0, na.rm = TRUE)) {
    errors <- c(errors, "Boundary counts (fours and sixes) cannot be negative.")
  }
  
  # B. Boundary consistency: 4*fours + 6*sixes <= runs
  boundary_runs <- (clean_df$fours * 4) + (clean_df$sixes * 6)
  inconsistent_boundaries <- which(boundary_runs > clean_df$runs)
  if (length(inconsistent_boundaries) > 0) {
    warnings <- c(warnings, sprintf(
      "Found %d rows where boundary runs (4*fours + 6*sixes) exceed total runs. Adjusted runs to match boundary lower-bound.",
      length(inconsistent_boundaries)
    ))
    # Fix boundary inconsistency safely by ensuring runs is at least boundary_runs
    clean_df$runs[inconsistent_boundaries] <- boundary_runs[inconsistent_boundaries]
  }
  
  # C. Dismissal check: must be 0 or 1
  invalid_dismissals <- which(!clean_df$dismissals %in% c(0, 1))
  if (length(invalid_dismissals) > 0) {
    warnings <- c(warnings, sprintf("Found %d rows with dismissals not equal to 0 or 1; defaulted to 1 (out).", length(invalid_dismissals)))
    clean_df$dismissals[invalid_dismissals] <- 1
  }
  
  # D. Balls faced vs runs: if runs > 0 and balls_faced == 0, fix safely
  zero_balls_positive_runs <- which(clean_df$runs > 0 & clean_df$balls_faced == 0)
  if (length(zero_balls_positive_runs) > 0) {
    warnings <- c(warnings, sprintf("Found %d rows with runs > 0 but balls_faced == 0; set balls_faced to estimated minimum.", length(zero_balls_positive_runs)))
    clean_df$balls_faced[zero_balls_positive_runs] <- pmax(1, clean_df$fours[zero_balls_positive_runs] + clean_df$sixes[zero_balls_positive_runs])
  }
  
  # Derived columns computed mathematically
  clean_df$strike_rate <- ifelse(
    clean_df$balls_faced > 0,
    round((clean_df$runs / clean_df$balls_faced) * 100, 2),
    0.0
  )
  clean_df$boundary_runs <- (clean_df$fours * 4) + (clean_df$sixes * 6)
  clean_df$boundary_pct <- ifelse(
    clean_df$runs > 0,
    round((clean_df$boundary_runs / clean_df$runs) * 100, 2),
    0.0
  )
  clean_df$is_not_out <- (clean_df$dismissals == 0)
  
  # Score milestone classification for categorical analysis
  clean_df$score_category <- cut(
    clean_df$runs,
    breaks = c(-Inf, 19, 49, 99, Inf),
    labels = c("Single Digit/Low (<20)", "Middle Score (20-49)", "Fifty (50-99)", "Century (100+)"),
    right = TRUE
  )
  
  list(
    valid = (length(errors) == 0),
    errors = errors,
    warnings = warnings,
    missing_report = missing_report,
    cleaned_data = clean_df
  )
}
