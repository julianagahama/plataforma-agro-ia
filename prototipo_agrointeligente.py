import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta

# ====== CONFIGURAÇÕES DE LOGIN SIMPLES ======
senha_correta = "agro123"

st.set_page_config(page_title="Plataforma Agro Inteligente", layout="centered")
st.title("🌾 Plataforma Agro Inteligente")

senha = st.text_input("🔐 Digite a senha para acessar:", type="password")

if senha != senha_correta:
    st.warning("Acesso restrito. Insira a senha correta.")
    st.stop()

st.success("✅ Acesso liberado!")

# ====== PARTE 1 - COLETANDO DADOS ======
st.subheader("📊 Preços Históricos - Soja e Milho")

# Datas para buscar dados
data_final = date.today()
data_inicial = data_final - timedelta(days=180)

# Dicionário de ativos
ativos = {
    "Soja (SOYB)": "SOYB",
    "Milho (CORN)": "CORN"
}

# Função para carregar os dados
@st.cache_data
def carregar_dados(ticker):
    dados = yf.download(ticker, start=data_inicial, end=data_final)
    return dados["Close"]

# Carregar e plotar os dados
dados_soja = carregar_dados(ativos["Soja (SOYB)"])
dados_milho = carregar_dados(ativos["Milho (CORN)"])

# Plotando os preços
fig, ax = plt.subplots()
dados_soja.plot(ax=ax, label="Soja (SOYB)", color='green')
dados_milho.plot(ax=ax, label="Milho (CORN)", color='orange')
ax.set_title("Preços dos últimos 6 meses")
ax.set_ylabel("Preço (USD)")
ax.legend()
st.pyplot(fig)

# ====== PARTE 2 - ANÁLISE DE TENDÊNCIA ======
st.subheader("🤖 Análise de Tendência")

def analisar_tendencia(dados, nome):
    variacao = dados[-1] - dados[0]
    if variacao > 0:
        return f"📈 Tendência de alta para {nome} (+{variacao:.2f} USD)"
    elif variacao < 0:
        return f"📉 Tendência de baixa para {nome} ({variacao:.2f} USD)"
    else:
        return f"⏸️ {nome} está estável."

st.write(analisar_tendencia(dados_soja, "Soja"))
st.write(analisar_tendencia(dados_milho, "Milho"))

# ====== PARTE 3 - OPINIÃO DE VENDA SIMPLES ======
st.subheader("📌 Recomendação Simplificada de Venda")

if dados_soja[-1] > dados_milho[-1]:
    st.info("💡 A Soja está com preço melhor atualmente.")
else:
    st.info("💡 O Milho está com preço melhor atualmente.")

