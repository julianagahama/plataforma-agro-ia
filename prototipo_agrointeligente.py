import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Plataforma Agro Inteligente", layout="centered")

st.title("🌾 Plataforma Agro Inteligente")
st.write("Acompanhe análises de mercado, preços e tendências agrícolas com apoio de inteligência de dados.")

# Parte 1: Entrada manual
st.header("📊 Comparação manual de preços")
preco_soja = st.number_input("Digite o preço atual da soja (R$ por saca):", min_value=0.0)
preco_milho = st.number_input("Digite o preço atual do milho (R$ por saca):", min_value=0.0)

if st.button("Analisar mercado manualmente"):
    if preco_soja > preco_milho:
        st.success("✅ A soja está com preço mais favorável para venda no momento.")
    elif preco_milho > preco_soja:
        st.success("✅ O milho está com preço mais favorável para venda no momento.")
    else:
        st.info("ℹ️ Os preços da soja e do milho estão iguais.")

st.markdown("---")

# Parte 2: Análise com dados históricos do yfinance
st.header("📈 Análise automática com dados históricos")

codigo_soja = "ZS=F"   # Soja futura
codigo_milho = "ZC=F"  # Milho futuro

dados_soja = yf.download(codigo_soja, period="30d")
dados_milho = yf.download(codigo_milho, period="30d")

if dados_soja.empty or dados_milho.empty:
    st.error("❌ Erro ao obter dados históricos. Verifique sua conexão ou tente novamente mais tarde.")
else:
    fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    ax[0].plot(dados_soja.index, dados_soja['Close'], label='Soja (Futuro)', color='green')
    ax[0].set_ylabel('Preço (USD)')
    ax[0].legend()
    ax[0].grid(True)

    ax[1].plot(dados_milho.index, dados_milho['Close'], label='Milho (Futuro)', color='orange')
    ax[1].set_ylabel('Preço (USD)')
    ax[1].legend()
    ax[1].grid(True)

    st.pyplot(fig)

    # Média móvel protegida com try/except
    try:
        media_movel_soja = dados_soja['Close'].rolling(window=7).mean().iloc[-1]
        st.write(f"Média móvel dos últimos 7 dias - Soja: **{media_movel_soja:.2f} USD**")
    except Exception:
        media_movel_soja = None
        st.warning("⚠️ Não foi possível calcular a média móvel da soja — dados insuficientes.")

    try:
        media_movel_milho = dados_milho['Close'].rolling(window=7).mean().iloc[-1]
        st.write(f"Média móvel dos últimos 7 dias - Milho: **{media_movel_milho:.2f} USD**")
    except Exception:
        media_movel_milho = None
        st.warning("⚠️ Não foi possível calcular a média móvel do milho — dados insuficientes.")

    # Análise de tendência
    if media_movel_soja is not None and not dados_soja['Close'].empty:
        if media_movel_soja > dados_soja['Close'].iloc[-1]:
            tendencia_soja = "📉 tendência de queda"
        else:
            tendencia_soja = "📈 tendência de alta"
        st.write(f"Tendência da Soja: {tendencia_soja}")
    else:
        st.info("Sem dados suficientes para tendência da soja.")

    if media_movel_milho is not None and not dados_milho['Close'].empty:
        if media_movel_milho > dados_milho['Close'].iloc[-1]:
            tendencia_milho = "📉 tendência de queda"
        else:
            tendencia_milho = "📈 tendência de alta"
        st.write(f"Tendência do Milho: {tendencia_milho}")
    else:
        st.info("Sem dados suficientes para tendência do milho.")

    # Recomendação automática
    if media_movel_soja and media_movel_milho:
        if tendencia_soja == "📈 tendência de alta" and tendencia_milho == "📉 tendência de queda":
            st.success("🔎 Recomendação: **venda soja, espere o milho**.")
        elif tendencia_milho == "📈 tendência de alta" and tendencia_soja == "📉 tendência de queda":
            st.success("🔎 Recomendação: **venda milho, espere a soja**.")
        else:
            st.info("🔎 Recomendação: **aguarde confirmação de mercado**.")

