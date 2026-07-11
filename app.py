import streamlit as st
from database import repo
from fpdf import FPDF

def gerar_pdf_vistoria(nome, marca, nota, valor):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Laudo de Avaliação - VERIS SIMP", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Modelo: {nome}", ln=True)
    pdf.cell(200, 10, f"Marca: {marca}", ln=True)
    pdf.cell(200, 10, f"Nota da Vistoria: {nota}", ln=True)
    pdf.cell(200, 10, f"Valor Precificado: R$ {valor:,.2f}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

st.set_page_config(page_title="VERIS SIMP", layout="centered")
st.title("🎯 VERIS SIMP")

tab1, tab2 = st.tabs(["📊 Precificar", "➕ Cadastrar"])

with tab1:
    modelos = repo.listar_modelos()
    opcoes = {f"{m['marca']} - {m['nome_completo']}": m for m in modelos}
    selecionado = st.selectbox("Buscar Modelo:", options=list(opcoes.keys()))
    
    m = opcoes[selecionado]
    nota = st.slider("Nota da Vistoria (1-5)", 1, 5, 5)
    valor = repo.calcular_valor_por_nota(m['valor_base'], nota)
    
    st.metric("Valor Precificado", f"R$ {valor:,.2f}")
    st.download_button("📥 Baixar Laudo PDF", gerar_pdf_vistoria(m['nome_completo'], m['marca'], nota, valor), f"Laudo_{m['crlv']}.pdf", "application/pdf")

with tab2:
    with st.form("c"):
        m_c = st.text_input("Marca")
        c_c = st.text_input("CRLV")
        n_c = st.text_input("Nome")
        v_c = st.number_input("Valor Base")
        if st.form_submit_button("Salvar"):
            repo.salvar_modelo(m_c, c_c, n_c, v_c)
            st.success("Salvo!")
