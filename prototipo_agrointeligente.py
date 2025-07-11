import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("Plataforma Agro Inteligente")
st.write("Acompanhe análises de mercado, preços e previsões agrícolas com auxílio de IA.")

# Parte 1 – Entrada manual
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

# Parte 2 – Análise automática com dados históricos
codigo_soja = "ZS=F"  # Soja futuro
codigo_milho = "ZC=F"  # Milho futuro

dados_soja = yf.download(codigo_soja, period="30d")
dados_milho = yf.download(codigo_milho, period="30d")

st.subheader("Análise automática com dados históricos")

if dados_soja.empty or dados_milho.empty:
    st.error("Erro ao baixar dados históricos. Tente novamente mais tarde.")
else:
    fig, ax = plt.subplots(2, 1, figsize=(10,6), sharex=True)

    ax[0].plot(dados_soja.index, dados_soja['Close'], label='Soja (Futuro)')
    ax[0].set_ylabel('Preço de Fechamento')
    ax[0].legend()
    ax[0].grid(True)

    ax[1].plot(dados_milho.index, dados_milho['Close'], label='Milho (Futuro)', color='orange')
    ax[1].set_ylabel('Preço de Fechamento')
    ax[1].legend()
    ax[1].grid(True)

    st.pyplot(fig)

    # Cálculo da média móvel
    media_movel_soja = dados_soja['Close'].rolling(window=7).mean().iloc[-1]
    media_movel_milho = dados_milho['Close'].rolling(window=7).mean().iloc[-1]

    st.write(f"Média móvel dos últimos 7 dias - Soja: {media_movel_soja:.2f}")
    st.write(f"Média móvel dos últimos 7 dias - Milho: {media_movel_milho:.2f}")

    # Tendência pela média móvel
    if media_movel_soja > dados_soja['Close'].iloc[-1]:
        tendencia_soja = "queda"
    else:
        tendencia_soja = "alta"

    if media_movel_milho > dados_milho['Close'].iloc[-1]:
        tendencia_milho = "queda"
    else:
        tendencia_milho = "alta"

    # 🔍 NOVO BLOCO – Resumo de mercado textual
    st.subheader("Resumo da Análise de Mercado")

    var_soja = ((dados_soja['Close'].iloc[-1] - dados_soja['Close'].iloc[-7]) / dados_soja['Close'].iloc[-7]) * 100
    var_milho = ((dados_milho['Close'].iloc[-1] - dados_milho['Close'].iloc[-7]) / dados_milho['Close'].iloc[-7]) * 100

    def analise_textual(nome, variacao, tendencia):
        if variacao > 2:
            movimento = "forte alta"
        elif variacao < -2:
            movimento = "forte queda"
        else:
            movimento = "estabilidade"
        return f"O mercado da {nome} apresentou uma {movimento} nos últimos 7 dias, com variação de {variacao:.2f}%. A tendência atual é de {tendencia}."

    texto_soja = analise_textual("soja", var_soja, tendencia_soja)
    texto_milho = analise_textual("milho", var_milho, tendencia_milho)

    st.write("📈 " + texto_soja)
    st.write("🌽 " + texto_milho)

    # Resultado final
    st.write(f"Tendência da Soja: {tendencia_soja}")
    st.write(f"Tendência do Milho: {tendencia_milho}")

    if tendencia_soja == "alta" and tendencia_milho == "queda":
        st.success("Recomendação: venda soja, espere o milho.")
    elif tendencia_milho == "alta" and tendencia_soja == "queda":
        st.success("Recomendação: venda milho, espere a soja.")
    else:
        st.info("Recomendação: aguarde confirmação do mercado.")


