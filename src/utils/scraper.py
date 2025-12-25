import re
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def scrape_with_requests(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.find("h1") or soup.find("title")
        nombre = title.get_text(strip=True) if title else None

        price_selectors = [
            ".price", ".product-price", "[itemprop=price]",
            ".precio", ".Price", ".price-tag", ".ui-pdp-price__part"
        ]

        price_raw = None
        for sel in price_selectors:
            el = soup.select_one(sel)
            if el:
                price_raw = el.get_text(strip=True)
                break

        precio = None
        if price_raw:
            value = re.sub(r"[^0-9\.,]", "", price_raw).replace(",", ".")
            try:
                precio = float(value)
            except:
                precio = None

        desc_el = soup.find("meta", {"name": "description"})
        descripcion = desc_el.get("content") if desc_el else None

        if not nombre or precio is None:
            return None

        return {
            "nombre": nombre,
            "precio": precio,
            "descripcion": descripcion or ""
        }

    except Exception:
        return None

def scrape_with_playwright(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)

            title_selectors = [
                "h1",
                ".product-title-text",
                ".ui-pdp-title",
                "title"
            ]

            nombre = None
            for sel in title_selectors:
                el = page.query_selector(sel)
                if el:
                    nombre = el.inner_text().strip()
                    break

            price_selectors = [
                ".product-price-value",
                ".ui-pdp-price__second-line span",
                "[itemprop=price]",
                ".price"
            ]

            precio = None
            for sel in price_selectors:
                el = page.query_selector(sel)
                if el:
                    value = el.inner_text().strip()
                    value = re.sub(r"[^0-9\.,]", "", value).replace(",", ".")
                    try:
                        precio = float(value)
                    except:
                        precio = None
                    break

            desc_el = page.query_selector("meta[name='description']")
            descripcion = desc_el.get_attribute("content") if desc_el else ""

            browser.close()

            return {
                "nombre": nombre or "Producto sin nombre",
                "precio": precio or 0.0,
                "descripcion": descripcion
            }

    except Exception as e:
        print("Playwright error:", e)
        return None


def scrap_product(url):
    data = scrape_with_requests(url)
    if data:
        return data

    return scrape_with_playwright(url)