import pymongo
import streamlit as st

class AgregadoRepository:
    def __init__(self):
        try:
            # A URI deve estar no seu secrets.toml como [mongo] uri
            self.client = pymongo.MongoClient(st.secrets["mongo"]["uri"])
            self.db = self.client["veris_db"]
            self.col_modelos = self.db["modelos"]
            self.col_fabricantes = self.db["fabricantes"]
        except Exception as e:
            st.error(f"Erro de conexão com o banco: {e}")
            self.client = None

    def listar_fabricantes(self):
        if self.client is None: return []
        return [f["nome"] for f in self.col_fabricantes.find({}).sort("nome", 1)]

    def listar_modelos(self):
        if self.client is None: return []
        return list(self.col_modelos.find({}))

    def salvar_fabricante(self, nome):
        self.col_fabricantes.update_one({"nome": nome}, {"$set": {"nome": nome}}, upsert=True)

    def salvar_modelo(self, marca, crlv, nome, valor):
        self.col_modelos.update_one({"crlv": crlv}, {"$set": {"marca": marca, "crlv": crlv, "nome_completo": nome, "valor_base": valor}}, upsert=True)
