import pymongo
import streamlit as st
from datetime import datetime

class AgregadoRepository:
    def __init__(self):
        self.client = pymongo.MongoClient(st.secrets["mongo_uri"])
        self.db = self.client["veris_simp_db"]
        self.col_modelos = self.db["modelos_base"]

    def calcular_cenarios(self, ano, valor_base):
        ano_atual = datetime.now().year
        idade = max(0, ano_atual - int(ano))
        
        # Faixas: (Idade limite, Percentual)
        faixas = [(0, 1.00), (1, 0.90), (3, 0.80), (5, 0.70), (10, 0.60), (20, 0.50), (40, 0.40)]
        perc = 0.40 
        for limite, p in faixas:
            if idade <= limite:
                perc = p
                break
        
        base = float(valor_base) * perc
        return {
            "Nota 5 (Excelente)": base * 1.0, 
            "Nota 4 (Muito Bom)": base * 0.9,
            "Nota 3 (Bom)": base * 0.8, 
            "Nota 2 (Regular)": base * 0.6, 
            "Nota 1 (Ruim)": base * 0.4
        }
