Proposta de Projeto — Monitoramento de Preços de Produtos

Resumo
- Tema: Monitoramento de preços de produtos com IA para identificar tendências de aumento/queda.
- Objetivo: Implementar ciclo ETL (Extração, Transformação, Carga) a partir de múltiplas fontes, treinar modelos para prever tendências de preço e entregar relatórios/exportações para avaliação.

Produtos-alvo (exemplos)
- Arroz 5kg (marca genérica)
- Leite UHT 1L
- Óleo de soja 900ml
- Açúcar 1kg
- Gasolina (R$/litro)
- Smartphone (ex.: iPhone 14 128GB)

Fontes e métodos de extração (4+ fontes)
1. API (JSON)
   - Exemplo: MercadoLibre Search API
   - Endpoint exemplo: https://api.mercadolibre.com/sites/MLB/search?q=arroz
   - Método: requisições HTTP para obter listagens/ preços.
2. CSV histórico
   - Exemplo: Datasets públicos (Kaggle) com histórico de preços no varejo.
   - Método: download/ingest automático do arquivo CSV.
3. Web scraping (HTML)
   - Exemplos: páginas de varejistas (Magazine Luiza, Carrefour, Mercado Livre).
   - Método: scraping com seletores para extrair `product name`, `price`, `unit price`, `availability`.
   - URLs de exemplo: https://lista.mercadolivre.com.br/arroz, https://www.magazineluiza.com.br/busca/?q=arroz
4. PDFs (folhetos promocionais)
   - Exemplo: folhetos semanais de supermercados.
   - Método: baixar PDFs e extrair tabelas com `pdfplumber`/`tabula`.
(5. Opcional) DOCX: listas internas de preços — método: `python-docx`.

Esquema de dados unificado (campos principais)
- `product_id`, `product_name`, `brand`, `sku` (se disponível), `price`, `currency`, `unit`, `store`, `url`, `availability`, `extraction_date`, `source_type`.

Frequência de coleta
- APIs & scraping: diário.
- PDFs: semanal.
- CSV histórico: ingestão única + atualizações mensais (quando aplicável).

Transformação e limpeza (resumo)
- Normalizar nomes e unidades, converter moedas, tratar missing values, remover outliers e unificar SKUs/marcas.

Modelo de IA / ML
- Tarefas: (A) Classificação de tendência (subida/queda/estável) para horizontes de 7/14 dias; (B) Previsão de preço numérico.
- Algoritmos propostos: XGBoost/RandomForest (regressão/classificação), Prophet para séries temporais; ensemble se necessário.
- Métricas: Accuracy/F1 (classificação), MAE/RMSE (regressão).

Cargas (entregáveis) — mínimo 3
- Excel (.xlsx) com histórico e previsões.
- Banco de dados (SQLite local ou PostgreSQL) com tabela unificada.
- Relatório PDF ou Word gerado automaticamente com tabela de produtos e tendências.
- Dashboard/Interface: Streamlit app (visualização + execução do ETL) — exportável como HTML/Docker; possível export CSV para Power BI.

Considerações técnicas e éticas
- Respeitar `robots.txt` e termos de uso dos sites; priorizar APIs oficiais.
- Citar fontes nos relatórios; anonimizar dados sensíveis.

Próximo passo solicitado ao professor
- Aprovar o tema: "Monitoramento de preços de produtos — IA identifica tendências de aumento/queda".
- Após aprovação, será entregue um cronograma com URLs/arquivos finais, amostra de dados e o plano de implementação (código, ambiente e apresentação).

Contato
- Se aprovado, posso começar a implementar o pipeline ETL e a interface; deseja que eu gere também um arquivo pronto em Word/PDF para enviar ao professor?
