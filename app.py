import streamlit as st
from database import repo

st.set_page_config(page_title="VERIS SIMP - Gestão")
st.title("🎯 VERIS SIMP - Gestão")

tab1, tab2 = st.tabs(["📊 Precificar / Consultar", "➕ Cadastro Geral"])

# --- ABA 1: CONSULTA ---
with tab1:
    st.subheader("Buscar Modelo no Sistema")
    modelos = repo.listar_modelos()
    
    if modelos:
        # Cria dicionário para busca fácil pelo nome
        opcoes = {m['nome_completo']: m for m in modelos}
        selecionado = st.selectbox("Selecione o modelo:", options=list(opcoes.keys()))
        
        if selecionado:
            m = opcoes[selecionado]
            st.write(f"**Marca:** {m['marca']}")
            st.write(f"**CRLV:** {m['crlv']}")
            st.write(f"**Valor Base:** R$ {m['valor_base']:,.2f}")
    else:
        st.info("Nenhum modelo cadastrado. Vá em 'Cadastro Geral' para adicionar.")

# --- ABA 2: CADASTRO ---
with tab2:
    st.subheader("Cadastrar Novo Modelo")
    with st.form("form_cadastro"):
        marca = st.text_input("Marca")
        crlv = st.text_input("CRLV (Identificador Único)")
        nome = st.text_input("Nome Completo do Modelo")
        valor = st.number_input("Valor Base (R$)", min_value=0.0)
        
        if st.form_submit_button("Salvar no Banco"):
            if marca and crlv and nome:
                repo.salvar_modelo(marca, crlv, nome, valor)
                st.success("Modelo salvo com sucesso!")
            else:
                st.error("Preencha todos os campos!")
