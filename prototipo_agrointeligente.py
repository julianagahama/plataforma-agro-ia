import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("Plataforma Agro Inteligente")
st.write("Aqui você pode acompanhar análises de mercado, preços e previsões agrícolas usando IA.")

# Entrada manual para análise simples
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
st.subheader("Análise automática com dados históricos")

# Tickers e download
codigo_soja = "ZS=F"
codigo_milho = "ZC=F"

dados_soja = yf.download(codigo_soja, period="60d")
dados_milho = yf.download(codigo_milho, period="60d")

if dados_soja.empty or dados_milho.empty:
    st.error("Erro ao baixar dados históricos. Tente novamente mais tarde.")
else:
    # Gráficos
    fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    ax[0].plot(dados_soja.index, dados_soja['Close'], label='Soja (Futuro)', color='green')
    ax[0].set_ylabel('Preço Fechamento')
    ax[0].legend()
    ax[0].grid(True)

    ax[1].plot(dados_milho.index, dados_milho['Close'], label='Milho (Futuro)', color='orange')
    ax[1].set_ylabel('Preço Fechamento')
    ax[1].legend()
    ax[1].grid(True)

    st.pyplot(fig)

    # Média móvel com segurança
    if len(dados_soja['Close'].dropna()) >= 7 and len(dados_milho['Close'].dropna()) >= 7:
        media_movel_soja = dados_soja['Close'].rolling(window=7).mean().iloc[-1]
        media_movel_milho = dados_milho['Close'].rolling(window=7).mean().iloc[-1]

        st.write(f"Média móvel dos últimos 7 dias - Soja: {media_movel_soja:.2f}")
        st.write(f"Média móvel dos últimos 7 dias - Milho: {media_movel_milho:.2f}")

        # Tendência
        if media_movel_soja > dados_soja['Close'].iloc[-1]:
            tendencia_soja = "queda"
        else:
            tendencia_soja = "alta"

        if media_movel_milho > dados_milho['Close'].iloc[-1]:
            tendencia_milho = "queda"
        else:
            tendencia_milho = "alta"

        st.write(f"Tendência da Soja: {tendencia_soja}")
        st.write(f"Tendência do Milho: {tendencia_milho}")

        # Recomendação
        if tendencia_soja == "alta" and tendencia_milho == "queda":
            st.success("Recomendação: vender soja, esperar milho.")
        elif tendencia_milho == "alta" and tendencia_soja == "queda":
            st.success("Recomendação: vender milho, esperar soja.")
        else:
            st.info("Recomendação: aguarde confirmação do mercado.")
    else:
        st.warning("Não foi possível calcular a média móvel — dados insuficientes.")
