import streamlit as st
from database import AgregadoRepository
from fpdf import FPDF

# --- Autenticação ---
def check_password():
    if "password_correct" not in st.session_state:
        st.text_input("Usuário", key="username")
        st.text_input("Senha", type="password", key="password")
        if st.button("Entrar"):
            if st.session_state["username"] == st.secrets["admin_user"] and st.session_state["password"] == st.secrets["admin_pass"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")
        return False
    return st.session_state["password_correct"]

if not check_password():
    st.stop()

# --- Sistema Principal ---
repo = AgregadoRepository()
st.title("📊 VERIS SIMP - Laudo Técnico")

with st.form("laudo_form"):
    col1, col2 = st.columns(2)
    marca = col1.text_input("Marca")
    crlv = col2.text_input("CRLV / Identificação")
    nome = st.text_input("Nome Completo do Modelo")
    ano = st.number_input("Ano Modelo", 1986, 2026, 2026)
    v_vendedor = st.number_input("Valor Informado pelo Vendedor (R$)", 0.0)
    obs = st.text_area("Observações Técnicas do Vistoriador")
    btn = st.form_submit_button("Analisar e Gerar Laudo")

if btn:
    niveis = repo.calcular_cenarios(ano)
    st.table(list(niveis.items()))
    
    # --- Geração do PDF ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "LAUDO TECNICO - VERIS SIMP", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Modelo: {nome} | CRLV: {crlv}", ln=True)
    pdf.cell(200, 10, f"Ano Modelo: {ano}", ln=True)
    pdf.cell(200, 10, f"Valor Informado pelo Vendedor: R$ {v_vendedor:,.2f}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, "--- Analise de Notas (Estimativa de Mercado) ---", ln=True)
    for nota, valor in niveis.items():
        pdf.cell(200, 10, f"{nota}: R$ {valor:,.2f}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Observacoes Tecnicas: {obs}")
    
    st.download_button("📥 Baixar Laudo PDF", data=pdf.output(dest='S').encode('latin-1'), 
                       file_name=f"laudo_{crlv}.pdf", mime="application/pdf")
