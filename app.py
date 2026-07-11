import streamlit as st
import streamlit_authenticator as stauth
from database import AgregadoRepository

st.set_page_config(page_title="Veris SIMP", page_icon="🎯", layout="wide")

repo = AgregadoRepository()

# --- AUTENTICAÇÃO ---
config = st.secrets.to_dict()
credentials_dict = {"usernames": config["credentials"]["usernames"]}

authenticator = stauth.Authenticate(
    credentials_dict, "veris_simp_cookie", config["auth"]["cookie_key"], int(config["auth"]["expiry_days"])
)
authenticator.login(location="main")

# --- INTERFACE PROTEGIDA ---
if st.session_state.get("authentication_status"):
    
    st.title("🎯 VERIS SIMP - Gestão de Agregados")
    
    tab_precificador, tab_catalogo = st.tabs(["🧮 Precificar / Consultar", "➕ Cadastrar Novo Modelo"])

    with tab_precificador:
        st.header("Buscar no Banco de Dados")
        
        # Carrega modelos do MongoDB
        todos_modelos = repo.listar_todos_modelos()
        lista_crlv = [m['crlv'] for m in todos_modelos]
        
        busca = st.selectbox("Selecione ou digite o modelo (CRLV):", [""] + lista_crlv)
        
        if busca:
            modelo = next((m for m in todos_modelos if m['crlv'] == busca), None)
            if modelo:
                st.success(f"Modelo: {modelo['nome_completo']} | Valor Referência: R$ {modelo['valor_base']:,.2f}")
        else:
            st.info("Digite um modelo acima para ver a precificação.")

        st.divider()
        st.markdown("""
        ### 🔍 Onde encontrar preços de referência?
        Caso o modelo não esteja no sistema, sugerimos consultar:
        * **[Shoptrans](https://www.shoptrans.com.br)**
        * **[Caminhões e Carretas](https://www.caminhoesecarretas.com.br)**
        * **[Mercado Livre (Implementos)](https://veiculos.mercadolivre.com.br/caminhoes/implementos/)**
        """)

    with tab_catalogo:
        st.header("Cadastrar Novo Modelo")
        with st.form("form_cadastro"):
            crlv = st.text_input("Descrição Resumida no CRLV").upper()
            marca = st.selectbox("Marca", ["RANDON", "NOMA", "FACCHINI", "SÃO PEDRO", "GUERRA", "LIBRELATO", "OUTRA"])
            nome = st.text_input("Nome Completo do Modelo")
            valor = st.number_input("Valor Médio de Referência (R$)", min_value=0.0)
            
            if st.form_submit_button("Salvar no Catálogo"):
                if crlv and valor > 0:
                    repo.salvar_modelo_catalogo(marca, crlv, nome, valor)
                    st.success("Modelo cadastrado com sucesso! Recarregue a página para ver na busca.")
                else:
                    st.error("Preencha o CRLV e o Valor.")

elif st.session_state.get("authentication_status") == False:
    st.error("Usuário ou senha inválidos.")
