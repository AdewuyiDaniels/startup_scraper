# Entry point for the script

from scraper.scraper import scrape_angellist, scrape_crunchbase, scrape_producthunt, scrape_google_search, scrape_linkedin
from scraper.email_finder import get_emails
from scraper.utils import save_to_csv
import asyncio

async def main():
    """Main function to scrape, filter, and fetch emails."""
    # Scrape data from all platforms
    startups = await scrape_angellist()
    companies = await scrape_crunchbase()
    products = await scrape_producthunt()
    google_results = await scrape_google_search("startups hiring data scientists")
    linkedin_results = await scrape_linkedin("data science startups")

    # Combine all data
    all_data = startups + companies + products + google_results + linkedin_results

    # Fetch emails and prepare final data
    final_data = []
    for item in all_data:
        emails = await get_emails(item['website'])
        if emails:
            # Add person name and position
            item.update({
                'Person Name': emails[0]['value'].split('@')[0],  # Extract name from email
                'Person Position': emails[0]['type'].title(),  # Capitalize position
                'Email': emails[0]['value']
            })
            final_data.append(item)

    # Save to CSV
    save_to_csv(final_data)

if __name__ == '__main__':
    asyncio.run(main())