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

# Definir códigos (tickers) do yfinance para soja e milho (exemplo)
# Obs: nem sempre yfinance tem preços em R$ por saca, pode ser em dólar e contratos futuros
# Aqui vamos usar códigos genéricos e converter para demonstrar — você pode ajustar depois
codigo_soja = "ZS=F"  # Soja futuro
codigo_milho = "ZC=F"  # Milho futuro

# Baixar dados dos últimos 30 dias
dados_soja = yf.download(codigo_soja, period="30d")
dados_milho = yf.download(codigo_milho, period="30d")

st.subheader("Análise automática com dados históricos")

if dados_soja.empty or dados_milho.empty:
    st.error("Erro ao baixar dados históricos. Tente novamente mais tarde.")
else:
    # Mostrar gráficos dos preços de fechamento
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

  import math  # coloque no topo se ainda não estiver

# Cálculo simples: média móvel dos últimos 7 dias
media_movel_soja = dados_soja['Close'].rolling(window=7).mean().iloc[-1]
media_movel_milho = dados_milho['Close'].rolling(window=7).mean().iloc[-1]

if not math.isnan(media_movel_soja):
    st.write(f"Média móvel dos últimos 7 dias - Soja: {media_movel_soja:.2f}")
else:
    st.write("Média móvel dos últimos 7 dias - Soja: dados insuficientes")

if not math.isnan(media_movel_milho):
    st.write(f"Média móvel dos últimos 7 dias - Milho: {media_movel_milho:.2f}")
else:
    st.write("Média móvel dos últimos 7 dias - Milho: dados insuficientes")

# Análise simples: qual está com tendência de alta pela média móvel
if not math.isnan(media_movel_soja) and media_movel_soja > dados_soja['Close'].iloc[-1]:
    tendencia_soja = "queda"
else:
    tendencia_soja = "alta"

if not math.isnan(media_movel_milho) and media_movel_milho > dados_milho['Close'].iloc[-1]:
    tendencia_milho = "queda"
else:
    tendencia_milho = "alta"

st.write(f"Tendência da Soja: {tendencia_soja}")
st.write(f"Tendência do Milho: {tendencia_milho}")

# Recomendação final simples (exemplo)
if tendencia_soja == "alta" and tendencia_milho == "queda":
    st.success("Recomendação automática: venda soja, espere o milho.")
elif tendencia_milho == "alta" and tendencia_soja == "queda":
    st.success("Recomendação automática: venda milho, espere a soja.")
else:
    st.info("Recomendação automática: aguarde confirmação de mercado.")


