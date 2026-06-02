import pandas as pd
from sqlalchemy import create_engine
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import os


def save_to_sqlite(df: pd.DataFrame, db_path: str, table_name='prices') -> None:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    engine = create_engine(f'sqlite:///{db_path}')
    df.to_sql(table_name, engine, if_exists='replace', index=False)


def generate_pdf_report(df: pd.DataFrame, pdf_path: str, title='Relatório de Preços') -> None:
    # Simple tabular PDF report: first 30 rows
    rows = [list(df.columns)] + df.head(30).fillna('').astype(str).values.tolist()
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    c.setFont('Helvetica-Bold', 14)
    c.drawString(40, height-40, title)
    table = Table(rows, colWidths=[(width-80)/len(rows[0])] * len(rows[0]))
    style = TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
    ])
    table.setStyle(style)
    w, h = table.wrapOn(c, width-80, height-120)
    table.drawOn(c, 40, height-80-h)
    c.save()


if __name__ == '__main__':
    import pandas as pd
    df = pd.DataFrame({'product_name':['arroz','leite'],'price':[20.5,3.2],'store':['loja A','loja B']})
    save_to_sqlite(df, 'output/prices.db')
    generate_pdf_report(df, 'output/report.pdf')
    print('Saved DB and PDF')
