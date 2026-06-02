import os
import subprocess
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import joblib

DATA_PATHS = ['output/combined_prices.csv', 'sample_prices.csv']
MODEL_REG = 'models/price_regressor.pkl'
MODEL_CLF = 'models/price_classifier.pkl'

@st.cache_data
def load_data():
    for p in DATA_PATHS:
        if os.path.exists(p):
            df = pd.read_csv(p)
            if 'extraction_date' in df.columns:
                df['extraction_date'] = pd.to_datetime(df['extraction_date'])
            return df
    return pd.DataFrame()

@st.cache_data
def load_models():
    reg = clf = None
    if os.path.exists(MODEL_REG):
        reg = joblib.load(MODEL_REG)
    if os.path.exists(MODEL_CLF):
        clf = joblib.load(MODEL_CLF)
    return reg, clf

st.title('Monitoramento de Preços — Previsões')

st.markdown('App demo: carrega dados coletados, mostra série temporal e usa modelos treinados para prever tendência.')

df = load_data()
reg, clf = load_models()

if df.empty:
    st.warning('Nenhum dado encontrado. Rode o pipeline ou coloque um `combined_prices.csv` ou `sample_prices.csv` na pasta.')
else:
    st.sidebar.header('Filtros')
    products = sorted(df['product_name'].dropna().unique())
    product = st.sidebar.selectbox('Produto', products)
    stores = sorted(df['store'].dropna().unique()) if 'store' in df.columns else []
    selected_stores = st.sidebar.multiselect('Comparar lojas (selecione 1+)', stores, default=stores[:1])
    smoothing = st.sidebar.slider('Janela média móvel (dias)', min_value=1, max_value=14, value=3)
    show_rolling = st.sidebar.checkbox('Mostrar média móvel', value=True)

    df_prod = df[df['product_name'] == product].sort_values('extraction_date')
    compare_mode = False
    if selected_stores:
        df_prod = df_prod[df_prod['store'].isin(selected_stores)]
        compare_mode = st.sidebar.checkbox('Comparar lojas por série temporal', value=False)

    st.subheader(product)
    st.dataframe(df_prod[['extraction_date','price','store']].reset_index(drop=True))

    if not df_prod.empty:
        if compare_mode and selected_stores:
            fig = px.line(df_prod, x='extraction_date', y='price', color='store', markers=True,
                          title=f'Histórico de preço por loja — {product}')
            if show_rolling and smoothing > 1:
                df_roll = df_prod.groupby('store').apply(lambda g: g.set_index('extraction_date')['price'].rolling(smoothing).mean().reset_index())
                df_roll = df_roll.reset_index(level=0).rename(columns={'level_0':'store'})
                fig.add_traces(px.line(df_roll, x='extraction_date', y='price', color='store', line_dash_sequence=['dash']).data)
        else:
            fig = px.line(df_prod, x='extraction_date', y='price', markers=True, title=f'Histórico de preço — {product}')
            if show_rolling and smoothing > 1:
                df_prod['rolling'] = df_prod['price'].astype(float).rolling(smoothing).mean()
                fig.add_trace(px.line(df_prod, x='extraction_date', y='rolling').data[0])
        st.plotly_chart(fig, use_container_width=True)

        # prepare features from last rows (per selected stores, take latest overall)
        last = df_prod.sort_values('extraction_date').groupby('store').tail(4)
        # pick last available row across stores
        if not last.empty:
            last_row = last.sort_values('extraction_date').iloc[-1]
            # build simple feature vector using most recent values from product across store selection
            recent = df_prod.sort_values('extraction_date').tail(4)['price'].astype(float).tolist()
            price = recent[-1] if len(recent)>=1 else 0.0
            lag_1 = recent[-2] if len(recent)>1 else price
            lag_2 = recent[-3] if len(recent)>2 else price
            lag_3 = recent[-4] if len(recent)>3 else price
            X = np.array([[price, lag_1, lag_2, lag_3]])

            if reg is not None:
                try:
                    pred_price = reg.predict(X)[0]
                    st.metric('Previsão próximo preço', f'{pred_price:.2f}')
                except Exception as e:
                    st.error(f'Erro ao prever preço: {e}')
            else:
                st.info('Modelo de regressão não encontrado.')

            if clf is not None:
                try:
                    pred_trend = clf.predict(X)[0]
                    trend_map = {1:'Subida', 0:'Estável', -1:'Queda'}
                    st.metric('Tendência prevista', trend_map.get(pred_trend, str(pred_trend)))
                except Exception as e:
                    st.error(f'Erro ao prever tendência: {e}')
            else:
                st.info('Modelo de classificação não encontrado.')

        st.markdown('---')
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Executar pipeline (coleta + processamento)'):
                with st.spinner('Executando pipeline...'):
                    try:
                        subprocess.run(['python','pipeline.py'], check=True)
                        st.success('Pipeline executado. Recarregue a página para ver novos dados.')
                    except subprocess.CalledProcessError as e:
                        st.error(f'Pipeline falhou: {e}')
        with col2:
            tmp = 'output/combined_prices.csv'
            if os.path.exists(tmp):
                with open(tmp,'rb') as f:
                    st.download_button('Download CSV', f, file_name='combined_prices.csv')
            else:
                st.warning('Arquivo CSV não encontrado para download.')

        # download chart as PNG (requires kaleido)
        try:
            img_bytes = fig.to_image(format='png')
            st.download_button('Download gráfico (PNG)', data=img_bytes, file_name='chart.png', mime='image/png')
        except Exception:
            st.info('Para baixar o gráfico em PNG instale a dependência `kaleido`.')
    # Export plot HTML and CSV for current view
    st.markdown('### Exportar visualização')
    if not df_prod.empty:
        csv_bytes = df_prod.to_csv(index=False).encode('utf-8')
        st.download_button('Baixar dados filtrados (.csv)', data=csv_bytes, file_name=f'{product}_filtered.csv')
        try:
            html = fig.to_html(full_html=False)
            st.download_button('Baixar gráfico (HTML)', data=html, file_name=f'{product}_chart.html')
        except Exception:
            st.info('Exportação do gráfico não disponível.')
