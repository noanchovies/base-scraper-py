# src/basescraper/scraper.py

import logging
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
# Pandas is no longer strictly needed in the BASE, but keep import if common usage expected
# import pandas as pd
from dotenv import load_dotenv

# Import configurations from config.py
from . import config # Use relative import within the package

# --- Basic Logging Setup ---
log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
log_level = getattr(logging, log_level_str, logging.INFO)
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Environment Variables ---
load_dotenv()

# --- Selenium WebDriver Setup (Core Reusable Function) ---

def setup_driver(headless=config.DEFAULT_HEADLESS_MODE):
    """Initializes and returns a Selenium WebDriver instance (Chrome)."""
    logging.info("Setting up Selenium WebDriver...")
    run_headless = os.getenv("HEADLESS", str(headless)).lower() in ('true', '1', 't')

    chrome_options = ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

    if run_headless:
        logging.info("Running WebDriver in headless mode.")
        chrome_options.add_argument("--headless")
    else:
        logging.info("Running WebDriver with browser window visible.")

    try:
        os.environ['WDM_LOG'] = str(logging.WARNING)
        os.environ['WDM_SSL_VERIFY'] = '0'
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logging.info("WebDriver setup complete.")
        return driver
    except Exception as e:
        logging.error(f"Error setting up WebDriver: {e}", exc_info=True)
        raise

# --- Navigation Function (Core Reusable Function) ---

def navigate_to_url(driver, url, wait_time=config.DEFAULT_WAIT_TIME):
    """Navigates the driver to the specified URL and waits."""
    logging.info(f"Navigating to URL: {url}")
    try:
        driver.get(url)
        actual_wait_time = int(os.getenv("WAIT_TIME", wait_time))
        logging.info(f"Successfully navigated to {url}. Waiting for {actual_wait_time} seconds...")
        time.sleep(actual_wait_time) # Simple wait, improve with explicit waits if needed
        logging.info("Wait complete.")
        return True
    except WebDriverException as e:
        logging.error(f"Error navigating to {url}: {e}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred during navigation: {e}", exc_info=True)
        return False

# --- Data Extraction Function (ABSTRACT - TO BE IMPLEMENTED BY USER) ---

def extract_data(page_source):
    """
    Parses HTML source and extracts data. MUST BE IMPLEMENTED for the specific target.

    This base implementation raises NotImplementedError. Copy this base scraper
    project and implement the BeautifulSoup (or other parsing) logic within
    this function in your new project's scraper.py.

    Args:
        page_source (str): The HTML source code of the page.

    Returns:
        list: A list of dictionaries representing the extracted data items.
    """
    logging.info("Attempting to extract data (Needs implementation)...")
    soup = BeautifulSoup(page_source, 'html.parser')
    # --- IMPLEMENTATION REQUIRED PER TARGET SITE ---
    # Example structure you might return:
    # extracted_items = [{'col1': 'value1', 'col2': 'value2'}, {'col1': 'valueA', 'col2': 'valueB'}]
    # return extracted_items
    # --- --------------------------------------- ---
    logging.warning("extract_data function not implemented in base.")
    raise NotImplementedError("The 'extract_data' function must be implemented in the project using this base scraper.")
    # Or, alternatively, just return an empty list if you prefer not to force an error:
    # return []

# --- Data Handling Function (ABSTRACT - TO BE IMPLEMENTED BY USER) ---

