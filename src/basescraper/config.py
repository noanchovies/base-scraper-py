# src/basescraper/config.py

# --- Default Base Configuration ---
# These values serve as defaults if not overridden by .env or CLI arguments
# when *using* the base scraper template for a specific project.

DEFAULT_TARGET_URL = "https://www.google.com/" # A generic default
DEFAULT_OUTPUT_FILENAME = "scraped_data.csv"   # Default filename if saving to CSV
DEFAULT_WAIT_TIME = 3                          # Default wait time in seconds
DEFAULT_HEADLESS_MODE = True                   # Default to headless