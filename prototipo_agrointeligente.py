import streamlit as st
import yfinance as yf
import pandas as pd

st.title("Plataforma Agro Inteligente")
st.write("Análises automáticas com dados reais.")

# Baixar dados históricos da soja e do milho
# Códigos do Yahoo Finance: Soja (ZS=F), Milho (ZC=F)

preco_soja_df = yf.download('ZS=F', period='1mo', interval='1d')
preco_milho_df = yf.download('ZC=F', period='1mo', interval='1d')

st.write("Preços históricos soja (último mês):")
st.dataframe(preco_soja_df[['Close']])

st.write("Preços históricos milho (último mês):")
st.dataframe(preco_milho_df[['Close']])

# Mostrar último preço de fechamento
ultimo_preco_soja = preco_soja_df['Close'][-1]
ultimo_preco_milho = preco_milho_df['Close'][-1]

st.write(f"Último preço soja: R$ {ultimo_preco_soja:.2f}")
st.write(f"Último preço milho: R$ {ultimo_preco_milho:.2f}")

# Análise simples
if ultimo_preco_soja > ultimo_preco_milho:
    st.success("Soja está com preço melhor para venda no momento.")
else:
    st.success("Milho está com preço melhor para venda no momento.")
