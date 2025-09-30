import streamlit as st
from fpdf import FPDF

# Lista inicial de corretores
if "corretores" not in st.session_state:
    st.session_state.corretores = ["Isabela", "Rovilson", "Telma", "Denise"]

st.set_page_config(page_title="Calculadora de Comissões", page_icon="💰")

# --- Menu lateral ---
menu = st.sidebar.radio("Navegação", ["Calculadora", "Regras", "Gerenciar Corretores"])

# --- Página de regras ---
if menu == "Regras":
    st.title("📘 Regras de Comissão")
    st.subheader("Locação")
    st.write("""
    - Captador: **15%** do valor do 1º aluguel (100% vai para a imobiliária).  
    - Negociador: **30%** do valor do 1º aluguel.
    """)
    st.subheader("Venda")
    st.write("""
    - Comissão da imobiliária: **6%** sobre o valor do imóvel.  
    - Captador: **10%** da comissão da imobiliária.  
    - Negociador: **35%** da comissão da imobiliária.
    """)

# --- Página de gerenciamento ---
elif menu == "Gerenciar Corretores":
    st.title("👥 Gerenciar Corretores")

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

# --- Página principal (Calculadora) ---
else:
    st.title("💰 Calculadora de Comissões")

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

        st.success(f"Comissão da Imobiliária: R$ {comissao_imobiliaria:.2f}")
        st.success(f"Comissão do Corretor ({corretor}): R$ {comissao_corretor:.2f}")

        # --- Gerar PDF ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "Resumo da Comissão", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, f"Corretor: {corretor}", ln=True)
        pdf.cell(200, 10, f"Tipo de negociação: {tipo}", ln=True)
        pdf.cell(200, 10, f"Valor: R$ {valor:.2f}", ln=True)
        pdf.cell(200, 10, f"Comissão da imobiliária: R$ {comissao_imobiliaria:.2f}", ln=True)
        pdf.cell(200, 10, f"Comissão do corretor: R$ {comissao_corretor:.2f}", ln=True)

        pdf_file = "resumo_comissao.pdf"
        pdf.output(pdf_file)

        with open(pdf_file, "rb") as file:
            st.download_button("📥 Baixar PDF", file, file_name=pdf_file, mime="application/pdf")
