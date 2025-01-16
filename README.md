# Startup Scraper

A Python script to scrape startup data from multiple platforms and fetch relevant emails for outreach.

## Features
- Scrapes startup data from AngelList, Crunchbase, Product Hunt, Google Search, and LinkedIn.
- Fetches emails using Hunter.io, Clearbit, and EmailHunter APIs with fallback logic.
- Filters companies based on relevance to data science, AI, machine learning, and analytics.
- Saves results to a CSV file with company name, website, person name, person position, and email.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/startup-scraper.git

Install dependencies:

      ```bash
      pip install -r requirements.txt
Add your API keys to scraper/config.py.

Usage
Run the script:

      ```bash
     python main.py

