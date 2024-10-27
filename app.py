import pandas as pd
import yfinance as yf
import datetime as dt
import streamlit as st

# Configuração da página do Streamlit
st.set_page_config(page_title="Agregador de Investimentos", page_icon=None, layout="wide")

st.title("Investor Bee")


end_date = dt.datetime.today()
start_date = dt.datetime(end_date.year - 1, end_date.month, end_date.day)

# Container para inputs do usuário
with st.container():
    st.header("Preencha as informações:")
    ativo = st.selectbox("Selecione o ativo desejado:", options=['PETR4.SA', 'VALE3.SA', 'MGLU3.SA', 'ITSA4.SA'])
    data_inicial = st.date_input('Selecione a Data Inicial:', start_date)
    data_final = st.date_input('Selecione a Data Final:', end_date)

# Retorna as informações da API
df = yf.download(tickers=ativo, start=data_inicial, end=data_final)

# Verifique se o DataFrame está vazio
if df.empty:
    st.error("Nenhum dado foi retornado. Verifique o ticker e as datas.")
else:
    # Verifique se o DataFrame possui um MultiIndex e extraia a camada correta
    if isinstance(df.columns, pd.MultiIndex):
        df = df.xs(ativo, level=1, axis=1)

    # Métricas
    ult_atualizacao = df.index.max()  # Data da última atualização
    ult_cotacao = round(df['Adj Close'].iloc[-1], 2)  # Última cotação ajustada
    menor_cotacao = round(df['Adj Close'].min(), 2)  # Menor cotação do período
    maior_cotacao = round(df['Adj Close'].max(), 2)  # Maior cotação do período
    prim_cotacao = round(df['Adj Close'].iloc[0], 2)  # Primeira cotação ajustada
    delta = round(((ult_cotacao - prim_cotacao) / prim_cotacao) * 100, 2) # Variação da cotação no período

    # Exibe as métricas
    with st.container():
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label=f"Última atualização - {ult_atualizacao.date()}", value=f"R$ {ult_cotacao:.2f}", delta=f"{delta:.2f}%")
        with col2:
            st.metric(label="Menor cotação do período", value=f"R$ {menor_cotacao:.2f}")
        with col3:
            st.metric(label="Maior cotação do período", value=f"R$ {maior_cotacao:.2f}")

    # Apresentação do DataFrame com gráficos
    with st.container():
        st.subheader("Visualização dos preços")
        
        # Gráfico de área para o fechamento ajustado
        st.area_chart(df['Adj Close'])

        # Gráfico de linha para preços mínimo, ajustado e máximo
        st.line_chart(df[['Low', 'Adj Close', 'High']])

