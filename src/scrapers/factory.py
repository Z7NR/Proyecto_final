from urllib.parse import urlparse
from src.scrapers.amazon_scraper import AmazonScraper
from src.scrapers.ebay_scraper import EbayScraper
from src.scrapers.aliexpress_scraper import AliExpressScraper
from src.scrapers.generic_scraper import GenericScraper

class ScraperFactory:

    @staticmethod
    def get_scraper(url: str):
        domain = urlparse(url).netloc.lower()

        if "amazon" in domain:
            return AmazonScraper()
        if "ebay" in domain:
            return EbayScraper()
        if "aliexpress" in domain:
            return AliExpressScraper()

        return GenericScraper()