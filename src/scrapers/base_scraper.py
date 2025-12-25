class BaseScraper:
    def fetch(self, url):
        """Método general, lo sobrescriben los scrapers específicos."""
        raise NotImplementedError

    def clean_price(self, price_text):
        import re
        cleaned = re.sub(r'[^0-9\.,]', '', price_text).replace(',', '.')
        try:
            return float(cleaned)
        except:
            return 0.0