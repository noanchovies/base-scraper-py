```python
# src/basescraper/cli.py

import typer
from rich.console import Console
import logging
import sys

# Import the main scraper function and config
try:
    from basescraper import scraper, config
except ImportError:
    # This allows running the CLI directly using `python -m src.basescraper.cli run`
    # without installing the package, by adjusting the Python path.
    import sys
    import os
    # Add the parent directory (project root) to the Python path
    # to allow finding the 'src' package
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    # Now try relative import from 'src' perspective
    from src.basescraper import scraper, config


# --- Typer App Initialization ---
app = typer.Typer(help="A generic base scraper framework using Selenium.")
console = Console()

# Configure root logger for CLI visibility if needed (scraper also configures)
log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
log_level = getattr(logging, log_level_str, logging.INFO)
logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s') # Simpler format for CLI

# --- CLI Command ---

@app.command()
def run(
    target_url: str = typer.Option(
        None, "--url", "-u",
        help="Target URL to scrape. Overrides TARGET_URL env var and config.py default.",
    ),
    output_file: str = typer.Option( # Renamed for clarity, used as 'output_target' in handle_data
        None, "--output", "-o",
        help="Output target (e.g., filename). Overrides OUTPUT_FILENAME env var and config.py default.",
    ),
    headless: bool = typer.Option(
        None, "--headless/--no-headless",
        help="Run browser headless. Overrides HEADLESS env var/config.",
    ),
    wait_time: int = typer.Option(
        None, "--wait", "-w",
        help="Wait time after page load (secs). Overrides WAIT_TIME env var/config.",
    )
):
    """
    Runs the base scraper framework for the specified target URL.
    NOTE: Requires 'extract_data' and 'handle_data' to be implemented
    in scraper.py for the specific project using this base.
    """
    console.print(f"[bold green]Starting base scraper framework via CLI...[/bold green]")
    try:
        # Call the main scraper orchestration function
        success = scraper.run_scraper(
            target_url=target_url,
            output_file=output_file,
            headless=headless,
            wait_time=wait_time
        )
        if success:
            console.print(f"[bold green]Framework finished successfully (Data handling depends on implementation).[/bold green]")
            raise typer.Exit(code=0)
        else:
            console.print(f"[bold yellow]Framework finished, but potential issues occurred (check logs).[/bold yellow]")
            raise typer.Exit(code=1)

    except NotImplementedError as e:
         console.print(f"[bold red]Execution Failed:[/bold red] {e}")
         console.print("Please copy this base project and implement the required functions in scraper.py.")
         raise typer.Exit(code=2)
    except Exception as e:
        console.print(f"[bold red]CLI Error: An unexpected exception occurred:[/bold red]")
        # Log the full exception for debugging
        logging.exception("Unhandled exception in CLI")
        raise typer.Exit(code=1)


# --- Entry point for CLI ---
if __name__ == "__main__":
    app()
```