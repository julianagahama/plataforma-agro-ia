import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Agro Inteligente", layout="centered")
st.title("🌾 Plataforma Agro Inteligente")
st.write("Acompanhe os preços da soja e do milho com análises automáticas.")

# Entrada manual
preco_soja = st.number_input("Digite o preço atual da soja (R$/saca):", min_value=0.0)
preco_milho = st.number_input("Digite o preço atual do milho (R$/saca):", min_value=0.0)

if st.button("Comparar preços"):
    if preco_soja > preco_milho:
        st.success("📈 Soja está mais valorizada.")
    elif preco_milho > preco_soja:
        st.success("📈 Milho está mais valorizado.")
    else:
        st.info("🔍 Os dois estão com o mesmo valor.")

st.write("---")

# Baixar dados
def carregar_dados(ticker):
    try:
        df = yf.download(ticker, period="90d", progress=False)
        if not df.empty:
            df = df.interpolate(method="linear").ffill().bfill()
        return df
    except:
        return pd.DataFrame()

df_soja = carregar_dados("ZS=F")
df_milho = carregar_dados("ZC=F")

# Verificar se os dados foram carregados
if df_soja.empty or df_milho.empty:
    st.error("Erro ao carregar dados de mercado. Tente novamente mais tarde.")
else:
    # Gráfico
    fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    ax[0].plot(df_soja.index, df_soja["Close"], label="Soja")
    ax[1].plot(df_milho.index, df_milho["Close"], label="Milho", color="orange")
    ax[0].legend(); ax[1].legend()
    ax[0].grid(); ax[1].grid()
    st.pyplot(fig)

    # Médias móveis
    def calcular_media_movel(df):
        if df.shape[0] >= 7:
            return df['Close'].rolling(window=7).mean().iloc[-1]
        return None

    media_soja = calcular_media_movel(df_soja)
    media_milho = calcular_media_movel(df_milho)
    preco_atual_soja = df_soja['Close'].iloc[-1]
    preco_atual_milho = df_milho['Close'].iloc[-1]

    if media_soja:
        st.write(f"Média móvel 7 dias (Soja): R$ {media_soja:.2f}")
    else:
        st.warning("Sem dados suficientes para calcular a média da soja.")

    if media_milho:
        st.write(f"Média móvel 7 dias (Milho): R$ {media_milho:.2f}")
    else:
        st.warning("Sem dados suficientes para calcular a média do milho.")

    # Tendência
    def tendencia(preco_atual, media):
        if media and preco_atual:
            return "alta" if preco_atual > media else "queda"
        return "indefinida"

    tendencia_soja = tendencia(preco_atual_soja, media_soja)
    tendencia_milho = tendencia(preco_atual_milho, media_milho)

    st.write(f"Tendência Soja: {tendencia_soja}")
    st.write(f"Tendência Milho: {tendencia_milho}")

    # Recomendação
    if tendencia_soja == "alta" and tendencia_milho == "queda":
        st.success("✅ Recomendação: Venda soja, espere o milho.")
    elif tendencia_milho == "alta" and tendencia_soja == "queda":
        st.success("✅ Recomendação: Venda milho, espere a soja.")
    elif "indefinida" in (tendencia_soja, tendencia_milho):
        st.info("ℹ️ Dados insuficientes para recomendação.")
    else:
        st.info("ℹ️ Aguarde movimentação mais clara do mercado.")

