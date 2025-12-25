import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class AliExpressScraper(BaseScraper):

    def fetch(self, url):
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')

        nombre = soup.select_one(".product-title-text")
        nombre = nombre.get_text(strip=True) if nombre else "Producto AliExpress"

        price = soup.select_one(".product-price-value")
        precio = self.clean_price(price.get_text(strip=True)) if price else 0.0

        desc = soup.select_one(".product-detail-main")
        descripcion = desc.get_text(" ", strip=True) if desc else ""

        return {
            "nombre": nombre,
            "precio": precio,
            "descripcion": descripcion
        }