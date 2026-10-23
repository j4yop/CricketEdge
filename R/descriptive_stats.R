# ==============================================================================
# CricketEdge — Descriptive Statistics Module
# Implements measures of central tendency, dispersion, tabulation, and consistency
# ==============================================================================

#' Compute high-level KPI and descriptive statistics for a filtered dataset
#' @param df A cleaned cricket data frame
#' @return A named list of overall metrics
compute_overall_metrics <- function(df) {
  if (is.null(df) || nrow(df) == 0) {
    return(list(
      total_innings = 0,
      total_players = 0,
      total_runs = 0,
      total_balls = 0,
      mean_runs = 0,
      median_runs = 0,
      sd_runs = 0,
      iqr_runs = 0,
      overall_strike_rate = 0,
      total_fours = 0,
      total_sixes = 0,
      boundary_runs = 0,
      boundary_runs_pct = 0,
      total_dismissals = 0,
      batting_average = 0
    ))
  }
  
  tot_runs <- sum(df$runs, na.rm = TRUE)
  tot_balls <- sum(df$balls_faced, na.rm = TRUE)
  tot_fours <- sum(df$fours, na.rm = TRUE)
  tot_sixes <- sum(df$sixes, na.rm = TRUE)
  tot_dismissals <- sum(df$dismissals, na.rm = TRUE)
  b_runs <- (tot_fours * 4) + (tot_sixes * 6)
  
  overall_sr <- if (tot_balls > 0) round((tot_runs / tot_balls) * 100, 2) else 0.0
  b_pct <- if (tot_runs > 0) round((b_runs / tot_runs) * 100, 2) else 0.0
  b_avg <- if (tot_dismissals > 0) round(tot_runs / tot_dismissals, 2) else Inf
  
  list(
    total_innings = nrow(df),
    total_players = length(unique(df$player)),
    total_runs = tot_runs,
    total_balls = tot_balls,
    mean_runs = round(mean(df$runs, na.rm = TRUE), 2),
    median_runs = round(median(df$runs, na.rm = TRUE), 2),
    sd_runs = round(sd(df$runs, na.rm = TRUE), 2),
    iqr_runs = round(IQR(df$runs, na.rm = TRUE), 2),
    overall_strike_rate = overall_sr,
    total_fours = tot_fours,
    total_sixes = tot_sixes,
    boundary_runs = b_runs,
    boundary_runs_pct = b_pct,
    total_dismissals = tot_dismissals,
    batting_average = b_avg
  )
}

#' Compute individual player summary metrics
#' @param df Cleaned cricket data frame
#' @param selected_players Character vector of player names to filter by (optional)
#' @return A data frame of player-level descriptive metrics
compute_player_metrics <- function(df, selected_players = NULL) {
  if (is.null(df) || nrow(df) == 0) {
    return(data.frame())
  }
  
  if (!is.null(selected_players) && length(selected_players) > 0) {
    df <- df[df$player %in% selected_players, , drop = FALSE]
  }
  
  if (nrow(df) == 0) return(data.frame())
  
  # Group by player using base R split-apply for universal reliability
  players_list <- split(df, df$player)
  
  res_list <- lapply(names(players_list), function(pname) {
    sub_df <- players_list[[pname]]
    n_inn <- nrow(sub_df)
    tot_r <- sum(sub_df$runs, na.rm = TRUE)
    tot_b <- sum(sub_df$balls_faced, na.rm = TRUE)
    tot_4s <- sum(sub_df$fours, na.rm = TRUE)
    tot_6s <- sum(sub_df$sixes, na.rm = TRUE)
    tot_outs <- sum(sub_df$dismissals, na.rm = TRUE)
    not_outs <- n_inn - tot_outs
    
    mean_r <- mean(sub_df$runs, na.rm = TRUE)
    median_r <- median(sub_df$runs, na.rm = TRUE)
    sd_r <- if (n_inn > 1) sd(sub_df$runs, na.rm = TRUE) else 0.0
    iqr_r <- IQR(sub_df$runs, na.rm = TRUE)
    
    bat_avg <- if (tot_outs > 0) tot_r / tot_outs else Inf
    sr <- if (tot_b > 0) (tot_r / tot_b) * 100 else 0.0
    
    b_runs <- (tot_4s * 4) + (tot_6s * 6)
    b_pct <- if (tot_r > 0) (b_runs / tot_r) * 100 else 0.0
    
    # Consistency Metric: Coefficient of Variation (CV = SD / Mean * 100)
    # Lower CV indicates greater scoring consistency (less relative dispersion)
    cv <- if (mean_r > 0) round((sd_r / mean_r) * 100, 1) else NA_real_
    
    # 50s and 100s counts
    fifties <- sum(sub_df$runs >= 50 & sub_df$runs < 100, na.rm = TRUE)
    hundreds <- sum(sub_df$runs >= 100, na.rm = TRUE)
    
    data.frame(
      Player = pname,
      Team = sub_df$team[1],
      Innings = n_inn,
      TotalRuns = tot_r,
      BallsFaced = tot_b,
      MeanRuns = round(mean_r, 2),
      MedianRuns = round(median_r, 2),
      SD = round(sd_r, 2),
      IQR = round(iqr_r, 2),
      Dismissals = tot_outs,
      NotOuts = not_outs,
      BattingAverage = ifelse(is.infinite(bat_avg), "Undef (0 Outs)", as.character(round(bat_avg, 2))),
      BattingAverageNum = bat_avg,
      StrikeRate = round(sr, 2),
      Fours = tot_4s,
      Sixes = tot_6s,
      BoundaryRuns = b_runs,
      BoundaryPct = round(b_pct, 1),
      Fifties = fifties,
      Hundreds = hundreds,
      CV_Pct = cv, # Lower is more consistent
      stringsAsFactors = FALSE
    )
  })
  
  out <- do.call(rbind, res_list)
  # Order by TotalRuns descending
  out[order(-out$TotalRuns), ]
}

#' Generate grouped summary cross-tabulation for any categorical factor
#' @param df Cleaned cricket data frame
#' @param group_col Column name to group by
#' @return A aggregated summary table
compute_group_tabulation <- function(df, group_col = "match_condition") {
  if (is.null(df) || nrow(df) == 0 || !group_col %in% names(df)) {
    return(data.frame())
  }
  
  splits <- split(df, df[[group_col]])
  rows <- lapply(names(splits), function(grp) {
    sub <- splits[[grp]]
    tot_r <- sum(sub$runs, na.rm = TRUE)
    tot_b <- sum(sub$balls_faced, na.rm = TRUE)
    sr <- if (tot_b > 0) round((tot_r / tot_b) * 100, 2) else 0.0
    
    data.frame(
      Category = grp,
      Innings = nrow(sub),
      TotalRuns = tot_r,
      MeanRuns = round(mean(sub$runs, na.rm = TRUE), 2),
      MedianRuns = round(median(sub$runs, na.rm = TRUE), 2),
      SD = round(sd(sub$runs, na.rm = TRUE), 2),
      IQR = round(IQR(sub$runs, na.rm = TRUE), 2),
      OverallStrikeRate = sr,
      stringsAsFactors = FALSE
    )
  })
  
  do.call(rbind, rows)
}
