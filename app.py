import streamlit as st
from database import AgregadoRepository
from fpdf import FPDF
from PIL import Image

repo = AgregadoRepository()

st.set_page_config(page_title="VERIS SIMP", layout="wide")

fatores = {5: 1.0, 4: 0.9, 3: 0.8, 2: 0.7, 1: 0.6}

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- Login, Logout e Logo na Barra Lateral ---
def check_password():
    if "password_correct" not in st.session_state:
        st.sidebar.title("🔐 Login VERIS SIMP")
        user_input = st.sidebar.text_input("Usuário", key="username")
        pwd_input = st.sidebar.text_input("Senha", type="password", key="password")
        
        if st.sidebar.button("Entrar"):
            # Validação multiusuário contra o dicionário completo do secrets
            usuarios_autorizados = st.secrets.get("usuarios", {})
            if user_input in usuarios_autorizados and str(usuarios_autorizados[user_input]) == str(pwd_input):
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.sidebar.error("Usuário ou senha inválidos")
        return False
    return st.session_state["password_correct"]

if not check_password(): st.stop()

# Logo na barra lateral acima do logout
try:
    st.sidebar.image("logo_veris.png", use_container_width=True)
except: st.sidebar.warning("Logo não encontrada.")

if st.sidebar.button("Logout"):
    st.session_state.password_correct = False
    st.rerun()

# --- Logo no topo da página ---
try:
    st.image("logo_veris.png", width=150)
except: pass

st.title("📊 VERIS SIMP - Agregados")

# --- Interface de Laudo ---
modelos_raw = list(repo.col_modelos.find())
opcoes = {f"{m.get('modelo_completo')} ({m.get('ano_modelo')})": m for m in modelos_raw}

with st.form("laudo_form"):
    sel_modelo = st.selectbox("Seleção de Modelo", list(opcoes.keys()))
    
    # Campo dinâmico exibindo o Valor Sugerido de Mercado (Nota 5) vindo direto do banco/JSON
    dados_selecionados = opcoes[sel_modelo] if sel_modelo else {}
    valor_sugerido_base = dados_selecionados.get('valor_nota_5', 0.0)
    st.info(f"💡 **Valor Sugerido de Mercado (Nota 5):** {formatar_moeda(valor_sugerido_base)}")
    
    valor_vendedor = st.number_input("Valor Informado pelo Vendedor (R$)", 0.0)
    btn = st.form_submit_button("Calcular Valor")

if btn:
    dados = opcoes[sel_modelo]
    st.write("### 📋 Valores por Nota de Vistoria:")
    
    # Exibição cruzada: Valores salvos no Banco/JSON vs. Valores Calculados (Vendedor)
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Valores Oficiais do Banco (FIPE):**")
        st.write(f"**Nota 5 (100%):** {formatar_moeda(dados.get('valor_nota_5', 0.0))}")
        st.write(f"**Nota 4 (95%):** {formatar_moeda(dados.get('valor_nota_4', 0.0))}")
        st.write(f"**Nota 3 (90%):** {formatar_moeda(dados.get('valor_nota_3', 0.0))}")
        st.write(f"**Nota 2 (80%):** {formatar_moeda(dados.get('valor_nota_2', 0.0))}")
        st.write(f"**Nota 1 (70%):** {formatar_moeda(dados.get('valor_nota_1', 0.0))}")

    with col2:
        st.write("**Valores Calculados (Vendedor):**")
        resultados = {nota: valor_vendedor * fator for nota, fator in fatores.items()}
        for nota, val in resultados.items():
            st.write(f"**Nota {nota}:** {formatar_moeda(val)}")

    # PDF com logo alinhada ao topo esquerdo e texto abaixo
    pdf = FPDF()
    pdf.add_page()
   
    try:
        # Logo no topo esquerdo (x=10, y=10)
        pdf.image("logo_veris.png", x=10, y=10, w=40)
    except: pass
   
    pdf.ln(30) # Espaço após a logo para não sobrepor
    pdf.set_font("Arial", size=12)
   
    pdf.cell(0, 10, f"Modelo: {dados.get('modelo_completo')}", ln=True)
    pdf.cell(0, 10, f"Modelo CRLV: {dados.get('modelo_crlv')}", ln=True)
    pdf.cell(0, 10, f"Ano: {dados.get('ano_modelo')}", ln=True)
    pdf.ln(5)
    
    pdf.cell(0, 10, "--- Valores Oficiais por Nota (Banco) ---", ln=True)
    for nota in [5, 4, 3, 2, 1]:
        v_banco = dados.get(f'valor_nota_{nota}', 0.0)
        pdf.cell(0, 10, f"Valor Nota {nota}: {formatar_moeda(v_banco)}", ln=True)
    
    pdf.ln(5)
    
    # Tratamento seguro para geração de bytes no mobile e web desktop
    pdf_output = pdf.output(dest='S')
    pdf_bytes = pdf_output.encode('latin-1') if isinstance(pdf_output, str) else pdf_output

    st.download_button(
        label="📥 Baixar Laudo PDF", 
        data=pdf_bytes,
        file_name="laudo_veris.pdf", 
        mime="application/pdf",
        use_container_width=True # Ajuste do tamanho do botão 100% responsivo focado em Mobile
    )

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
