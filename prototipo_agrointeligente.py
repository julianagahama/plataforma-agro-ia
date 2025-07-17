import streamlit as st
import requests

st.subheader("Consulta do Clima")

cidade_usuario = st.text_input("Digite a cidade para ver o clima:")

sua_chave_api = "4fb243378fa31424203528547e3c3f3a"  # sua chave

def obter_clima(cidade, chave_api):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={chave_api}&units=metric&lang=pt_br"
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
        if dados.get("cod") != 200:
            return None, f"Erro da API: {dados.get('message', 'Cidade não encontrada')}"
        temp = dados['main']['temp']
        descricao = dados['weather'][0]['description']
        return f"{temp}ºC, {descricao}", None
    except requests.exceptions.RequestException as e:
        return None, f"Erro ao conectar à API do clima: {str(e)}"

if cidade_usuario:
    clima, erro = obter_clima(cidade_usuario, sua_chave_api)
    if erro:
        st.error(f"Não foi possível obter informações climáticas: {erro}")
    else:
        st.write(f"Clima atual em {cidade_usuario}: {clima}")
