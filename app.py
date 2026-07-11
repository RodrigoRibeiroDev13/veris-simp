import streamlit as st
from database import AgregadoRepository
from fpdf import FPDF
from datetime import datetime

# --- Configuração ---
repo = AgregadoRepository()

def check_password():
    if "password_correct" not in st.session_state:
        st.sidebar.title("🔐 Login VERIS SIMP")
        st.sidebar.text_input("Usuário", key="username")
        st.sidebar.text_input("Senha", type="password", key="password")
        if st.sidebar.button("Entrar"):
            if st.session_state["username"] == st.secrets["admin_user"] and \
               st.session_state["password"] == st.secrets["admin_pass"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.sidebar.error("Credenciais inválidas")
        return False
    return st.session_state["password_correct"]

if not check_password():
    st.stop()

st.title("📊 VERIS SIMP - Auditoria de Ativos")

# --- Formulario ---
modelos = list(repo.col_modelos.find())
opcoes = {m['modelo_nome']: m for m in modelos}

with st.form("laudo_form"):
    sel_modelo = st.selectbox("Selecione o Modelo", list(opcoes.keys()))
    dados = opcoes[sel_modelo]
    
    ano = st.number_input("Ano do Equipamento", min_value=1986, max_value=datetime.now().year, value=datetime.now().year)
    v_vendedor = st.number_input("Valor Informado pelo Vendedor (R$)", 0.0)
    obs = st.text_area("Observações Técnicas")
    btn = st.form_submit_button("Gerar Laudo PDF (Dark Mode)")

if btn:
    resultados = repo.calcular_cenarios(ano, dados['valor_base_novo'])
    st.table(list(resultados.items()))
    
    # --- Geração PDF Dark Mode ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(50, 50, 50) # Cinza Escuro
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(255, 255, 255) # Branco
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "LAUDO TECNICO - VERIS SIMP", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Modelo: {sel_modelo} | Ano: {ano}", ln=True)
    pdf.cell(0, 10, f"Valor Vendedor: R$ {v_vendedor:,.2f}", ln=True)
    pdf.ln(5)
    for n, v in resultados.items():
        pdf.cell(0, 10, f"{n}: R$ {v:,.2f}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Observacoes: {obs}")
    
    st.download_button("📥 Baixar Laudo PDF", data=pdf.output(dest='S').encode('latin-1'), 
                       file_name=f"laudo_{sel_modelo}.pdf", mime="application/pdf")

# --- Administrativo ---
with st.expander("⚙️ Cadastrar Novo Modelo"):
    with st.form("admin_novo"):
        n_marca = st.text_input("Marca")
        n_nome = st.text_input("Nome do Modelo")
        n_valor = st.number_input("Valor Base Novo")
        if st.form_submit_button("Salvar"):
            repo.col_modelos.insert_one({"marca": n_marca, "modelo_nome": n_nome, "valor_base_novo": n_valor})
            st.rerun()
