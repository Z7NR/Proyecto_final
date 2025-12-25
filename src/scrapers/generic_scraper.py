import re
import requests
from bs4 import BeautifulSoup
from src.scrapers.base import BaseScraper

class GenericScraper(BaseScraper):

    def scrape(self, url: str) -> dict:
        r = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )

        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.find("h1") or soup.find("title")
        nombre = title.get_text(strip=True) if title else None

        precio = 0.0
        price_el = soup.select_one("[itemprop=price], .price, .precio")
        if price_el:
            raw = re.sub(r"[^0-9.,]", "", price_el.get_text())
            raw = raw.replace(",", ".")
            try:
                precio = float(raw)
            except ValueError:
                pass

        desc = ""
        meta_desc = soup.find("meta", {"name": "description"})
        if meta_desc:
            desc = meta_desc.get("content", "")

        return {
            "nombre": nombre,
            "descripcion": desc,
            "precio": precio,
            "categoria": "importado",
            "stock": 0,
            "fuente": "generic"
        }