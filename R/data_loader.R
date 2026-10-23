# ==============================================================================
# CricketEdge — Data Loader Module
# Generates synthetic demonstration data and loads user-provided CSVs
# ==============================================================================

#' Generate a reproducible, realistic synthetic cricket dataset
#' @param seed Random seed for strict reproducibility (default: 42)
#' @param n_matches Number of matches to simulate (default: 50)
#' @return A data frame containing synthetic cricket batting records
generate_synthetic_cricket_data <- function(seed = 42, n_matches = 50) {
  set.seed(seed)
  
  # Player profiles with realistic statistical parameters
  # mean_runs: expected runs; sd_runs: spread; out_prob: probability of dismissal (1 - not_out_rate);
  # six_rate: sixes per ball; four_rate: fours per ball; strike_rate_target: target SR
  players <- list(
    "V. Kohli" = list(team = "India", pos = 3, mean_runs = 48, sd_runs = 26, out_prob = 0.82, six_rate = 0.04, four_rate = 0.12, target_sr = 138),
    "R. Sharma" = list(team = "India", pos = 1, mean_runs = 38, sd_runs = 29, out_prob = 0.88, six_rate = 0.08, four_rate = 0.13, target_sr = 142),
    "J. Root" = list(team = "England", pos = 3, mean_runs = 44, sd_runs = 24, out_prob = 0.80, six_rate = 0.02, four_rate = 0.11, target_sr = 126),
    "S. Smith" = list(team = "Australia", pos = 3, mean_runs = 42, sd_runs = 25, out_prob = 0.81, six_rate = 0.03, four_rate = 0.11, target_sr = 129),
    "K. Williamson" = list(team = "New Zealand", pos = 3, mean_runs = 41, sd_runs = 23, out_prob = 0.79, six_rate = 0.03, four_rate = 0.10, target_sr = 127),
    "B. Stokes" = list(team = "England", pos = 5, mean_runs = 34, sd_runs = 27, out_prob = 0.90, six_rate = 0.07, four_rate = 0.09, target_sr = 144),
    "G. Maxwell" = list(team = "Australia", pos = 5, mean_runs = 31, sd_runs = 28, out_prob = 0.92, six_rate = 0.11, four_rate = 0.10, target_sr = 158),
    "KL Rahul" = list(team = "India", pos = 2, mean_runs = 39, sd_runs = 26, out_prob = 0.85, six_rate = 0.06, four_rate = 0.12, target_sr = 136)
  )
  
  venues <- c("Melbourne", "Lord's", "Wankhede", "Eden Gardens", "Sydney", "The Oval")
  conditions <- c("Day", "Day/Night", "Overcast", "Dry/Spin", "Pace-friendly")
  opponents_pool <- c("India", "England", "Australia", "New Zealand", "South Africa", "Pakistan")
  
  start_date <- as.Date("2024-01-15")
  records <- list()
  record_id <- 1
  
  for (m in 1:n_matches) {
    match_id <- sprintf("M%03d", 100 + m)
    match_date <- format(start_date + (m * 4), "%Y-%m-%d")
    venue <- sample(venues, 1)
    condition <- sample(conditions, 1)
    
    # Select 4 to 6 players who participated in this match
    active_player_names <- sample(names(players), size = sample(4:6, 1))
    
    # Determine innings total runs for the match
    t1_score <- sample(145:215, 1)
    t2_score <- sample(135:210, 1)
    
    for (p_name in active_player_names) {
      prof <- players[[p_name]]
      team <- prof$team
      
      # Select opponent (not own team)
      avail_opps <- setdiff(opponents_pool, team)
      opponent <- sample(avail_opps, 1)
      
      # Innings: 1 or 2
      innings <- sample(1:2, 1)
      innings_total <- ifelse(innings == 1, t1_score, t2_score)
      wickets_lost <- sample(3:9, 1)
      
      # Batting position with slight variation
      pos <- max(1, min(7, prof$pos + sample(c(-1, 0, 0, 1), 1)))
      
      # Generate runs using realistic skewed distribution (gamma / negative binomial style)
      # Shape and scale derived from mean and sd
      shape_val <- (prof$mean_runs / prof$sd_runs)^2
      scale_val <- (prof$sd_runs^2) / prof$mean_runs
      sim_runs <- round(rgamma(1, shape = shape_val, scale = scale_val))
      sim_runs <- max(0, min(sim_runs, 135)) # cap realistic T20 score
      
      # Estimate balls faced based on player's target strike rate with random variation
      if (sim_runs == 0) {
        balls <- sample(1:4, 1)
        fours <- 0
        sixes <- 0
      } else {
        # Target balls = (runs / target_sr) * 100
        ideal_balls <- (sim_runs / prof$target_sr) * 100
        balls <- max(1, round(rnorm(1, mean = ideal_balls, sd = max(2, ideal_balls * 0.15))))
        
        # Max boundary runs cannot exceed total runs
        max_sixes <- floor(sim_runs / 6)
        sixes <- rbinom(1, size = max_sixes, prob = min(0.65, prof$six_rate * 6))
        
        rem_runs <- sim_runs - (sixes * 6)
        max_fours <- floor(rem_runs / 4)
        fours <- rbinom(1, size = max_fours, prob = min(0.70, prof$four_rate * 4))
        
        # Guarantee balls >= fours + sixes
        balls <- max(balls, fours + sixes + ceiling((sim_runs - fours*4 - sixes*6)/3))
      }
      
      # Dismissal: 1 = out, 0 = not out
      # If batsman scored high and batted 2nd, chance of not out is higher
      out_prob <- prof$out_prob
      if (sim_runs > 50 && innings == 2) out_prob <- out_prob * 0.7
      dismissal <- rbinom(1, 1, prob = out_prob)
      
      records[[record_id]] <- data.frame(
        match_id = match_id,
        date = match_date,
        player = p_name,
        team = team,
        opponent = opponent,
        venue = venue,
        innings = innings,
        batting_position = pos,
        runs = sim_runs,
        balls_faced = balls,
        fours = fours,
        sixes = sixes,
        dismissals = dismissal,
        wickets_lost = wickets_lost,
        innings_total = innings_total,
        overs = 20,
        match_condition = condition,
        stringsAsFactors = FALSE
      )
      record_id <- record_id + 1
    }
  }
  
  df <- do.call(rbind, records)
  df
}

