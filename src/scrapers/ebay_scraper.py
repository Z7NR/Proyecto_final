import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class EbayScraper(BaseScraper):

    def fetch(self, url):
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')

        nombre = soup.select_one("h1.x-item-title__mainTitle")
        nombre = nombre.get_text(strip=True) if nombre else "Producto eBay"

        price = soup.select_one(".x-price-primary")
        precio = self.clean_price(price.get_text(strip=True)) if price else 0.0

        desc = soup.select_one("#viTabs_0_is")
        descripcion = desc.get_text(" ", strip=True) if desc else ""

        return {
            "nombre": nombre,
            "precio": precio,
            "descripcion": descripcion
        }