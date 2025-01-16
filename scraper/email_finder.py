# Asynchronous email finding logic with multi-API fallback

import aiohttp
from typing import List, Dict
from .config import HUNTER_API_KEY, CLEARBIT_API_KEY, EMAILHUNTER_API_KEY
import logging

async def get_emails_hunter(session: aiohttp.ClientSession, domain: str) -> List[Dict]:
    """Fetch emails using Hunter.io API."""
    url = "https://api.hunter.io/v2/domain-search"
    params = {
        'domain': domain,
        'api_key': HUNTER_API_KEY
    }
    try:
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            data = await response.json()
            emails = data.get('data', {}).get('emails', [])
            # Filter out generic emails and prioritize specific roles
            valid_emails = []
            for email in emails:
                if any(word in email['value'] for word in ['contact', 'support', 'info']):
                    continue
                # Prioritize C-suite and hiring roles
                if any(role in email['type'] for role in ['ceo', 'cto', 'hiring', 'head of data']):
                    valid_emails.insert(0, email)  # Add to the top of the list
                else:
                    valid_emails.append(email)
            logging.info(f"Fetched {len(valid_emails)} valid emails for {domain} using Hunter.io.")
            return valid_emails[:2]  # Return up to 2 emails
    except Exception as e:
        logging.error(f"Hunter.io API error for {domain}: {e}")
        return []

async def get_emails_clearbit(session: aiohttp.ClientSession, domain: str) -> List[Dict]:
    """Fetch emails using Clearbit API."""
    url = "https://company.clearbit.com/v2/companies/find"
    params = {
        'domain': domain,
        'api_key': CLEARBIT_API_KEY
    }
    try:
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            data = await response.json()
            emails = data.get('emails', [])
            # Filter out generic emails and prioritize specific roles
            valid_emails = []
            for email in emails:
                if any(word in email['value'] for word in ['contact', 'support', 'info']):
                    continue
                # Prioritize C-suite and hiring roles
                if any(role in email['type'] for role in ['ceo', 'cto', 'hiring', 'head of data']):
                    valid_emails.insert(0, email)  # Add to the top of the list
                else:
                    valid_emails.append(email)
            logging.info(f"Fetched {len(valid_emails)} valid emails for {domain} using Clearbit.")
            return valid_emails[:2]  # Return up to 2 emails
    except Exception as e:
        logging.error(f"Clearbit API error for {domain}: {e}")
        return []

async def get_emails_emailhunter(session: aiohttp.ClientSession, domain: str) -> List[Dict]:
    """Fetch emails using EmailHunter API."""
    url = "https://api.emailhunter.co/v1/search"
    params = {
        'domain': domain,
        'api_key': EMAILHUNTER_API_KEY
    }
    try:
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            data = await response.json()
            emails = data.get('emails', [])
            # Filter out generic emails and prioritize specific roles
            valid_emails = []
            for email in emails:
                if any(word in email['value'] for word in ['contact', 'support', 'info']):
                    continue
                # Prioritize C-suite and hiring roles
                if any(role in email['type'] for role in ['ceo', 'cto', 'hiring', 'head of data']):
                    valid_emails.insert(0, email)  # Add to the top of the list
                else:
                    valid_emails.append(email)
            logging.info(f"Fetched {len(valid_emails)} valid emails for {domain} using EmailHunter.")
            return valid_emails[:2]  # Return up to 2 emails
    except Exception as e:
        logging.error(f"EmailHunter API error for {domain}: {e}")
        return []

async def get_emails(domain: str) -> List[Dict]:
    """Fetch emails using multiple APIs with fallback logic."""
    apis = [
        get_emails_hunter,
        get_emails_clearbit,
        get_emails_emailhunter
    ]
    async with aiohttp.ClientSession() as session:
        for api in apis:
            emails = await api(session, domain)
            if emails:
                return emails
    logging.warning(f"No emails found for {domain} using any API.")
    return []