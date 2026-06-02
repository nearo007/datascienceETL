import pandas as pd
import numpy as np
from .utils import parse_price


def clean_prices(df: pd.DataFrame, price_col='price') -> pd.DataFrame:
    df = df.copy()
    if price_col in df.columns:
        df[price_col] = df[price_col].apply(lambda x: parse_price(x) if not pd.isna(x) else x)
    return df


def fill_missing_store(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if 'store' in df.columns:
        df['store'] = df['store'].fillna('unknown')
    return df


def remove_price_outliers(df: pd.DataFrame, price_col='price') -> pd.DataFrame:
    df = df.copy()
    if price_col in df.columns:
        q1 = df[price_col].quantile(0.05)
        q3 = df[price_col].quantile(0.95)
        df = df[(df[price_col] >= q1) & (df[price_col] <= q3)]
    return df


def normalize_product_names(df: pd.DataFrame, col='product_name') -> pd.DataFrame:
    df = df.copy()
    if col in df.columns:
        df[col] = df[col].str.lower().str.replace('\n',' ').str.replace('\r',' ').str.strip()
    return df


def pipeline_clean(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = clean_prices(df)
    df = fill_missing_store(df)
    df = normalize_product_names(df)
    df = remove_price_outliers(df)
    df = df.drop_duplicates(subset=['product_name','price','store'], keep='last')
    return df


if __name__ == '__main__':
    import pandas as pd
    df = pd.DataFrame({'product_name':['Arroz 5kg','Arroz 5kg','Leite 1L'], 'price':['R$ 20,50','25,00','3.50']})
    print(pipeline_clean(df))
