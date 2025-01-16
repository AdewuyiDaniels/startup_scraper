# Core asynchronous scraping logic for all platforms

import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
from .utils import validate_company_data
from .config import REQUEST_DELAY, USER_AGENT, KEYWORDS
import asyncio
import logging

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    """Fetch HTML content asynchronously."""
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return ""

def is_relevant_company(description: str) -> bool:
    """Check if a company is relevant based on keywords."""
    return any(keyword.lower() in description.lower() for keyword in KEYWORDS)

async def scrape_angellist() -> List[Dict]:
    """Scrape startup data from AngelList."""
    url = "https://angel.co/companies"
    async with aiohttp.ClientSession(headers={'User-Agent': USER_AGENT}) as session:
        html = await fetch(session, url)
        if not html:
            return []
        soup = BeautifulSoup(html, 'html.parser')
        startups = []
        for item in soup.select('.startup-link'):
            name = item.select_one('.startup-name').text.strip()
            website = item.select_one('.website-link').get('href')
            description = item.select_one('.description').text.strip()
            if is_relevant_company(description):
                company = {'name': name, 'website': website, 'description': description}
                if validate_company_data(company):
                    startups.append(company)
        logging.info(f"Scraped {len(startups)} relevant startups from AngelList.")
        return startups

async def scrape_crunchbase() -> List[Dict]:
    """Scrape company data from Crunchbase."""
    url = "https://www.crunchbase.com/discover/organization.companies"
    async with aiohttp.ClientSession(headers={'User-Agent': USER_AGENT}) as session:
        html = await fetch(session, url)
        if not html:
            return []
        soup = BeautifulSoup(html, 'html.parser')
        companies = []
        for item in soup.select('.company-card'):
            name = item.select_one('.company-name').text.strip()
            website = item.select_one('.website-link').get('href')
            description = item.select_one('.description').text.strip()
            if is_relevant_company(description):
                company = {'name': name, 'website': website, 'description': description}
                if validate_company_data(company):
                    companies.append(company)
        logging.info(f"Scraped {len(companies)} relevant companies from Crunchbase.")
        return companies

async def scrape_producthunt() -> List[Dict]:
    """Scrape product data from Product Hunt."""
    url = "https://www.producthunt.com"
    async with aiohttp.ClientSession(headers={'User-Agent': USER_AGENT}) as session:
        html = await fetch(session, url)
        if not html:
            return []
        soup = BeautifulSoup(html, 'html.parser')
        products = []
        for item in soup.select('.product-item'):
            name = item.select_one('.product-name').text.strip()
            website = item.select_one('.website-link').get('href')
            description = item.select_one('.description').text.strip()
            if is_relevant_company(description):
                product = {'name': name, 'website': website, 'description': description}
                if validate_company_data(product):
                    products.append(product)
        logging.info(f"Scraped {len(products)} relevant products from Product Hunt.")
        return products

async def scrape_google_search(query: str) -> List[Dict]:
    """Scrape company data from Google Search."""
    url = f"https://www.google.com/search?q={query}"
    async with aiohttp.ClientSession(headers={'User-Agent': USER_AGENT}) as session:
        html = await fetch(session, url)
        if not html:
            return []
        soup = BeautifulSoup(html, 'html.parser')
        companies = []
        for item in soup.select('.tF2Cxc'):
            name = item.select_one('.DKV0Md').text.strip()
            website = item.select_one('.yuRUbf a').get('href')
            description = item.select_one('.VwiC3b').text.strip()
            if is_relevant_company(description):
                company = {'name': name, 'website': website, 'description': description}
                if validate_company_data(company):
                    companies.append(company)
        logging.info(f"Scraped {len(companies)} relevant companies from Google Search.")
        return companies

async def scrape_linkedin(query: str) -> List[Dict]:
    """Scrape company data from LinkedIn."""
    url = f"https://www.linkedin.com/search/results/companies/?keywords={query}"
    async with aiohttp.ClientSession(headers={'User-Agent': USER_AGENT}) as session:
        html = await fetch(session, url)
        if not html:
            return []
        soup = BeautifulSoup(html, 'html.parser')
        companies = []
        for item in soup.select('.entity-result'):
            name = item.select_one('.entity-result__title-text').text.strip()
            website = item.select_one('.entity-result__primary-subtitle').text.strip()
            description = item.select_one('.entity-result__summary').text.strip()
            if is_relevant_company(description):
                company = {'name': name, 'website': website, 'description': description}
                if validate_company_data(company):
                    companies.append(company)
        logging.info(f"Scraped {len(companies)} relevant companies from LinkedIn.")
        return companies