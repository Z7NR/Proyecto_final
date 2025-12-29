import requests
import re
from bs4 import BeautifulSoup

class GenericScraper:

    def scrape(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        # Nombre
        title = soup.find("h1") or soup.find("title")
        nombre = title.get_text(strip=True) if title else "Producto importado"

        # Precio (heurístico)
        precio = 0.0
        for sel in ["[itemprop=price]", ".price", ".product-price", ".precio"]:
            el = soup.select_one(sel)
            if el:
                raw = re.sub(r"[^0-9.,]", "", el.get_text())
                try:
                    precio = float(raw.replace(",", "."))
                    break
                except:
                    pass

        return {
            "nombre": nombre,
            "descripcion": f"Importado desde {url}",
            "precio": precio,
            "categoria": "importado",
            "stock": 0
        }