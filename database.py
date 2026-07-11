import pymongo
import streamlit as st

class AgregadoRepository:
    def __init__(self):
        self.client = pymongo.MongoClient(st.secrets["mongo"]["uri"])
        self.db = self.client["veris_simp_db"]
        self.col_modelos = self.db["modelos"]
        if self.col_modelos.count_documents({}) == 0:
            self._carregar_dados_iniciais()

    def _carregar_dados_iniciais(self):
        top_marcas = ["RANDON", "FACCHINI", "LIBRELATO", "NOMA", "GUERRA", "PASTRE", "KRONE", 
                      "RODOLISO", "TRIEL-HT", "RECRUSUL", "SERGOMEL", "DANTAS", "MTU", "IBIPORA", 
                      "GOMES", "STRUML", "BRUMAQ", "CARRAZZA", "JABUR", "VARGAS", "DIMA", 
                      "TECNO-TRANS", "METALESP", "SÃO PEDRO", "TROPPA", "IMPLANOR", "HERCULES", 
                      "ASTRA", "ROSSI", "KONEBRAS", "METALURGICA", "RECMAR", "VETOR", "METALFRIO", 
                      "BASC-BRAS", "TANQ-TECH", "GRAN-SUL", "SIDE-NORTE", "PRAN-LIDER", "FURG-MAX", 
                      "AGRO-TEC", "FLOR-ESTA", "CANA-FORTE", "ROAD-TECH", "MEGA-TRUCK", "EURO-TRAIL", 
                      "GLOBAL-VANS", "MASTER-LOG", "SILO-FIX", "TRANS-VITA"]
        
        outras_marcas = [f"REG_{i:03d}" for i in range(1, 151)]
        modelos_base = ["Graneleiro", "Sider", "Basculante", "Carga Aberta", "Tanque"]
        
        dados = []
        for marca in top_marcas:
            for i, mod in enumerate(modelos_base):
                dados.append({"marca": marca, "crlv": f"{marca[:3]}-{mod[:3]}-{i}", "nome_completo": f"{marca} {mod}", "valor_base": float(150000 + (i * 25000))})
        
        for marca in outras_marcas:
            for mod in modelos_base:
                if len(dados) < 1000:
                    dados.append({"marca": marca, "crlv": f"{marca}-{mod[:2]}", "nome_completo": f"{marca} - {mod}", "valor_base": 140000.0})
        
        self.col_modelos.insert_many(dados)

    def listar_modelos(self):
        return list(self.col_modelos.find({}))

    def salvar_modelo(self, marca, crlv, nome, valor):
        self.col_modelos.update_one({"crlv": crlv}, {"$set": {"marca": marca, "crlv": crlv, "nome_completo": nome, "valor_base": float(valor)}}, upsert=True)

    def calcular_valor_por_nota(self, valor_base, nota):
        fatores = {5: 1.0, 4: 0.9, 3: 0.8, 2: 0.6, 1: 0.4}
        return float(valor_base) * fatores.get(int(nota), 0.4)

repo = AgregadoRepository()
