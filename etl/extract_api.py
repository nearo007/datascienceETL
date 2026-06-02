import requests
import pandas as pd
from datetime import datetime


CURRENCIES = [
    ("USD-BRL", "USD/BRL", "Dólar Americano"),
    ("EUR-BRL", "EUR/BRL", "Euro"),
    ("GBP-BRL", "GBP/BRL", "Libra Esterlina"),
    ("ARS-BRL", "ARS/BRL", "Peso Argentino"),
    ("CAD-BRL", "CAD/BRL", "Dólar Canadense"),
    ("AUD-BRL", "AUD/BRL", "Dólar Australiano"),
]


def fetch_prices_api():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,GBP-BRL,ARS-BRL,CAD-BRL,AUD-BRL"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    rows = []
    now = datetime.utcnow().strftime("%Y-%m-%d")
    for code, pair, name in CURRENCIES:
        key = code.replace("-", "")
        item = data.get(key, {})
        rows.append({
            "product_name": f"{name} ({pair})",
            "price": float(item.get("bid", 0)),
            "currency": "BRL",
            "store": "AwesomeAPI",
            "url": f"https://economia.awesomeapi.com.br/{code}",
            "extraction_date": now,
        })
    return pd.DataFrame(rows)


if __name__ == '__main__':
    df = fetch_prices_api()
    print(df.head())
