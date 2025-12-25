import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class AmazonScraper(BaseScraper):

    def fetch(self, url):
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')

        title = soup.select_one("#productTitle")
        nombre = title.get_text(strip=True) if title else "Producto Amazon"

        price = soup.select_one("#priceblock_ourprice") \
            or soup.select_one("#priceblock_dealprice")
        precio = self.clean_price(price.get_text(strip=True)) if price else 0.0

        desc = soup.select_one("#feature-bullets")
        descripcion = desc.get_text(" ", strip=True) if desc else ""

        return {
            "nombre": nombre,
            "precio": precio,
            "descripcion": descripcion
        }
