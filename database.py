import pymongo
import streamlit as st

class AgregadoRepository:
    def __init__(self):
        # Acesso seguro via secrets (configurado no dashboard do Streamlit)
        self.client = pymongo.MongoClient(st.secrets["mongo_uri"])
        self.db = self.client["veris_simp_db"]
        self.col_modelos = self.db["modelos"]

    def calcular_cenarios(self, ano):
        idade = max(0, 2026 - int(ano))
        # Lógica de faixas de mercado (estilo FIPE)
        faixas = [(0, 1.00), (1, 0.90), (3, 0.80), (5, 0.70), (10, 0.60), (20, 0.50), (40, 0.40)]
        perc = 0.40 
        for limite, p in faixas:
            if idade <= limite:
                perc = p
                break
        
        base = 200000.0 * perc
        return {
            "Nota 5 (Excelente)": base * 1.0, 
            "Nota 4 (Muito Bom)": base * 0.9,
            "Nota 3 (Bom)": base * 0.8, 
            "Nota 2 (Regular)": base * 0.6, 
            "Nota 1 (Ruim)": base * 0.4
        }
