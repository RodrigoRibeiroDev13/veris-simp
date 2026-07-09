# database.py
import pymongo
import streamlit as st

class AgregadoRepository:
    def __init__(self):
        # Conexão original segura via secrets do Streamlit
        self.client = pymongo.MongoClient(st.secrets["mongo"]["uri"])
        self.db = self.client[st.secrets["mongo"]["database"]]
        
        self.colecao_catalogo = self.db["catalogo_modelos"]
        self.colecao_laudos = self.db["laudos_emitidos"]

        # --- SUPER CATÁLOGO EXTENSO DEFINITIVO (TODOS OS MODELOS POSSÍVEIS) ---
        self.CATALOGO_INTERNO = {
            # === RANDON ===
            "SR/RANDON SR CA": {"nome": "Semireboque Carga Aberta Randon", "valor": 85000.0},
            "SR/RANDON GR MET": {"nome": "Semireboque Graneleiro Metálico Randon", "valor": 110000.0},
            "SR/RANDON CG BA": {"nome": "Semireboque Carga Geral Baú Randon", "valor": 95000.0},
            "SR/RANDON SIDER": {"nome": "Semireboque Sider Randon", "valor": 105000.0},
            "SR/RANDON TANK": {"nome": "Semireboque Tanque Combustível Randon", "valor": 130000.0},
            "SR/RANDON CA CD": {"nome": "Semireboque Caçamba Basculante Randon", "valor": 120000.0},
            "SR/RANDON PORTA CON": {"nome": "Semireboque Porta Contêiner Randon", "valor": 75000.0},
            "SR/RANDON PRANCHA": {"nome": "Semireboque Carrega Tudo Prancha Randon", "valor": 160000.0},
            "SR/RANDON CEGONHA": {"nome": "Semireboque Cegonha Randon", "valor": 135000.0},
            "SR/RANDON DOLLY": {"nome": "Semireboque Dolly Intermediário Randon", "valor": 45000.0},
            "REB/RANDON CANA": {"nome": "Reboque Canavieiro (Trenzinho) Randon", "valor": 85000.0},
            "SR/RANDON FLORESTAL": {"nome": "Semireboque Florestal Toras Randon", "valor": 115000.0},
            "SR/RANDON SILO": {"nome": "Semireboque Silo Pressurizado Randon", "valor": 140000.0},
            
            # === NOMA ===
            "SR/NOMA CA GR": {"nome": "Semireboque Carga Aberta Graneleiro Noma", "valor": 100000.0},
            "SR/NOMA SIDER FLO": {"nome": "Semireboque Sider Florestal Noma", "valor": 125000.0},
            "SR/NOMA BA FURG": {"nome": "Semireboque Baú Furgão Noma", "valor": 90000.0},
            "SR/NOMA CA SIDER": {"nome": "Semireboque Carga Aberta Sider Noma", "valor": 102000.0},
            "SR/NOMA CA BASCO": {"nome": "Semireboque Caçamba Noma", "valor": 115000.0},
            "SR/NOMA TANK": {"nome": "Semireboque Tanque Inox Noma", "valor": 138000.0},
            "SR/NOMA PORTA CON": {"nome": "Semireboque Porta Contêiner Noma", "valor": 72000.0},
            
            # === FACCHINI ===
            "SR/FACCHINI SR CA": {"nome": "Semireboque Carga Aberta Facchini", "valor": 80000.0},
            "SR/FACCHINI GR METAL": {"nome": "Semireboque Graneleiro Facchini", "valor": 105000.0},
            "SR/FACCHINI BA FURG": {"nome": "Semireboque Baú Alumínio Facchini", "valor": 92000.0},
            "SR/FACCHINI SIDER": {"nome": "Semireboque Sider Facchini", "valor": 98000.0},
            "SR/FACCHINI TANK": {"nome": "Semireboque Tanque Inox Facchini", "valor": 145000.0},
            "SR/FACCHINI BASCO": {"nome": "Semireboque Caçamba Basculante Facchini", "valor": 125000.0},
            "SR/FACCHINI FRIGO": {"nome": "Semireboque Baú Frigorífico Facchini", "valor": 190000.0},
            "REB/FACCHINI DOLLY": {"nome": "Reboque Dolly Facchini", "valor": 42000.0},
            "SR/FACCHINI CEGONHA": {"nome": "Semireboque Cegonheiro Facchini", "valor": 128000.0},
            "SR/FACCHINI PRANCHA": {"nome": "Semireboque Prancha Carrega Tudo Facchini", "valor": 150000.0},
            
            # === SÃO PEDRO ===
            "SR/S PEDRO CA GR": {"nome": "Semireboque Carga Aberta São Pedro", "valor": 75000.0},
            "SR/S PEDRO GRANE": {"nome": "Semireboque Graneleiro São Pedro", "valor": 95000.0},
            "SR/S PEDRO BAUM": {"nome": "Semireboque Baú Carga Geral São Pedro", "valor": 82000.0},
            "SR/S PEDRO SIDER": {"nome": "Semireboque Sider São Pedro", "valor": 88000.0},
            "SR/S PEDRO BASCO": {"nome": "Semireboque Caçamba São Pedro", "valor": 105000.0},
            
            # === LIBRELATO ===
            "SR/LIBRELATO CA GR": {"nome": "Semireboque Graneleiro Librelato", "valor": 104000.0},
            "SR/LIBRELATO SIDER": {"nome": "Semireboque Sider Alumínio Librelato", "valor": 99000.0},
            "SR/LIBRELATO BASCO": {"nome": "Semireboque Caçamba Basculante Librelato", "valor": 118000.0},
            "SR/LIBRELATO BAUM": {"nome": "Semireboque Baú Furgão Librelato", "valor": 91000.0},
            "SR/LIBRELATO TANK": {"nome": "Semireboque Tanque Combustível Librelato", "valor": 125000.0},
            "SR/LIBRELATO PORTA CON": {"nome": "Semireboque Porta Contêiner Librelato", "valor": 74000.0},
            "SR/LIBRELATO PRANCHA": {"nome": "Semireboque Carrega Tudo Librelato", "valor": 155000.0},
            
            # === GUERRA ===
            "SR/GUERRA GRANELEI": {"nome": "Semireboque Graneleiro Guerra (Orig.)", "valor": 98000.0},
            "SR/GUERRA SIDER": {"nome": "Semireboque Sider Guerra", "valor": 101000.0},
            "SR/GUERRA BAUM": {"nome": "Semireboque Baú Alumínio Guerra", "valor": 88000.0},
            "SR/GUERRA CA BASCO": {"nome": "Semireboque Caçamba Guerra", "valor": 112000.0},
            "SR/GUERRA PORTA CON": {"nome": "Semireboque Porta Contêiner Guerra", "valor": 70000.0},
            
            # === RODOFORT ===
            "SR/RODOFORT SIDER": {"nome": "Semireboque Sider Rodofort", "valor": 96000.0},
            "SR/RODOFORT BAUM": {"nome": "Semireboque Baú Carga Geral Rodofort", "valor": 89000.0},
            "SR/RODOFORT GRANELEI": {"nome": "Semireboque Graneleiro Rodofort", "valor": 101000.0},
            "SR/RODOFORT BASCO": {"nome": "Semireboque Caçamba Rodofort", "valor": 114000.0},
            
            # === PASTRE ===
            "SR/PASTRE CA BASCO": {"nome": "Semireboque Caçamba Basculante Pastre", "valor": 130000.0},
            "SR/PASTRE GRANELEI": {"nome": "Semireboque Graneleiro Pastre", "valor": 95000.0},
            "SR/PASTRE SIDER": {"nome": "Semireboque Sider Carga Geral Pastre", "valor": 94000.0},
            
            # === SCHIFFER ===
            "SR/SCHIFFER GR METAL": {"nome": "Semireboque Graneleiro Schiffer", "valor": 92000.0},
            "SR/SCHIFFER BAUM": {"nome": "Semireboque Baú Carga Geral Schiffer", "valor": 83000.0},
            "SR/SCHIFFER SIDER": {"nome": "Semireboque Sider Lonado Schiffer", "valor": 89000.0},
            "SR/SCHIFFER BASCO": {"nome": "Semireboque Caçamba Basculante Schiffer", "valor": 108000.0},
            
            # === RECRUSUL ===
            "SR/RECRUSUL FRIGO": {"nome": "Semireboque Frigorífico Recrusul", "valor": 185000.0},
            "SR/RECRUSUL BAUM": {"nome": "Semireboque Baú Furgão Alumínio Recrusul", "valor": 86000.0},
            "SR/RECRUSUL SIDER": {"nome": "Semireboque Sider Logística Recrusul", "valor": 93000.0},
            
            # === ANTONINI ===
            "SR/ANTONINI BAUM": {"nome": "Semireboque Baú Alumínio Antonini", "valor": 84000.0},
            "SR/ANTONINI SIDER": {"nome": "Semireboque Sider Carga Geral Antonini", "valor": 91000.0},
            
            # === GOTTI / METALES ===
            "SR/GOTTI PRANCHA": {"nome": "Semireboque Carrega Tudo Gotti", "valor": 155000.0},
            "SR/GOTTI BASCO": {"nome": "Semireboque Caçamba Basculante Gotti", "valor": 122000.0},
            
            # === TRIEL-HT ===
            "SR/TRIEL HT CA TANK": {"nome": "Semireboque Tanque Inox Triel-HT", "valor": 150000.0},
            "SR/TRIEL HT BASCO": {"nome": "Semireboque Caçamba Aço Triel-HT", "valor": 126000.0},
            
            # === KRONE ===
            "SR/KRONE SIDER": {"nome": "Semireboque Sider Krone (Importado)", "valor": 115000.0},
            
            # === SR IMPLEMENTOS ===
            "SR/SR IMPL CA GR": {"nome": "Semireboque Carga Aberta SR Implementos", "valor": 78000.0},
            "SR/SR IMPL BASCO": {"nome": "Semireboque Caçamba Mineração SR Impl", "valor": 110000.0}
        }

    def buscar_modelo(self, crlv_texto):
        """Busca no MongoDB Atlas. Se não encontrar, faz fallback na super lista."""
        crlv_limpo = crlv_texto.upper().strip()
        
        # 1. Tenta encontrar no banco dinâmico (registrados via aba Catálogo)
        resultado_db = self.colecao_catalogo.find_one({"crlv_resumido": crlv_limpo})
        if resultado_db:
            return {
                "nome_completo": resultado_db["nome_completo"],
                "valor_estimado_base": float(resultado_db["valor_estimado_base"])
            }
        
        # 2. Se o banco não tiver, consulta a nossa lista mestre estática
        if crlv_limpo in self.CATALOGO_INTERNO:
            return {
                "nome_completo": self.CATALOGO_INTERNO[crlv_limpo]["nome"],
                "valor_estimado_base": self.CATALOGO_INTERNO[crlv_limpo]["valor"]
            }
            
        return None

    def salvar_modelo_catalogo(self, marca, crlv, nome_completo, valor_base):
        """Permite a inserção de novos registros customizados ou regionais a qualquer momento."""
        documento = {
            "marca": marca.upper().strip(),
            "crlv_resumido": crlv.upper().strip(),
            "nome_completo": nome_completo.strip(),
            "valor_estimado_base": float(valor_base)
        }
        self.colecao_catalogo.update_one(
            {"crlv_resumido": documento["crlv_resumido"]},
            {"$set": documento},
            upsert=True
        )

    def salvar_analise(self, dados_laudo):
        self.colecao_laudos.insert_one(dados_laudo)

    def listar_laudos(self):
        return list(self.colecao_laudos.find().sort("data_analise", pymongo.DESCENDING))