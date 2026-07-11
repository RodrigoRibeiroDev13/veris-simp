import pymongo
import streamlit as st

class AgregadoRepository:
    def __init__(self):
        # A URI do MongoDB deve estar no seu secrets.toml
        self.client = pymongo.MongoClient(st.secrets["mongo"]["uri"])
        self.db = self.client["veris_db"]
        self.col_modelos = self.db["modelos"]
        self.col_fabricantes = self.db["fabricantes"]

    # --- FABRICANTES ---
    def salvar_fabricante(self, nome_fabricante):
        self.col_fabricantes.update_one(
            {"nome": nome_fabricante}, 
            {"$set": {"nome": nome_fabricante}}, 
            upsert=True
        )

    def listar_fabricantes(self):
        return [f["nome"] for f in self.col_fabricantes.find({}).sort("nome", 1)]

    # --- MODELOS ---
    def salvar_modelo(self, marca, crlv, nome, valor):
        query = {"crlv": crlv}
        new_values = {
            "$set": {
                "marca": marca, 
                "crlv": crlv, 
                "nome_completo": nome, 
                "valor_base": valor
            }
        }
        self.col_modelos.update_one(query, new_values, upsert=True)

    def listar_modelos(self):
        return list(self.col_modelos.find({}))
