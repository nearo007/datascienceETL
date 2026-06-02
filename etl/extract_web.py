import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from .utils import parse_price


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def scrape_list_page(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'lxml')
    now = datetime.utcnow().strftime("%Y-%m-%d")
    rows = []
    # Try multiple selector patterns used by MercadoLibre
    for item in soup.select("li.ui-search-layout__item, .andes-card, [data-polygon-id]"):
        title_tag = item.select_one("h2, .ui-search-item__title, [data-article]")
        price_tag = item.select_one(".andes-money-amount__fraction, .price-tag-fraction, [class*=price]")
        title = title_tag.get_text(strip=True) if title_tag else None
        price = parse_price(price_tag.get_text(strip=True)) if price_tag else None
        if title and price:
            rows.append({"product_name": title, "price": price, "url": url, "extraction_date": now})
    return pd.DataFrame(rows)


if __name__ == '__main__':
    df = scrape_list_page('https://lista.mercadolivre.com.br/arroz')
    print(df.head())
