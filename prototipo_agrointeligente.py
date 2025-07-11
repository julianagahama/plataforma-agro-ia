import streamlit as st

st.title("Plataforma Agro Inteligente")
st.write("Aqui você pode acompanhar análises de mercado, preços e previsões agrícolas usando IA.")

# Exemplo simples de entrada do usuário e exibição
preco_soja = st.number_input("Digite o preço atual da soja (R$ por saca):", min_value=0.0)
preco_milho = st.number_input("Digite o preço atual do milho (R$ por saca):", min_value=0.0)

if st.button("Analisar mercado"):
    if preco_soja > preco_milho:
        st.success("A soja está com preço melhor para venda no momento.")
    else:
        st.success("O milho está com preço melhor para venda no momento.")
