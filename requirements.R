# CricketEdge - Dependency Installer and Verifier
# Run this script in R / RStudio to ensure all required packages are installed.

required_packages <- c(
  "shiny",
  "ggplot2",
  "bslib",
  "dplyr",
  "readr"
)

cat("==================================================\n")
cat("CricketEdge Dependency Checker\n")
cat("==================================================\n")

# Detect missing packages
installed_pkgs <- rownames(installed.packages())
missing_pkgs <- required_packages[!required_packages %in% installed_pkgs]

if (length(missing_pkgs) > 0) {
  cat("Installing missing packages:", paste(missing_pkgs, collapse = ", "), "\n")
  install.packages(missing_pkgs, repos = "https://cloud.r-project.org")
} else {
  cat("All required packages are already installed!\n")
}

# Verify loading
cat("\nVerifying package loading:\n")
all_loaded <- TRUE
for (pkg in required_packages) {
  loaded <- suppressPackageStartupMessages(require(pkg, character.only = TRUE, quietly = TRUE))
  cat(sprintf("  [%s] %s\n", ifelse(loaded, "OK", "FAIL"), pkg))
  if (!loaded) all_loaded <- FALSE
}

if (all_loaded) {
  cat("\nSUCCESS: All dependencies are installed and operational.\n")
  cat("You can launch CricketEdge by opening RStudio and running:\n")
  cat("  shiny::runApp()\n")
} else {
  cat("\nWARNING: Some dependencies failed to load. Please inspect CRAN repository settings.\n")
}
