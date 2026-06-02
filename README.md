# Monitoramento de Preços de Produtos

Pipeline ETL para coletar preços de múltiplas fontes, treinar modelos de Machine Learning para identificar tendências de aumento/queda, e visualizar resultados via dashboard Streamlit.

## Estrutura do projeto

```
.
├── pipeline.py              # Executa o pipeline ETL completo
├── app.py                   # Dashboard Streamlit com gráficos e previsões
├── convert_proposal.py      # Converte proposta (.md → .docx, .pdf)
├── create_presentation.py   # Gera apresentação PowerPoint (.pptx)
├── requirements.txt         # Dependências do projeto
├── sample_prices.csv        # Dados de exemplo (fallback)
│
├── etl/
│   ├── extract_api.py       # Extração de API (AwesomeAPI — cotações)
│   ├── extract_csv.py       # Extração de arquivo CSV
│   ├── extract_web.py       # Web scraping (MercadoLibre)
│   ├── extract_pdf.py       # Extração de tabelas de PDF
│   ├── transform.py         # Limpeza e normalização dos dados
│   ├── load.py              # Persistência (SQLite + PDF report)
│   ├── train_model.py       # Treinamento de modelos (regressão + classificação)
│   └── utils.py             # Utilitários (parse_price, unify_columns)
│
├── models/                  # Modelos treinados (.pkl)
├── output/                  # Dados processados (CSV, XLSX, SQLite, PDF)
├── tests/                   # Testes automatizados
└── proposta_professor.*     # Proposta acadêmica em múltiplos formatos
```

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

### Pipeline ETL (coleta + processamento)

```bash
python pipeline.py
```

Extrai dados de 3 fontes:
- **API**: AwesomeAPI (cotações de USD, EUR, GBP, ARS, CAD, AUD em BRL)
- **CSV**: `sample_prices.csv` (dados de produtos)
- **Web scraping**: MercadoLibre (pode falhar devido a bloqueios — pipeline segue)
- **PDF**: `folheto.pdf` (se existir)

Gera em `output/`: `combined_prices.csv`, `combined_prices.xlsx`, `prices.db`, `report.pdf`

### Treinar modelos

```bash
python etl/train_model.py
```

Treina:
- **Regressor** (`models/price_regressor.pkl`) — prevê o próximo preço
- **Classifier** (`models/price_classifier.pkl`) — classifica tendência (subida/estável/queda)

### Dashboard Streamlit

```bash
streamlit run app.py
```

Funcionalidades:
- Seleção de produto e lojas
- Série temporal com média móvel
- Previsão do próximo preço
- Classificação de tendência
- Exportação de dados e gráficos
- Botão para executar o pipeline

### Testes

```bash
pytest tests/ -v
```

## Fontes de dados

| Fonte | Tipo | Status |
|---|---|---|
| AwesomeAPI (cotações) | API | Funcionando |
| `sample_prices.csv` | CSV | 6 produtos de exemplo |
| MercadoLibre | Web scraping | Bloqueado (Cloudflare) |
| `folheto.pdf` | PDF | Se existir |

## Próximos passos

- Agendamento (cron/Airflow) para coleta diária
- Autenticação na API do MercadoLibre para acesso oficial
- Deployment do Streamlit em nuvem
- Mais features preditivas (sazonalidade, séries temporais)
