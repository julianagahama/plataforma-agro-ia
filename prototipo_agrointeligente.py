import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("Plataforma Agro Inteligente")
st.write("Aqui você pode acompanhar análises de mercado, preços e previsões agrícolas usando IA.")

# Parte 1: Entrada manual e botão para comparar soja e milho
preco_soja = st.number_input("Digite o preço atual da soja (R$ por saca):", min_value=0.0)
preco_milho = st.number_input("Digite o preço atual do milho (R$ por saca):", min_value=0.0)

if st.button("Analisar mercado manual"):
    if preco_soja > preco_milho:
        st.success("A soja está com preço melhor para venda no momento.")
    elif preco_milho > preco_soja:
        st.success("O milho está com preço melhor para venda no momento.")
    else:
        st.info("Os preços da soja e milho estão iguais.")

st.write("---")

# Parte 2: Análise automática com dados históricos (usando yfinance)

codigo_soja = "ZS=F"  # Soja futuro
codigo_milho = "ZC=F"  # Milho futuro

dados_soja = yf.download(codigo_soja, period="60d")
dados_milho = yf.download(codigo_milho, period="60d")

st.subheader("Análise automática com dados históricos")

if dados_soja.empty or dados_milho.empty:
    st.error("Erro ao baixar dados históricos. Tente novamente mais tarde.")
else:
    fig, ax = plt.subplots(2, 1, figsize=(10,6), sharex=True)

    ax[0].plot(dados_soja.index, dados_soja['Close'], label='Soja (Futuro)')
    ax[0].set_ylabel('Preço fechamento')
    ax[0].legend()
    ax[0].grid(True)

    ax[1].plot(dados_milho.index, dados_milho['Close'], label='Milho (Futuro)', color='orange')
    ax[1].set_ylabel('Preço fechamento')
    ax[1].legend()
    ax[1].grid(True)

    st.pyplot(fig)

    # Cálculo seguro da média móvel dos últimos 7 dias
    try:
        media_movel_soja = dados_soja['Close'].rolling(window=7).mean().iloc[-1]
        st.write(f"Média móvel dos últimos 7 dias - Soja: {media_movel_soja:.2f}")
    except Exception:
        media_movel_soja = None
        st.warning("Não foi possível calcular a média móvel da soja por dados insuficientes.")

    try:
        media_movel_milho = dados_milho['Close'].rolling(window=7).mean().iloc[-1]
        st.write(f"Média móvel dos últimos 7 dias - Milho: {media_movel_milho:.2f}")
    except Exception:
        media_movel_milho = None
        st.warning("Não foi possível calcular a média móvel do milho por dados insuficientes.")

    # Análise simples de tendência com base na média móvel
    if media_movel_soja is not None:
        if media_movel_soja > dados_soja['Close'].iloc[-1]:
            tendencia_soja = "queda"
        else:
            tendencia_soja = "alta"
        st.write(f"Tendência da Soja: {tendencia_soja}")
    else:
        tendencia_soja = None

    if media_movel_milho is not None:
        if media_movel_milho > dados_milho['Close'].iloc[-1]:
            tendencia_milho = "queda"
        else:
            tendencia_milho = "alta"
        st.write(f"Tendência do Milho: {tendencia_milho}")
    else:
        tendencia_milho = None

    # Recomendação automática com base nas tendências
    if tendencia_soja == "alta" and tendencia_milho == "queda":
        st.success("Recomendação automática: venda soja, espere o milho.")
    elif tendencia_milho == "alta" and tendencia_soja == "queda":
        st.success("Recomendação automática: venda milho, espere a soja.")
    elif tendencia_soja is None or tendencia_milho is None:
        st.info("Recomendação automática indisponível por dados insuficientes.")
    else:
        st.info("Recomendação automática: aguarde confirmação de mercado.")

