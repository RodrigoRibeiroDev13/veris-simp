# app.py
import streamlit as st
import streamlit_authenticator as stauth
from database import AgregadoRepository
from calculator import CalculadoraAgregados
import datetime

st.set_page_config(page_title="Veris SIMP", page_icon="🎯", layout="wide")

repo = AgregadoRepository()

# --- CONFIGURAÇÃO DE AUTENTICAÇÃO (CORRIGIDA) ---
credentials_config = st.secrets["credentials"].to_dict()

# Ajuste nos parâmetros da versão atual da biblioteca
authenticator = stauth.Authenticate(
    credentials=credentials_config["usernames"],
    cookie_name="veris_simp_cookie",
    key=st.secrets["auth"]["cookie_key"],
    cookie_expiry_days=int(st.secrets["auth"]["expiry_days"])
)

# Renderização da tela de login
authenticator.login(location="main")

# Captura de dados de estado
authentication_status = st.session_state.get("authentication_status")
username = st.session_state.get("username")
name = credentials_config["usernames"].get(username, {}).get("name", "") if username else ""

if authentication_status == False:
    st.error("Usuário ou senha incorretos do Veris SIMP.")
elif authentication_status == None:
    st.info("Insira suas credenciais para acesso ao sistema.")
elif authentication_status:
   
    with st.sidebar:
        st.markdown("### 🛡️ Credencial Corporativa")
        st.write(f"👤 **Analista:** {name}")
        st.write(f"🔑 **ID:** @{username}")
        st.divider()
        authenticator.logout("Desconectar do Veris SIMP", "sidebar")
   
    # --- LOGOMARCA E IDENTIDADE VISUAL DO SISTEMA ---
    st.markdown(
        """
        <div style="text-align: center; padding: 10px; border-bottom: 2px solid #0284C7;">
            <h1 style="color: #0284C7; margin-bottom: 0px; font-family: 'Montserrat', sans-serif; font-weight: 800; letter-spacing: 2px;">
                🎯 VERIS <span style="color: #64748B; font-weight: 300;">SIMP</span>
            </h1>
            <p style="color: #94A3B8; font-size: 12px; margin-top: 5px; letter-spacing: 1px;">
                SISTEMA INTELIGENTE DE MODELOS E PRECIFICAÇÃO
            </p>
        </div>
        """,
        unsafe_html=True
    )
    st.write("") 
   
    tab_precificador, tab_catalogo, tab_historico = st.tabs([
        "🧮 Interface de Precificação", "➕ Catálogo de Modelos", "📊 Histórico & PDF"
    ])

    # INTERFACE 1: PRECIFICADOR
    with tab_precificador:
        st.subheader("Avaliação de Mercado Automatizada")
        c1, c2 = st.columns(2)
        with c1:
            marca = st.selectbox("Marca do Implemento", ["RANDON", "NOMA", "FACCHINI", "SÃO PEDRO", "OUTRA"])
            crlv_busca = st.text_input("Descrição Resumida do CRLV (Busca no Banco)").upper().strip()
            codigo_fipe = st.text_input("Código FIPE (Opcional - Consulta BrasilAPI)", placeholder="Ex: 054001-3")
       
        modelo_db = repo.buscar_modelo(crlv_busca)
       
        with c2:
            ano = st.number_input("Ano do Modelo", min_value=1990, max_value=2027, value=2022)
            estado = st.selectbox("Estado de Conservação Física", [
                "Excelente (Sem detalhes / Pneus Novos)", "Bom (Marcas normais de uso)",
                "Regular (Necessita de pequenas reformas)", "Ruim (Avariado / Sem condições de rodagem)"
            ])
           
            valor_base = modelo_db["valor_estimado_base"] if modelo_db else 80000.0
            nome_comercial = modelo_db["nome_completo"] if modelo_db else "Modelo não mapeado localmente"
            st.text(f"Mapeamento Local Detectado: {nome_comercial}")

        precificacao = CalculadoraAgregados.obter_valor_sugerido(valor_base, ano, estado, codigo_fipe)
       
        st.divider()
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(label="Preço Calculado Automático", value=f"R$ {precificacao['valor_final']:,.2f}")
            st.caption(f"Fonte de Dados Utilizada: {precificacao['fonte']}")
        with col_m2:
            valor_fixado = st.number_input("Valor Final Arbitrado pelo Analista (R$)", value=float(precificacao['valor_final']))
           
        placa = st.text_input("Placa do Agregado", max_chars=7).upper()
        justificativa = st.text_area("Justificativa Técnica do Laudo")
       
        if st.button("Gravar Avaliação Definitiva", type="primary"):
            if not placa or not crlv_busca:
                st.error("Campos obrigatórios (Placa e CRLV) não foram preenchidos.")
            else:
                dados_laudo = {
                    "placa": placa, "marca": marca, "crlv_resumido": crlv_busca, "nome_completo": nome_comercial,
                    "ano_fabricacao": ano, "estado_conservacao": estado, "valor_final_fixado": valor_fixado,
                    "justificativa": justificativa, "analista": username, "data_analise": datetime.datetime.now()
                }
                repo.salvar_analise(dados_laudo)
                st.success("Avaliação registrada com sucesso no MongoDB Atlas!")

    # INTERFACE 2: ALIMENTAÇÃO DE MODELOS
    with tab_catalogo:
        st.subheader("Injeção de Novos Modelos no Catálogo")
        with st.form("form_novo_modelo"):
            m_marca = st.selectbox("Marca Associada", ["RANDON", "NOMA", "FACCHINI", "SÃO PEDRO", "OUTRA"])
            m_crlv = st.text_input("Texto do CRLV (Ex: SR/NOMA CA)").upper()
            m_nome = st.text_input("Nome Comercial Completo (Ex: Semireboque Carga Aberta Noma)")
            m_valor = st.number_input("Valor de Referência Novo (R$)", value=100000.0)
           
            if st.form_submit_button("Registrar Modelo no Catálogo"):
                if m_crlv and m_nome:
                    repo.salvar_modelo_catalogo(m_marca, m_crlv, m_nome, m_valor)
                    st.success("Modelo adicionado com sucesso para consultas futuras no Veris SIMP!")
                else:
                    st.error("Preencha todos os campos do formulário.")

    # INTERFACE 3: HISTÓRICO E COMPONENTE DOWNLOAD DE PDF
    with tab_historico:
        st.subheader("Histórico de Laudos Emitidos")
        historico = repo.listar_laudos()
        if not historico:
            st.info("Nenhum laudo gravado no sistema.")
        for h in historico:
            with st.expander(f"📋 Placa: {h['placa']} | {h['marca']} - R$ {h['valor_final_fixado']:,.2f}"):
                st.write(f"**Analista:** @{h['analista']} | **Modelo:** {h['nome_completo']}")
                st.write(f"**Justificativa:** {h['justificativa']}")
               
                pdf_output = CalculadoraAgregados.gerar_pdf_laudo(h)
               
                if isinstance(pdf_output, bytes):
                    pdf_bytes = pdf_output
                elif hasattr(pdf_output, 'output'):
                    pdf_bytes = pdf_output.output(dest='S')
                else:
                    pdf_bytes = bytes(str(pdf_output), 'utf-8')
               
                st.download_button(
                    label="📥 Gerar e Baixar Laudo PDF",
                    data=pdf_bytes,
                    file_name=f"laudo_{h['placa']}.pdf",
                    mime="application/pdf",
                    key=f"btn_{h['_id']}"
                )
