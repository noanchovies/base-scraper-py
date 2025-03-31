Use https://github.com/noanchovies/scraper-engine instead 

---CURRENTLY BEING REVISED AND POTENTIALLY TO BE MERGED WITH A NEWER MORE EFFICIENT VERSION---

# Base Scraper Template (Python/Selenium)

A generic base template project for building web scrapers using Python, Selenium, BeautifulSoup, and Typer. Designed to be easily copied and adapted for various scraping targets.

**Note:** For quickly briefing AI assistants (like Google Gemini) on this template's structure and how to adapt it, refer to the `AI_CONTEXT.txt` file in the project root. It includes a summary and an adaptation checklist for next steps.

## Key Features

* **Selenium WebDriver:** Uses Selenium with `webdriver-manager` for automated browser control, capable of handling dynamic JavaScript-heavy websites. Configurable headless mode.
* **HTML Parsing:** Integrates BeautifulSoup for parsing HTML structure obtained via Selenium.
* **Configurable:** Easily configure target URLs, output filenames, wait times, and headless mode via `src/basescraper/config.py`, `.env` files, or command-line arguments.
* **CLI Interface:** Uses Typer to provide a clean command-line interface for running the scraper.
* **Modular Structure:** Separates concerns into configuration (`config.py`), core scraping logic (`scraper.py`), and CLI (`cli.py`) within a standard `src` layout.
* **Placeholder Implementation:** Core data extraction (`extract_data`) and data handling (`handle_data`) functions are provided as clear placeholders (`NotImplementedError`) that **must** be implemented for each specific scraping project.
* **Structured Output (Example):** Includes an optional pattern for saving data to CSV using Pandas (`save_to_csv` function commented out within `handle_data` placeholder).

## Technology Stack

* **Language:** Python 3.8+
* **Browser Automation:** Selenium
* **Driver Management:** webdriver-manager
* **HTML Parsing:** BeautifulSoup4
* **Data Handling (Example):** Pandas (for CSV saving pattern)
* **CLI:** Typer, Rich
* **Configuration:** python-dotenv
* **Packaging:** setuptools, pyproject.toml

## Setup (For Using the Template)

1.  **Copy Template:** Create a new project by copying this entire `base-scraper-py` directory.
2.  **Navigate:** `cd` into your new project directory.
3.  **Create Virtual Environment:** `python -m venv venv`
4.  **Activate Environment:**
    * Windows: `.\venv\Scripts\activate`
    * macOS/Linux: `source venv/bin/activate`
5.  **Install Dependencies:** `pip install -r requirements.txt`
6.  **(Optional) Git Init:** If desired, delete the copied `.git` folder, run `git init`, create a new remote repository, and link it (`git remote add origin <url>`).

## Usage

1.  **Implement Logic:** Follow the detailed steps in `HOW_TO_USE_BASE.txt` to implement the required `extract_data` and `handle_data` functions within `src/basescraper/scraper.py` for your specific target website.
2.  **Configure:** Set your target URL and other parameters in `.env` or `src/basescraper/config.py`.
3.  **Run from CLI:**
    * Option A (Run as module): `python -m src.basescraper.cli run [OPTIONS]`
    * Option B (If installed editable `pip install -e .`): `basescraper run [OPTIONS]`
4.  **CLI Options:** Use `--help` to see available options:
    ```bash
    python -m src.basescraper.cli run --help
    # or
    basescraper run --help
    ```
    Example: `basescraper run --url "your-target-url.com" -o "my_output.csv" --no-headless`

## Adapting the Base

The core adaptation steps are detailed in `HOW_TO_USE_BASE.txt`. Primarily involves implementing:

* `extract_data(page_source)`: Add logic using BeautifulSoup selectors to parse the HTML (`page_source`) from your target site and return a list of dictionaries.
* `handle_data(data, output_target)`: Add logic to process the list of dictionaries returned by `extract_data` (e.g., save to CSV, database, API).

## License

MIT License (Update `LICENSE` file and `pyproject.toml` if using a different license).

## Contributing / Contact

(Add details here if you plan for others to contribute or how to contact you).
