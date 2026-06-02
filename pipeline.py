import os
import pandas as pd
from etl.extract_api import fetch_prices_api
from etl.extract_csv import load_csv
from etl.extract_web import scrape_list_page
from etl.extract_pdf import extract_tables_from_pdf
from etl.utils import unify_columns
from etl.load import save_to_sqlite, generate_pdf_report


OUTPUT_DIR = os.path.abspath('output')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_sample_pipeline():
    # 1) API (exchange rates via AwesomeAPI)
    try:
        df_api = fetch_prices_api()
    except Exception as e:
        print('API fetch failed:', e)
        df_api = pd.DataFrame()

    # 2) CSV (if exists)
    csv_path = 'sample_prices.csv'
    if os.path.exists(csv_path):
        df_csv = load_csv(csv_path)
    else:
        df_csv = pd.DataFrame()

    # 3) Web scrape (best-effort)
    try:
        df_web = scrape_list_page('https://lista.mercadolivre.com.br/arroz')
    except Exception as e:
        print('Web scrape failed:', e)
        df_web = pd.DataFrame()

    # 4) PDFs (if present)
    pdf_path = 'folheto.pdf'
    if os.path.exists(pdf_path):
        df_pdf = extract_tables_from_pdf(pdf_path)
    else:
        df_pdf = pd.DataFrame()

    # unify and concat
    dfs = [df_api, df_csv, df_web, df_pdf]
    dfs = [unify_columns(df) for df in dfs if not df.empty]
    if dfs:
        full = pd.concat(dfs, ignore_index=True, sort=False)
    else:
        full = pd.DataFrame()

    # save outputs
    if not full.empty:
        full.to_excel(os.path.join(OUTPUT_DIR, 'combined_prices.xlsx'), index=False)
        full.to_csv(os.path.join(OUTPUT_DIR, 'combined_prices.csv'), index=False)
        # Persist to SQLite and generate PDF report
        db_path = os.path.join(OUTPUT_DIR, 'prices.db')
        try:
            save_to_sqlite(full, db_path)
        except Exception as e:
            print('Failed saving to DB:', e)
        try:
            generate_pdf_report(full, os.path.join(OUTPUT_DIR, 'report.pdf'))
        except Exception as e:
            print('Failed generating PDF report:', e)
        print('Saved combined datasets to output/')
    else:
        print('No data collected in this run.')


if __name__ == '__main__':
    run_sample_pipeline()
