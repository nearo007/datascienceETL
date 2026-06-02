import pdfplumber
import pandas as pd


def extract_tables_from_pdf(path):
    rows = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                df = pd.DataFrame(table[1:], columns=table[0])
                rows.append(df)
    if rows:
        return pd.concat(rows, ignore_index=True)
    return pd.DataFrame()


if __name__ == '__main__':
    import sys
    p = sys.argv[1] if len(sys.argv)>1 else 'folheto.pdf'
    print(extract_tables_from_pdf(p).head())
