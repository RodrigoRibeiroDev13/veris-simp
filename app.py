import streamlit as st
from database import AgregadoRepository
from fpdf import FPDF
from datetime import datetime
from PIL import Image

repo = AgregadoRepository()

# --- Configuração Inicial e Logo ---
st.set_page_config(page_title="VERIS SIMP", layout="wide")

try:
    logo = Image.open("logo_veris.png")
    st.sidebar.image(logo, use_container_width=True)
except:
    st.sidebar.warning("Logo não encontrada (salve como logo_veris.png)")

# --- Login ---
def check_password():
    if "password_correct" not in st.session_state:
        st.sidebar.title("🔐 Login VERIS SIMP")
        user = st.sidebar.text_input("Usuário", key="username")
        pwd = st.sidebar.text_input("Senha", type="password", key="password")
        if st.sidebar.button("Entrar"):
            if user == st.secrets["admin_user"] and pwd == st.secrets["admin_pass"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.sidebar.error("Credenciais inválidas")
        return False
    return st.session_state["password_correct"]

if not check_password():
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state.password_correct = False
    st.rerun()

st.title("📊 VERIS SIMP - Agregados")

# --- Interface de Laudo ---
modelos_raw = list(repo.col_modelos.find())
opcoes = {m.get('modelo_nome', 'Modelo Sem Nome'): m for m in modelos_raw}

if not opcoes:
    st.error("Nenhum modelo encontrado no banco! Use a aba administrativa abaixo.")
    opcoes = {"Nenhum": {"marca": "N/A", "valor_base_novo": 0}}

with st.form("laudo_form"):
    sel_modelo = st.selectbox("Seleção de Modelo", list(opcoes.keys()))
    dados = opcoes[sel_modelo]
    ano = st.number_input("Ano do Equipamento", min_value=1986, max_value=datetime.now().year, value=datetime.now().year)
    v_vendedor = st.number_input("Valor Informado pelo Vendedor (R$)", 0.0)
    obs = st.text_area("Observações Técnicas")
    btn = st.form_submit_button("Gerar Laudo PDF")

if btn:
    resultados = repo.calcular_cenarios(ano, dados.get('valor_base_novo', 0))
    st.table(list(resultados.items()))

    # --- Geração PDF com Logo ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(50, 50, 50)
    pdf.rect(0, 0, 210, 297, 'F')
    
    # Inserir Logo no PDF (tamanho ajustado)
    try:
        pdf.image("logo_veris.png", x=80, y=10, w=50)
        pdf.ln(30)
    except:
        pass

    pdf.set_text_color(255, 255, 255)
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
    pdf.multi_cell(0, 10, f"Observações: {obs}")

    st.download_button("📥 Baixar Laudo PDF", data=pdf.output(dest='S').encode('latin-1'),
                       file_name=f"laudo_{sel_modelo}.pdf", mime="application/pdf")

# --- Administrativo com Validação ---
with st.expander("⚙️ Cadastrar Novo Modelo"):
    with st.form("admin_novo"):
        n_marca = st.text_input("Marca")
        n_nome = st.text_input("Nome do Modelo")
        n_valor = st.number_input("Valor Base Novo")
        
        if st.form_submit_button("Salvar no Banco"):
            if not n_marca or not n_nome or n_valor == 0:
                st.error("Erro: Preencha todos os campos corretamente!")
            else:
                repo.col_modelos.insert_one({"marca": n_marca, "modelo_nome": n_nome, "valor_base_novo": n_valor})
                st.success("Cadastrado com sucesso!")
                st.rerun()
