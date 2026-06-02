import re
import pandas as pd
from datetime import datetime


def parse_price(text):
    if text is None:
        return None
    s = re.sub(r"[^0-9,\.]+", "", str(text))
    comma_count = s.count(',')
    dot_count = s.count('.')
    if comma_count == 0:
        pass
    elif comma_count == 1 and dot_count == 0:
        s = s.replace(',', '.')
    elif dot_count > 0:
        last_comma = s.rfind(',')
        last_dot = s.rfind('.')
        if last_comma > last_dot:
            s = s.replace('.', '').replace(',', '.')
        else:
            s = s.replace(',', '')
    else:
        s = s.replace(',', '')
    try:
        return float(s)
    except Exception:
        return None


def unify_columns(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {}
    lower = {c.lower(): c for c in df.columns}
    for want in ['product_name','price','currency','store','url','extraction_date']:
        for k,v in lower.items():
            if want in k:
                mapping[v] = want
                break
    df = df.rename(columns=mapping)
    if 'extraction_date' not in df.columns:
        df['extraction_date'] = datetime.utcnow()
    return df
