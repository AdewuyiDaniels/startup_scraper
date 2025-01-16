# Utility functions for logging, validation, etc.

import logging
from typing import Dict, List
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_company_data(company: Dict) -> bool:
    """Validate scraped company data."""
    required_fields = ['name', 'website', 'description']
    return all(field in company for field in required_fields)

def save_to_csv(data: List[Dict], filename: str = 'data/startup_emails.csv'):
    """Save data to a CSV file."""
    df = pd.DataFrame(data)
    # Ensure all required columns are present
    df = df.reindex(columns=['name', 'website', 'Person Name', 'Person Position', 'Email'], fill_value='')
    df.to_csv(filename, index=False)
    logging.info(f"Saved {len(data)} records to {filename}.")