#' Create default sample data and CSV template files on disk
#' @param data_dir Path to the data directory (default: "data")
create_sample_csv_files <- function(data_dir = "data") {
  if (!dir.exists(data_dir)) {
    dir.create(data_dir, recursive = TRUE)
  }
  
  sample_path <- file.path(data_dir, "sample_cricket_data.csv")
  template_path <- file.path(data_dir, "cricket_data_template.csv")
  
  # Generate reproducible dataset
  raw_sample <- generate_synthetic_cricket_data(seed = 42, n_matches = 50)
  write.csv(raw_sample, file = sample_path, row.names = FALSE)
  
  # Generate blank template with column headers and 2 clear example rows
  template_rows <- raw_sample[1:2, ]
  write.csv(template_rows, file = template_path, row.names = FALSE)
  
  list(sample_path = sample_path, template_path = template_path)
}

#' Load sample cricket data, generating and validating if necessary
#' @param data_path Path to sample CSV (default: "data/sample_cricket_data.csv")
#' @return A validated cricket data list object
load_sample_data <- function(data_path = "data/sample_cricket_data.csv") {
  if (!file.exists(data_path)) {
    create_sample_csv_files(dirname(data_path))
  }
  df <- read.csv(data_path, stringsAsFactors = FALSE)
  validate_cricket_data(df)
}

#' Load and validate a user-supplied cricket CSV file
#' @param file_path Path to the uploaded CSV file
#' @return A validated cricket data list object
load_user_csv <- function(file_path) {
  if (missing(file_path) || is.null(file_path) || !file.exists(file_path)) {
    return(list(
      valid = FALSE,
      errors = "File does not exist or path is invalid.",
      warnings = character(),
      missing_report = data.frame(),
      cleaned_data = NULL
    ))
  }
  
  df <- tryCatch({
    read.csv(file_path, stringsAsFactors = FALSE)
  }, error = function(e) {
    NULL
  })
  
  if (is.null(df)) {
    return(list(
      valid = FALSE,
      errors = "Failed to parse CSV file. Ensure it is a valid comma-separated text file.",
      warnings = character(),
      missing_report = data.frame(),
      cleaned_data = NULL
    ))
  }
  
  validate_cricket_data(df)
}
