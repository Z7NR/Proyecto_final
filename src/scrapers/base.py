class BaseScraper:
    def scrape(self, url: str) -> dict:
        raise NotImplementedError