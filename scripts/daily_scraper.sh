#!/bin/bash
cd /home/cryptoscraper/coingecko/
source venv/bin/activate
cd crypto-scraper
python -c 'from tasks import daily_scraper; daily_scraper()'