# app.py
import streamlit as st
import streamlit_authenticator as stauth
from database import AgregadoRepository
from calculator import CalculadoraAgregados
import datetime

st.set_page_config(page_title="Veris SIMP", page_icon="🎯", layout="wide")

repo = AgregadoRepository()

# --- CONFIGURAÇÃO DE AUTENTICAÇÃO (ROBUSTA) ---
config = st.secrets.to_dict()
# Estrutura obrigatória para a versão atual da biblioteca
credentials_dict = {"usernames": config["credentials"]["usernames"]}

authenticator = stauth.Authenticate(
    credentials=credentials_dict,
    cookie_name="veris_simp_cookie",
    key=config["auth"]["cookie_key"],
    cookie_expiry_days=int(config["auth"]["expiry_days"])
)

# Renderiza o formulário de login
authenticator.login(location="main")

# --- LÓGICA DE CONTROLE DE ACESSO COM FEEDBACK ---
if st.session_state.get("authentication_status") == True:
    username = st.session_state.get("username")
    name = credentials_dict["usernames"].get(username, {}).get("name", "Usuário")

    with st.sidebar:
        st.markdown("### 🛡️ Credencial Corporativa")
        st.write(f"👤 **Analista:** {name}")
        st.write(f"🔑 **ID:** @{username}")
        st.divider()
        authenticator.logout("Desconectar do Veris SIMP", "sidebar")
   
    st.markdown("""<div style="text-align: center; padding: 10px; border-bottom: 2px solid #0284C7;">
            <h1 style="color: #0284C7; margin-bottom: 0px; font-family: 'Montserrat', sans-serif; font-weight: 800; letter-spacing: 2px;">
                🎯 VERIS <span style="color: #64748B; font-weight: 300;">SIMP</span>
            </h1>
            <p style="color: #94A3B8; font-size: 12px; margin-top: 5px; letter-spacing: 1px;">
                SISTEMA INTELIGENTE DE MODELOS E PRECIFICAÇÃO
            </p>
        </div>""", unsafe_html=True)
   
    tab_precificador, tab_catalogo, tab_historico = st.tabs([
        "🧮 Interface de Precificação", "➕ Catálogo de Modelos", "📊 Histórico & PDF"
    ])

    with tab_precificador:
        st.subheader("Avaliação de Mercado Automatizada")
        c1, c2 = st.columns(2)
        with c1:
            marca = st.selectbox("Marca do Implemento", ["RANDON", "NOMA", "FACCHINI", "SÃO PEDRO", "OUTRA"])
            crlv_busca = st.text_input("Descrição Resumida do CRLV (Busca no Banco)").upper().strip()
            codigo_fipe = st.text_input("Código FIPE", placeholder="Ex: 054001-3")
        modelo_db = repo.buscar_modelo(crlv_busca)
        with c2:
            ano = st.number_input("Ano do Modelo", min_value=1990, max_value=2027, value=2022)
            estado = st.selectbox("Estado de Conservação", ["Excelente", "Bom", "Regular", "Ruim"])
            valor_base = modelo_db["valor_estimado_base"] if modelo_db else 80000.0
            st.text(f"Mapeamento Local: {modelo_db['nome_completo'] if modelo_db else 'Não mapeado'}")

        precificacao = CalculadoraAgregados.obter_valor_sugerido(valor_base, ano, estado, codigo_fipe)
        st.divider()
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(label="Preço Calculado Automático", value=f"R$ {precificacao['valor_final']:,.2f}")
        with col_m2:
            valor_fixado = st.number_input("Valor Final Arbitrado (R$)", value=float(precificacao['valor_final']))
        placa = st.text_input("Placa do Agregado", max_chars=7).upper()
        justificativa = st.text_area("Justificativa Técnica")
       
        if st.button("Gravar Avaliação Definitiva", type="primary"):
            dados_laudo = {
                "placa": placa, "marca": marca, "nome_completo": modelo_db.get("nome_completo", "N/A") if modelo_db else "N/A",
                "ano_fabricacao": ano, "estado_conservacao": estado, "valor_final_fixado": valor_fixado,
                "justificativa": justificativa, "analista": username, "data_analise": datetime.datetime.now()
            }
            repo.salvar_analise(dados_laudo)
            st.success("Avaliação registrada com sucesso!")

    with tab_catalogo:
        st.subheader("Injeção de Novos Modelos")
        with st.form("form_novo_modelo"):
            m_marca = st.selectbox("Marca Associada", ["RANDON", "NOMA", "FACCHINI", "SÃO PEDRO", "OUTRA"])
            m_crlv = st.text_input("Texto do CRLV").upper()
            m_nome = st.text_input("Nome Comercial Completo")
            m_valor = st.number_input("Valor de Referência (R$)", value=100000.0)
            if st.form_submit_button("Registrar Modelo"):
                repo.salvar_modelo_catalogo(m_marca, m_crlv, m_nome, m_valor)
                st.success("Modelo adicionado!")

    with tab_historico:
        st.subheader("Histórico de Laudos")
        historico = repo.listar_laudos()
        for h in historico:
            with st.expander(f"Placa: {h['placa']} - R$ {h['valor_final_fixado']:,.2f}"):
                st.write(f"Analista: @{h['analista']}")
                pdf_output = CalculadoraAgregados.gerar_pdf_laudo(h)
                st.download_button("📥 Baixar Laudo PDF", data=pdf_output, file_name=f"laudo_{h['placa']}.pdf")

elif st.session_state.get("authentication_status") == False:
    st.error("Usuário ou senha incorretos.")
elif st.session_state.get("authentication_status") == None:
    st.info("Insira suas credenciais para acessar o Veris SIMP.")
