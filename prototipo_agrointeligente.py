import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import time

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

def baixar_dados(ticker, periodo="90d", tentativas=3):
    for tentativa in range(tentativas):
        try:
            dados = yf.download(ticker, period=periodo, auto_adjust=True)
            if not dados.empty:
                dados = dados.interpolate(method='linear').ffill().bfill()
                return dados
        except Exception:
            if tentativa < tentativas - 1:
                time.sleep(2)
            else:
                return pd.DataFrame()
    return pd.DataFrame()

dados_soja = baixar_dados(codigo_soja)
dados_milho = baixar_dados(codigo_milho)

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

    # Cálculo da média móvel protegido
    try:
        media_movel_soja = dados_soja['Close'].rolling(window=7).mean().iloc[-1]
    except Exception:
        media_movel_soja = None

    try:
        media_movel_milho = dados_milho['Close'].rolling(window=7).mean().iloc[-1]
    except Exception:
        media_movel_milho = None

    if media_movel_soja is not None:
        st.write(f"Média móvel dos últimos 7 dias - Soja: {media_movel_soja:.2f}")
    else:
        st.warning("Não foi possível calcular a média móvel para soja.")

    if media_movel_milho is not None:
        st.write(f"Média móvel dos últimos 7 dias - Milho: {media_movel_milho:.2f}")
    else:
        st.warning("Não foi possível calcular a média móvel para milho.")

    # Análise de tendência simples, só se as médias existirem
    if media_movel_soja is not None and not dados_soja['Close'].empty:
        if media_movel_soja > dados_soja['Close'].iloc[-1]:
            tendencia_soja = "queda"
        else:
            tendencia_soja = "alta"
    else:
        tendencia_soja = "indefinida"

    if media_movel_milho is not None and not dados_milho['Close'].empty:
        if media_movel_milho > dados_milho['Close'].iloc[-1]:
            tendencia_milho = "queda"
        else:
            tendencia_milho = "alta"
    else:
        tendencia_milho = "indefinida"

    st.write(f"Tendência da Soja: {tendencia_soja}")
    st.write(f"Tendência do Milho: {tendencia_milho}")

    # Recomendação final simples
    if tendencia_soja == "alta" and tendencia_milho == "queda":
        st.success("Recomendação automática: venda soja, espere o milho.")
    elif tendencia_milho == "alta" and tendencia_soja == "queda":
        st.success("Recomendação automática: venda milho, espere a soja.")
    elif tendencia_soja == "indefinida" or tendencia_milho == "indefinida":
        st.info("Recomendação automática: dados insuficientes para análise.")
    else:
        st.info("Recomendação automática: aguarde confirmação de mercado.")

