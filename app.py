import streamlit as st
import streamlit_authenticator as stauth
from database import AgregadoRepository

st.set_page_config(page_title="Veris SIMP", page_icon="🎯", layout="wide")

repo = AgregadoRepository()

# --- AUTENTICAÇÃO ---
config = st.secrets.to_dict()
authenticator = stauth.Authenticate(
    {"usernames": config["credentials"]["usernames"]}, 
    "veris_simp_cookie", config["auth"]["cookie_key"], int(config["auth"]["expiry_days"])
)
authenticator.login(location="main")

if st.session_state.get("authentication_status"):
    st.title("🎯 VERIS SIMP - Gestão de Agregados")
    
    tab_precificador, tab_catalogo = st.tabs(["🧮 Precificar / Consultar", "➕ Cadastro Geral"])

    with tab_precificador:
        st.header("Buscar Modelo no Sistema")
        modelos = repo.listar_modelos()
        lista_crlv = [m['crlv'] for m in modelos]
        
        busca = st.selectbox("Selecione o modelo (CRLV):", [""] + lista_crlv)
        
        if busca:
            m = next((mod for mod in modelos if mod['crlv'] == busca), None)
            st.success(f"**Modelo:** {m['nome_completo']} | **Marca:** {m['marca']} | **Valor Base:** R$ {m['valor_base']:,.2f}")
        else:
            st.info("Selecione um modelo na lista acima para visualizar os dados.")

    with tab_catalogo:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Novo Fabricante")
            with st.form("form_fab"):
                novo_fab = st.text_input("Nome do Fabricante").upper()
                if st.form_submit_button("Salvar Fabricante"):
                    if novo_fab:
                        repo.salvar_fabricante(novo_fab)
                        st.success(f"Fabricante {novo_fab} salvo!")
                        st.rerun()
        
        with col2:
            st.subheader("Novo Modelo")
            fabricantes = repo.listar_fabricantes()
            with st.form("form_mod"):
                marca = st.selectbox("Selecione o Fabricante", fabricantes)
                crlv = st.text_input("CRLV/Identificação (Chave única)").upper()
                nome = st.text_input("Nome Comercial Completo")
                valor = st.number_input("Valor Referência (R$)", min_value=0.0)
                if st.form_submit_button("Salvar Modelo"):
                    if crlv and marca:
                        repo.salvar_modelo(marca, crlv, nome, valor)
                        st.success("Modelo salvo com sucesso!")
                        st.rerun()
                    else:
                        st.error("Preencha o CRLV e selecione um fabricante.")

elif st.session_state.get("authentication_status") == False:
    st.error("Usuário ou senha incorretos.")
