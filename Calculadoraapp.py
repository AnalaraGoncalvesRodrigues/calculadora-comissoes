import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF

# Configuração inicial
st.set_page_config(page_title="Dashboard Grupo Gonçalves", page_icon="🏢", layout="wide")

# Logo e título
st.image("https://widesysw1489.s3.sa-east-1.amazonaws.com/images/logo-site.png", width=180)
st.markdown("<h2 style='text-align:center; color:#2E4053;'>📊 Painel de Controle - Grupo Gonçalves</h2>", unsafe_allow_html=True)
st.markdown("---")

# Lista inicial de corretores
if "corretores" not in st.session_state:
    st.session_state.corretores = ["Isabela", "Rovilson", "Telma", "Denise"]

# Menu lateral
menu = st.sidebar.radio("Navegação", ["Visão Geral", "Atendimentos", "Visitas", "Propostas", "Calculadora", "Gerenciar Corretores", "Regras"])

# --- Dados fictícios (pode depois puxar de Excel/BD) ---
dados = pd.DataFrame({
    "Corretor": ["Isabela", "Rovilson", "Telma", "Denise"],
    "Atendimentos": [12, 18, 9, 14],
    "Visitas": [5, 7, 3, 6],
    "Propostas": [2, 3, 1, 2],
    "Comissão": [3200, 4700, 1800, 2500]
})

# --- Página Visão Geral ---
if menu == "Visão Geral":
    st.subheader("📈 Resumo Geral")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total de Atendimentos", dados["Atendimentos"].sum())
        st.metric("Total de Visitas", dados["Visitas"].sum())

    with col2:
        st.metric("Total de Propostas", dados["Propostas"].sum())
        st.metric("Total de Comissões (R$)", dados["Comissão"].sum())

    st.markdown("### Gráfico de Comissões por Corretor")
    fig = px.bar(dados, x="Corretor", y="Comissão", color="Corretor", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# --- Página Atendimentos ---
elif menu == "Atendimentos":
    st.subheader("📞 Atendimentos")
    st.dataframe(dados[["Corretor", "Atendimentos"]])

# --- Página Visitas ---
elif menu == "Visitas":
    st.subheader("🏠 Visitas")
    st.dataframe(dados[["Corretor", "Visitas"]])

# --- Página Propostas ---
elif menu == "Propostas":
    st.subheader("📝 Propostas")
    st.dataframe(dados[["Corretor", "Propostas"]])

# --- Página Calculadora ---
elif menu == "Calculadora":
    st.subheader("💰 Calculadora de Comissões")

    corretor = st.selectbox("Selecione o corretor", st.session_state.corretores)
    tipo = st.radio("Tipo de negociação", ["Venda", "Locação"])
    valor = st.number_input("Valor do imóvel/aluguel", min_value=0.0, step=100.0)

    captador = st.checkbox("Captador")
    negociador = st.checkbox("Negociador")

    if st.button("Calcular"):
        comissao_imobiliaria = 0
        comissao_corretor = 0

        if tipo == "Venda":
            comissao_imobiliaria = valor * 0.06
            if captador:
                comissao_corretor += comissao_imobiliaria * 0.10
            if negociador:
                comissao_corretor += comissao_imobiliaria * 0.35
        else:  # Locação
            comissao_imobiliaria = valor
            if captador:
                comissao_corretor += comissao_imobiliaria * 0.15
            if negociador:
                comissao_corretor += comissao_imobiliaria * 0.30

        # Exibir resultados
        st.info(f"💵 Valor total considerado: R$ {valor:.2f}")
        st.success(f"🏢 Imobiliária: R$ {comissao_imobiliaria - comissao_corretor:.2f}")
        st.success(f"👤 Corretor ({corretor}): R$ {comissao_corretor:.2f}")

        # PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "Resumo da Comissão", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, f"Corretor: {corretor}", ln=True)
        pdf.cell(200, 10, f"Tipo de negociação: {tipo}", ln=True)
        pdf.cell(200, 10, f"Valor: R$ {valor:.2f}", ln=True)
        pdf.cell(200, 10, f"Imobiliária: R$ {comissao_imobiliaria - comissao_corretor:.2f}", ln=True)
        pdf.cell(200, 10, f"Corretor ({corretor}): R$ {comissao_corretor:.2f}", ln=True)

        pdf_file = "resumo_comissao.pdf"
        pdf.output(pdf_file)

        with open(pdf_file, "rb") as file:
            st.download_button("📥 Baixar PDF", file, file_name=pdf_file, mime="application/pdf")

# --- Página Gerenciar Corretores ---
elif menu == "Gerenciar Corretores":
    st.subheader("👥 Gerenciar Corretores")

    novo = st.text_input("Adicionar novo corretor:")
    if st.button("Adicionar"):
        if novo and novo not in st.session_state.corretores:
            st.session_state.corretores.append(novo)
            st.success(f"Corretor {novo} adicionado com sucesso!")

    remover = st.selectbox("Remover corretor:", st.session_state.corretores)
    if st.button("Remover"):
        st.session_state.corretores.remove(remover)
        st.success(f"Corretor {remover} removido com sucesso!")

    st.write("Corretores atuais:", st.session_state.corretores)

# --- Página Regras ---
elif menu == "Regras":
    st.subheader("📘 Regras de Comissão")
    st.write("""
    ### Locação
    - Captador: **15%** do valor do 1º aluguel (100% vai para a imobiliária).  
    - Negociador: **30%** do valor do 1º aluguel.

    ### Venda
    - Comissão da imobiliária: **6%** sobre o valor do imóvel.  
    - Captador: **10%** da comissão da imobiliária.  
    - Negociador: **35%** da comissão da imobiliária.
    """)
