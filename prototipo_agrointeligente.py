import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import requests
import time

st.title("Plataforma Agro Inteligente")
st.write("Aqui você pode acompanhar análises de mercado, preços, clima e previsões agrícolas usando IA.")

# Parte 1: Entrada manual e botão para comparar soja e milho
preco_soja = st.number_input("Digite o preço atual da soja (R$ por saca):", min_value=0.0, format="%.2f")
preco_milho = st.number_input("Digite o preço atual do milho (R$ por saca):", min_value=0.0, format="%.2f")

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

    # Média móvel protegida
    media_movel_soja = None
    media_movel_milho = None

    try:
        media_movel_soja = dados_soja['Close'].rolling(window=7).mean().iloc[-1]
    except Exception:
        pass

    try:
        media_movel_milho = dados_milho['Close'].rolling(window=7).mean().iloc[-1]
    except Exception:
        pass

    if media_movel_soja is not None and pd.notna(media_movel_soja):
        st.write(f"Média móvel dos últimos 7 dias - Soja: {media_movel_soja:.2f}")
    else:
        st.warning("Não foi possível calcular a média móvel para soja.")

    if media_movel_milho is not None and pd.notna(media_movel_milho):
        st.write(f"Média móvel dos últimos 7 dias - Milho: {media_movel_milho:.2f}")
    else:
        st.warning("Não foi possível calcular a média móvel para milho.")

    # Análise de tendência simples, só se médias existirem
    tendencia_soja = "indefinida"
    tendencia_milho = "indefinida"

    if media_movel_soja is not None and pd.notna(media_movel_soja) and not dados_soja['Close'].empty:
        try:
            if media_movel_soja > dados_soja['Close'].iloc[-1]:
                tendencia_soja = "queda"
            else:
                tendencia_soja = "alta"
        except Exception:
            tendencia_soja = "indefinida"

    if media_movel_milho is not None and pd.notna(media_movel_milho) and not dados_milho['Close'].empty:
        try:
            if media_movel_milho > dados_milho['Close'].iloc[-1]:
                tendencia_milho = "queda"
            else:
                tendencia_milho = "alta"
        except Exception:
            tendencia_milho = "indefinida"

    st.write(f"Tendência da Soja: {tendencia_soja}")
    st.write(f"Tendência do Milho: {tendencia_milho}")

    # Recomendação final simples
    if tendencia_soja == "alta" and tendencia_milho == "queda":
        st.success("Recomendação automática: venda soja, espere o milho.")
    elif tendencia_milho == "alta" and tendencia_soja == "queda":
        st.success("Recomendação automática: venda milho, espere a soja.")
    elif "indefinida" in (tendencia_soja, tendencia_milho):
        st.info("Recomendação automática: dados insuficientes para análise.")
    else:
        st.info("Recomendação automática: aguarde confirmação de mercado.")

st.write("---")

# Parte 3: Consulta do clima via OpenWeather API

def obter_clima(cidade, chave_api):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={chave_api}&units=metric&lang=pt_br"
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()  # Lança erro para códigos HTTP ruins
        dados = resposta.json()

        if dados.get("cod") != 200:
            return None, f"Erro da API: {dados.get('message', 'Cidade não encontrada')}"

        temp = dados['main']['temp']
        descricao = dados['weather'][0]['description']
        return f"{temp}ºC, {descricao}", None
    except requests.exceptions.RequestException as e:
        return None, f"Erro ao conectar à API do clima: {str(e)}"

st.subheader("Consulta do Clima")

cidade_usuario = st.text_input("Digite a cidade para ver o clima:")

sua_chave_api = "4fb243378fa31424203528547e3c3f3a"  # sua chave

if cidade_usuario:
    clima, erro = obter_clima(cidade_usuario, sua_chave_api)
    if erro:
        st.error(f"Não foi possível obter informações climáticas: {erro}")
    else:
        st.write(f"Clima atual em {cidade_usuario}: {clima}")