def handle_data(data, output_target=config.DEFAULT_OUTPUT_FILENAME):
    """
    Handles the extracted data. MUST BE IMPLEMENTED for the desired action.

    This base implementation raises NotImplementedError. Copy this base scraper
    project and implement your desired data handling logic (e.g., save to CSV
    using Pandas, save to database, send to API) within this function in
    your new project's scraper.py.

    Args:
        data (list): The list of dictionaries returned by extract_data.
        output_target (str): A configuration parameter indicating where/how
                             to save or send the data (e.g., filename, DB connection string).
    """
    if not data:
        logging.warning("No data provided to handle_data function.")
        return False

    logging.info(f"Attempting to handle data (Needs implementation)... Target: {output_target}")
    # --- IMPLEMENTATION REQUIRED FOR DESIRED OUTPUT ---
    # Example: Save to CSV using Pandas
    # try:
    #     import pandas as pd
    #     output_filename = os.getenv("OUTPUT_FILENAME", output_target)
    #     df = pd.DataFrame(data)
    #     output_dir = os.path.dirname(output_filename)
    #     if output_dir and not os.path.exists(output_dir): os.makedirs(output_dir)
    #     df.to_csv(output_filename, index=False, encoding='utf-8')
    #     logging.info(f"Data successfully saved to {output_filename}.")
    #     return True
    # except Exception as e:
    #     logging.error(f"Error saving data to CSV: {e}")
    #     return False

    # Example: Print to console
    # for item in data:
    #     print(item)
    # return True
    # --- ------------------------------------------ ---
    logging.warning("handle_data function not implemented in base.")
    raise NotImplementedError("The 'handle_data' function must be implemented in the project using this base scraper.")
    # Or, alternatively, just log and return False:
    # logging.info(f"Data received but not handled: {data[:2]}")
    # return False


# --- Main Orchestration Function (Handles the flow) ---

def run_scraper(target_url=None, output_file=None, headless=None, wait_time=None):
    """Runs the full scraping process framework."""
    url_to_scrape = target_url if target_url is not None else os.getenv("TARGET_URL", config.DEFAULT_TARGET_URL)
    output_target = output_file if output_file is not None else os.getenv("OUTPUT_FILENAME", config.DEFAULT_OUTPUT_FILENAME)
    run_headless_mode = headless if headless is not None else os.getenv("HEADLESS", str(config.DEFAULT_HEADLESS_MODE)).lower() in ('true', '1', 't')
    navigation_wait_time = wait_time if wait_time is not None else int(os.getenv("WAIT_TIME", config.DEFAULT_WAIT_TIME))

    logging.info(f"--- Starting Base Scraper Framework ---")
    logging.info(f"Target URL: {url_to_scrape}")
    logging.info(f"Output Target: {output_target}") # Note: Handling depends on implementation
    logging.info(f"Headless Mode: {run_headless_mode}")
    logging.info(f"Navigation Wait: {navigation_wait_time}s")

    driver = None
    success = False
    try:
        driver = setup_driver(headless=run_headless_mode)
        if not driver: raise Exception("WebDriver setup failed.")

        navigation_successful = navigate_to_url(driver, url_to_scrape, wait_time=navigation_wait_time)
        if not navigation_successful: raise Exception(f"Navigation to {url_to_scrape} failed.")

        logging.info("Navigation successful. Getting page source...")
        html_source = driver.page_source
        logging.info(f"Page source length: {len(html_source)}")

        # --- Attempt to extract and handle data (Requires implementation) ---
        try:
            scraped_data = extract_data(html_source)
            if scraped_data: # Only proceed if extract_data returns non-empty list
                success = handle_data(scraped_data, output_target)
                if success:
                     logging.info("Data handling completed successfully (as implemented).")
                else:
                    logging.warning("Data handling failed or returned False (as implemented).")
            else:
                logging.warning("No data extracted (as implemented), skipping data handling.")
                # Consider if base should still signal success if no data is expected/found
                success = True # Or False, depending on desired base behavior? Let's assume True if process ran.

        except NotImplementedError:
             logging.error("CRITICAL: 'extract_data' or 'handle_data' function is not implemented in this project!")
             logging.error("Please copy the base scraper and implement these functions.")
             success = False # Indicate failure due to missing implementation
        except Exception as e:
             logging.error(f"Error during extraction or handling phase: {e}", exc_info=True)
             success = False

        logging.info(f"--- Scraper Framework Finished (Success: {success}) ---")

    except Exception as e:
        logging.error(f"A critical error occurred in the main scraping process: {e}", exc_info=True)
        success = False
    finally:
        if driver:
            driver.quit()
            logging.info("WebDriver closed.")

    return success # Return overall success status