Projeto: Monitoramento de Preços de Produtos

Objetivo
- Implementar pipeline ETL para coletar preços de múltiplas fontes e treinar modelos para identificar tendências de aumento/queda.

Arquivos principais
- `proposta_professor.md` - proposta enviada ao professor
- `pipeline.py` - runner de amostra que executa extrações e junta dados
- `etl/` - scripts de extração:
  - `extract_api.py` (MercadoLibre exemplo)
  - `extract_csv.py`
  - `extract_web.py`
  - `extract_pdf.py`
  - `utils.py`

Instalação
```bash
pip install -r requirements.txt
```

Execução de teste
```bash
python pipeline.py
```

Próximos passos
- Implementar rotinas de limpeza/normalização mais robustas
- Agendamento (cron/airflow) para coleta diária
- Treinamento de modelos e geração de relatórios (Excel/PDF/DB)
- Interface com Streamlit
