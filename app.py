import streamlit as st
from database import AgregadoRepository
from fpdf import FPDF
from PIL import Image

repo = AgregadoRepository()

st.set_page_config(page_title="VERIS SIMP", layout="wide")

fatores = {5: 1.0, 4: 0.9, 3: 0.8, 2: 0.7, 1: 0.6}

def formatar_moeda(valor):
    return f"R$ ({valor:,.2f})".replace(",", "X").replace(".", ",").replace("X", ".")

# --- Login, Logout e Logo na Barra Lateral ---
def check_password():
    if "password_correct" not in st.session_state:
        st.sidebar.title("🔐 Login VERIS SIMP")
        user = st.sidebar.text_input("Usuário", key="username")
        pwd = st.sidebar.text_input("Senha", type="password", key="password")
        if st.sidebar.button("Entrar"):
            if user == st.secrets["admin_user"] and pwd == st.secrets["admin_pass"]:
                st.session_state["password_correct"] = True
                st.rerun()
        return False
    return st.session_state["password_correct"]

if not check_password(): st.stop()

# Logo acima do logout
try:
    st.sidebar.image("logo_veris.png", use_container_width=True)
except: st.sidebar.warning("Logo não encontrada.")

if st.sidebar.button("Logout"):
    st.session_state.password_correct = False
    st.rerun()

st.title("📊 VERIS SIMP - Agregados")

# --- Interface de Laudo ---
modelos_raw = list(repo.col_modelos.find())
opcoes = {f"{m.get('modelo_completo')} ({m.get('ano_modelo')})": m for m in modelos_raw}

with st.form("laudo_form"):
    sel_modelo = st.selectbox("Seleção de Modelo", list(opcoes.keys()))
    valor_vendedor = st.number_input("Valor Informado pelo Vendedor (R$)", 0.0)
    btn = st.form_submit_button("Calcular Valor")

if btn:
    st.write("### Valores por Nota:")
    resultados = {nota: valor_vendedor * fator for nota, fator in fatores.items()}
    for nota, val in resultados.items():
        st.write(f"**Nota {nota}:** {formatar_moeda(val)}")

    # PDF com espaçamento de 3 linhas (ln(30)) após a logo
    dados = opcoes[sel_modelo]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(50, 50, 50)
    pdf.rect(0, 0, 210, 297, 'F')
    
    try:
        pdf.image("logo_veris.png", x=80, y=20, w=50)
    except: pass
    
    pdf.ln(30) # Espaço de 3 linhas após a logo
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", size=12)
    
    pdf.cell(0, 10, f"Modelo: {dados.get('modelo_completo')}", ln=True)
    pdf.cell(0, 10, f"Modelo CRLV: {dados.get('modelo_crlv')}", ln=True)
    pdf.cell(0, 10, f"Ano: {dados.get('ano_modelo')}", ln=True)
    pdf.ln(5)
    for nota, val in resultados.items():
        pdf.cell(0, 10, f"Valor Nota {nota}: {formatar_moeda(val)}", ln=True)

    st.download_button("📥 Baixar Laudo PDF", data=pdf.output(dest='S').encode('latin-1'),
                       file_name="laudo_veris.pdf", mime="application/pdf")

# --- Administrativo ---
with st.expander("⚙️ Cadastrar Novo Modelo"):
    with st.form("admin_novo"):
        marca = st.text_input("Marca")
        modelo_crlv = st.text_input("Modelo (CRLV)")
        modelo_comp = st.text_input("Modelo Completo")
        categoria = st.text_input("Categoria")
        ano_mod = st.number_input("Ano Modelo", min_value=1900, max_value=2050)
        ano_fab = st.number_input("Ano Fabricação", min_value=1900, max_value=2050)
        
        if st.form_submit_button("Salvar no Banco"):
            repo.col_modelos.insert_one({
                "marca": marca, "modelo_crlv": modelo_crlv, 
                "modelo_completo": modelo_comp, "categoria": categoria,
                "ano_modelo": ano_mod, "ano_fabricacao": ano_fab
            })
            st.success("Cadastrado com sucesso!")
            st.rerun()
