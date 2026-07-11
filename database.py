import pymongo
import streamlit as st

class AgregadoRepository:
    def __init__(self):
        # Conecta usando a URI que está nos seus Secrets
        self.client = pymongo.MongoClient(st.secrets["mongo"]["uri"])
        self.db = self.client["veris_simp_db"]
        self.col_modelos = self.db["modelos"]

    def listar_modelos(self):
        # Busca tudo o que estiver no banco
        return list(self.col_modelos.find({}))

    def salvar_modelo(self, marca, crlv, nome, valor):
        # Salva ou atualiza se o CRLV já existir
        self.col_modelos.update_one(
            {"crlv": crlv}, 
            {"$set": {"marca": marca, "crlv": crlv, "nome_completo": nome, "valor_base": valor}}, 
            upsert=True
        )

# Instancia o repositório
repo = AgregadoRepository()
