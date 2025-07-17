import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import time
import requests

# --- Configurações iniciais ---
st.set_page_config(page_title="Plataforma Agro Inteligente", layout="centered")

st.title("Plataforma Agro Inteligente")
st.write("Acompanhe análises de mercado, clima e recomendações agrícolas usando IA.")

# --- Parte 1: Entrada manual ---
st.header("Comparativo Manual de Preços")
preco_soja = st.number_input("Digite o preço atual da soja (R$ por saca):", min_value=0.0)
preco_milho = st.number_input("Digite o preço atual do milho (R$ por saca):", min_value=0.0)

if st.button("Analisar mercado manual"):
    if preco_soja > preco_milho:
        st.success("A soja está com preço melhor para venda no momento.")
    elif preco_milho > preco_soja:
        st.success("O milho está com preço melhor para venda no momento.")
    else:
        st.info("Os preços da soja e milho estão iguais.")

# --- Parte 2: Clima por cidade ---
st.header("Clima na sua Região")
cidade = st.text_input("Digite o nome da sua cidade:")

if cidade:
    chave_api = "4fb243378fa31424203528547e3c3f3a"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={chave_api}&lang=pt_br&units=metric"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados_clima = resposta.json()
        clima = dados_clima['weather'][0]['description'].capitalize()
        temp = dados_clima['main']['temp']
        umidade = dados_clima['main']['humidity']
        st.write(f"**Condição atual:** {clima}")
        st.write(f"**Temperatura:** {temp} °C")
        st.write(f"**Umidade:** {umidade}%")
    else:
        st.warning("Não foi possível obter informações climáticas.")

# --- Parte 3: Análise automática de mercado ---
st.header("Análise Automática de Mercado")

codigo_soja = "ZS=F"
codigo_milho = "ZC=F"

def baixar_dados(ticker, periodo="90d", tentativas=3):
    for tentativa in range(tentativas):
        try:
            dados = yf.download(ticker, period=periodo, auto_adjust=True)
            if not dados.empty:
                return dados.interpolate(method='linear').ffill().bfill()
        except:
            time.sleep(2)
    return pd.DataFrame()

dados_soja = baixar_dados(codigo_soja)
dados_milho = baixar_dados(codigo_milho)

if dados_soja.empty or dados_milho.empty:
    st.error("Erro ao baixar dados históricos. Tente novamente mais tarde.")
else:
    fig, ax = plt.subplots(2, 1, figsize=(10,6), sharex=True)

    ax[0].plot(dados_soja.index, dados_soja['Close'], label='Soja (Futuro)')
    ax[0].set_ylabel('Preço Fechamento')
    ax[0].legend()
    ax[0].grid(True)

    ax[1].plot(dados_milho.index, dados_milho['Close'], label='Milho (Futuro)', color='orange')
    ax[1].set_ylabel('Preço Fechamento')
    ax[1].legend()
    ax[1].grid(True)

    st.pyplot(fig)

    # Médias móveis
    soja_close = dados_soja['Close']
    milho_close = dados_milho['Close']

    if len(soja_close) >= 7:
        media_soja = soja_close.rolling(window=7).mean().iloc[-1]
        st.write(f"Média móvel dos últimos 7 dias - Soja: {media_soja:.2f}")
    else:
        media_soja = None
        st.warning("Dados insuficientes para média móvel da soja.")

    if len(milho_close) >= 7:
        media_milho = milho_close.rolling(window=7).mean().iloc[-1]
        st.write(f"Média móvel dos últimos 7 dias - Milho: {media_milho:.2f}")
    else:
        media_milho = None
        st.warning("Dados insuficientes para média móvel do milho.")

    # Tendência
    if media_soja is not None:
        tendencia_soja = "alta" if media_soja <= soja_close.iloc[-1] else "queda"
        st.write(f"Tendência da Soja: {tendencia_soja}")
    else:
        tendencia_soja = "indefinida"

    if media_milho is not None:
        tendencia_milho = "alta" if media_milho <= milho_close.iloc[-1] else "queda"
        st.write(f"Tendência do Milho: {tendencia_milho}")
    else:
        tendencia_milho = "indefinida"

    # Recomendação
    st.subheader("Recomendação Automática")
    if tendencia_soja == "alta" and tendencia_milho == "queda":
        st.success("Recomendação: venda soja, espere o milho.")
    elif tendencia_milho == "alta" and tendencia_soja == "queda":
        st.success("Recomendação: venda milho, espere a soja.")
    elif "indefinida" in (tendencia_soja, tendencia_milho):
        st.info("Dados insuficientes para recomendação precisa.")
    else:
        st.info("Aguarde confirmação de tendências para melhor decisão.")

