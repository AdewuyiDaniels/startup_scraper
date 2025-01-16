# Package initialization file

# Expose the main functions and classes
from .scraper import (
    scrape_angellist,
    scrape_crunchbase,
    scrape_producthunt,
    scrape_google_search,
    scrape_linkedin
)
from .email_finder import get_emails
from .utils import save_to_csv

# Define what gets imported with `from scraper import *`
__all__ = [
    'scrape_angellist',
    'scrape_crunchbase',
    'scrape_producthunt',
    'scrape_google_search',
    'scrape_linkedin',
    'get_emails',
    'save_to_csv'
]